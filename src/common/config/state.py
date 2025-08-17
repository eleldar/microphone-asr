from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.database.orm import metadata, start_mappers

from .settings import Settings

settings = Settings()

if settings.DEBUG:
    pass

try:
    DB_URI = (
        f"{settings.MICROPHONE_ASR_DB_TYPE}://{settings.MICROPHONE_ASR_DB_USER}:{settings.MICROPHONE_ASR_DB_PASSWORD}@"
        f"{settings.MICROPHONE_ASR_DB_HOST}:{settings.MICROPHONE_ASR_DB_PORT}/{settings.MICROPHONE_ASR_DB_NAME}"
    )
    metadata.create_all(bind=create_engine(DB_URI))
    start_mappers()
    db_session = sessionmaker(bind=create_engine(DB_URI))
except Exception as error:
    print(f"⚠️ Database not available: {error}")
    db_session = None
