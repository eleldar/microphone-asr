from sqlalchemy import Column, Float, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from common.domain.record import Record

metadata = MetaData()
mapper_registry = registry()

records = Table(
    "records",
    metadata,
    Column("record_id", String, primary_key=True),
    Column("filename", String, nullable=True),
    Column("filesize", Integer, nullable=True),
    Column("start_time", Float, nullable=True),
    Column("end_time", Float, nullable=True),
)


def start_mappers():
    mapper_registry.map_imperatively(Record, records)
