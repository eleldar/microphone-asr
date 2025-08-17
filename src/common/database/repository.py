import abc
from typing import List, Optional

from domain.base import IDomain
from domain.record import Record
from sqlalchemy.orm.session import Session


class IRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, data: IDomain, foreign_key: Optional[str] = None) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, object_id: str) -> IDomain:
        raise NotImplementedError


class RecordRepository(IRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, data: Record) -> None:     ■ Method "add" overrides clas
        self.db.add(data)

    def get(self, object_id: str) -> Record:
        return self.db.query(Record).filter_by(user_id=object_id).first()

    def list(self) -> List[Record]:
        query = self.db.query(Record).all()
        return sorted(query, key=lambda x: x.start_time, reverse=True)

    def delete(self, object_id: str) -> None:
        record = self.get(object_id)
        if record is not None:
            self.db.delete(record)

