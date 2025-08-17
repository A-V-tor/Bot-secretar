import typing
from datetime import datetime

from sqlalchemy import DateTime, Integer, create_engine, func, select
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

from config import settings
from src.utils.tools import TimeZoneEnum

if typing.TYPE_CHECKING:
    from src.database.models.users import User


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_timeout=60,
    # echo=True
)

session_factory = sessionmaker(
    engine,
    expire_on_commit=False,
)


def get_session():
    with session_factory() as session:
        yield session


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class TimeZone(Base):
    __tablename__ = 'time_zones'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time_zones: Mapped[TimeZoneEnum] = mapped_column(ENUM(TimeZoneEnum, name='timezones'), nullable=False, unique=True)
    users: Mapped[list['User']] = relationship('User', back_populates='time_zones')

    @classmethod
    def add_record(cls, time_zone: TimeZoneEnum):
        with session_factory() as session:
            stmt = cls(
                time_zones=time_zone,
            )
            session.add(stmt)
            try:
                session.commit()
                return stmt
            except IntegrityError:
                session.rollback()
                print(f"Часовой пояс '{time_zone.value}' уже существует")

    @classmethod
    async def get_time_zone_id(cls, timezone_string: str) -> int:
        with session_factory() as session:
            query = select(cls).where(cls.time_zones == TimeZoneEnum.get_offset(timezone_string))
            result = session.execute(query).scalar_one_or_none()
            return result.id
