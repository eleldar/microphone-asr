from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SAMPLE_RATE: int = Field(default=16000, description="Sample rate")
    CHUNK_DURATION_MS: int = Field(default=30, description="Chunk duration (ms)")
    VAD_AGGRESSIVENESS: int = Field(default=1, description="VAD aggressiveness")
    SILENCE_DURATION_S: int = Field(default=2, description="Silence duration (sec)")
    MAX_FILE_DURATION_S: int = Field(default=10, description="Max file duration (sec)")
    TEMPORARY_DIRECTORY: str = Field(default="tempdir", description="Temporary directory to records")

    MICROPHONE_ASR_DB_TYPE: str = Field(default="postgresql", description="DB type")
    MICROPHONE_ASR_DB_HOST: str = Field(default="db", description="DB host")
    MICROPHONE_ASR_DB_PORT: int = Field(default=5432, description="DB port")
    MICROPHONE_ASR_DB_NAME: str = Field(default="microphone_asr_name", description="DB name")
    MICROPHONE_ASR_DB_USER: str = Field(default="microphone_asr_user", description="DB user")
    MICROPHONE_ASR_DB_PASSWORD: str = Field(description="DB password")

    MICROPHONE_ASR_FILE_STORAGE_HOST: str = Field(default="minio", description="File storage host")
    MICROPHONE_ASR_FILE_STORAGE_PORT: int = Field(default=9000, description="File storage port")
    MICROPHONE_ASR_FILE_STORAGE_BUCKET_NAME: str = Field(default="records", description="File storage bucket name")
    MICROPHONE_ASR_FILE_STORAGE_ACCESS_KEY: str = Field(description="File storage access key")
    MICROPHONE_ASR_FILE_STORAGE_SECRET_KEY: str = Field(description="File storage secret key")

    MICROPHONE_ASR_VECTOR_STORAGE_HOST: str = Field(default="qdrant", description="Vector storage host")
    MICROPHONE_ASR_VECTOR_STORAGE_PORT: int = Field(default=9200, description="Vector storage port")
    MICROPHONE_ASR_VECTOR_STORAGE_USERNAME: str = Field(default="qdrant", description="Vector storage username")
    MICROPHONE_ASR_VECTOR_STORAGE_PASSWORD: str = Field(description="Vector storage password")

    OPENAI_API_MODEL: str = Field(default="google/gemma-3-27b-it", description="Default LLM")
    OPENAI_API_HOST: str = Field(default="http://10.21.209.162:11435/v1", description="Openai API URL")
    OPENAI_API_KEY: str = Field(description="Openai API key")

    DEBUG: int = Field(default=0, description="Debug mode flag")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
