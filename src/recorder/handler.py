import os
import subprocess
import uuid
import wave
from datetime import datetime
from pathlib import Path

import webrtcvad

from common.config.state import settings

CHUNK_BYTES = (settings.SAMPLE_RATE * settings.CHUNK_DURATION_MS // 1000) * 2  # 16-bit PCM
CHUNKS_PER_SECOND = 1000 // settings.CHUNK_DURATION_MS
SILENCE_CHUNKS_THRESHOLD = settings.SILENCE_DURATION_S * CHUNKS_PER_SECOND
RECORDINGS_DIR = Path(settings.TEMPORARY_DIRECTORY)

vad = webrtcvad.Vad(settings.VAD_AGGRESSIVENESS)


def main():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)
    sox_cmd = ["rec", "-t", "alsa", "default", "-t", "raw", "-r", str(settings.SAMPLE_RATE), "-c", "1", "-b", "16", "-"]
    process = subprocess.Popen(sox_cmd, stdout=subprocess.PIPE)
    state = "IDLE"
    silent_chunks = 0
    current_wave_file = None
    current_record_id = None
    current_file_started_time = None
    while True:
        audio_chunk = process.stdout.read(CHUNK_BYTES)
        if not audio_chunk:
            break
        is_speech = vad.is_speech(audio_chunk, settings.SAMPLE_RATE)
        if state == "IDLE":
            if is_speech:
                state = "RECORDING"
                silent_chunks = 0
                start_time = datetime.now()
                current_file_started_time = start_time
                current_record_id = uuid.uuid4()
                filename = f"{current_record_id}.wav"
                filepath = str(RECORDINGS_DIR / filename)
                current_wave_file = wave.open(filepath, "wb")
                current_wave_file.setnchannels(1)
                current_wave_file.setsampwidth(2)
                current_wave_file.setframerate(settings.SAMPLE_RATE)
        elif current_wave_file is not None and current_file_started_time is not None and state == "RECORDING":
            current_wave_file.writeframes(audio_chunk)
            if is_speech:
                silent_chunks = 0
            else:
                silent_chunks += 1
            current_file_finished_time = datetime.now()
            duration_since_start = (current_file_finished_time - current_file_started_time).total_seconds()
            if silent_chunks > SILENCE_CHUNKS_THRESHOLD or duration_since_start >= settings.MAX_FILE_DURATION_S:
                state = "IDLE"
                current_wave_file.close()
                if duration_since_start >= settings.MAX_FILE_DURATION_S and is_speech:
                    state = "IDLE"
                    is_speech = True
                    continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping application.")
