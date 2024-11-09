from datetime import datetime
from typing import AsyncGenerator, Generator

from sqlalchemy import Boolean, DateTime, Integer, func

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from sqlalchemy import create_engine

from config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_timeout=60,
    # echo=True
)

session_factory = sessionmaker(
    engine,
    expire_on_commit=False,
)


def get_session() -> Generator[Session, None, None]:
    with session_factory() as session:
        yield session