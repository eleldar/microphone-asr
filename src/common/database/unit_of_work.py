from __future__ import annotations

import abc

from common.repository import RecordRepository
from services.config import db_session


class IUoW(abc.ABC):
    def __init__(self, db_session=db_session):
        self.db_session = db_session

    def __enter__(self) -> IUoW:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class RecordUoW(IUoW):
    def __enter__(self) -> RecordUoW:
        self.db = self.db_session()
        self.files = RecordRepository(self.db)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.db.close()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()
