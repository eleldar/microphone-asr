from __future__ import annotations

from typing import List, Optional

from common.utils.time_formatter import get_string_time

from .base import IDomain


class Record(IDomain):
    def __init__(self, record_id: str, filename: str, filesize: int, start_time: float, end_time: float):
        self.record_id = record_id
        self.filename = filename
        self.filesize = filesize
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other):
        if not isinstance(other, Record):
            return False
        return self.record_id == other.record_id

    def __lt__(self, other):
        if not isinstance(other, Record):
            return NotImplemented
        return self.start_time < other.start_time

    def __le__(self, other):
        if not isinstance(other, Record):
            return NotImplemented
        return self.start_time <= other.start_time

    def __gt__(self, other):
        if not isinstance(other, Record):
            return NotImplemented
        return self.start_time > other.start_time

    def __ge__(self, other):
        if not isinstance(other, Record):
            return NotImplemented
        return self.start_time >= other.start_time

    def __hash__(self):
        return hash(self.record_id)

    def __str__(self):
        start_time = get_string_time(self.start_time)
        end_time = get_string_time(self.end_time)
        return f"file: {self.record_id}: {start_time} - {end_time}"

    def __bool__(self):
        return bool(self.filesize and self.end_time > self.start_time)
