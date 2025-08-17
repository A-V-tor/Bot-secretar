"""Заполнение базы данных базовыми записями (фикстурами)"""

from src.database.base import TimeZone
from src.utils.tools import TimeZoneEnum


def add_timezones_records():
    """Добавление записей о временных зонах в базу данных"""
    for timezone in TimeZoneEnum:
        TimeZone.add_record(timezone)


if __name__ == '__main__':
    add_timezones_records()
