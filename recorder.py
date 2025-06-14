import os
import subprocess
import time
import uuid
import wave
from datetime import datetime

import webrtcvad

VAD_AGGRESSIVENESS = int(os.getenv("VAD_AGGRESSIVENESS", 1))
SILENCE_DURATION_S = int(os.getenv("SILENCE_DURATION_S", 2))
MAX_FILE_DURATION_S = int(os.getenv("MAX_FILE_DURATION_S", 600))
RECORDINGS_DIR = os.getenv("RECORDINGS_DIR", "recordings")

SAMPLE_RATE = 16000
CHUNK_DURATION_MS = 30
CHUNK_BYTES = (SAMPLE_RATE * CHUNK_DURATION_MS // 1000) * 2  # 16-bit PCM
CHUNKS_PER_SECOND = 1000 // CHUNK_DURATION_MS
SILENCE_CHUNKS_THRESHOLD = SILENCE_DURATION_S * CHUNKS_PER_SECOND

vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)


def main():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)
    sox_cmd = ["rec", "-t", "alsa", "default", "-t", "raw", "-r", str(SAMPLE_RATE), "-c", "1", "-b", "16", "-"]
    process = subprocess.Popen(sox_cmd, stdout=subprocess.PIPE)
    print("Sox process started. Listening for voice activity...")
    state = "IDLE"
    silent_chunks = 0
    current_wave_file = None
    current_record_id = None
    current_file_started_time = None
    while True:
        audio_chunk = process.stdout.read(CHUNK_BYTES)
        if not audio_chunk:
            break
        is_speech = vad.is_speech(audio_chunk, SAMPLE_RATE)
        print(is_speech)
        if state == "IDLE":
            if is_speech:
                state = "RECORDING"
                silent_chunks = 0
                start_time = datetime.now()
                current_file_started_time = start_time
                filename = f"{uuid.uuid4()}.wav"
                filepath = os.path.join(RECORDINGS_DIR, filename)
                current_wave_file = wave.open(filepath, "wb")
                current_wave_file.setnchannels(1)
                current_wave_file.setsampwidth(2)
                current_wave_file.setframerate(SAMPLE_RATE)
                print(f"Speech detected! Started recording to {filename}")
        elif state == "RECORDING":
            current_wave_file.writeframes(audio_chunk)
            if is_speech:
                silent_chunks = 0
            else:
                silent_chunks += 1
            duration_since_start = (datetime.now() - current_file_started_time).total_seconds()
            if silent_chunks > SILENCE_CHUNKS_THRESHOLD or duration_since_start >= MAX_FILE_DURATION_S:
                print("Stopping current recording segment...")
                state = "IDLE"
                current_wave_file.close()
                if duration_since_start >= MAX_FILE_DURATION_S and is_speech:
                    print("Max duration reached, but speech continues. Starting new file immediately.")
                    state = "IDLE"
                    is_speech = True
                    continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping application.")
