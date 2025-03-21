import typing

from sqlalchemy import (
    DECIMAL,
    ForeignKey,
    and_,
    extract,
    func,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, session_factory

if typing.TYPE_CHECKING:
    from src.database.models.users import User


class Weight(Base):
    __tablename__ = 'weight'

    value: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), nullable=True)
    user: Mapped['User'] = relationship('User', back_populates='weight')

    def __str__(self):
        return f'Вес: {self.value}'

    @classmethod
    def get_note_by_id(cls, note_id: int):
        with session_factory() as session:
            result = session.get(cls, note_id)

            return result

    @classmethod
    def new_note_weight(cls, telegram_id: int, weight: float):
        with session_factory() as session:
            new_note = cls(value=weight, user_telegram_id=telegram_id)

            session.add(new_note)
            session.commit()

            return True

    @classmethod
    def check_note_by_telegram_id(cls, telegram_id: int, year: int, month: int, day: int):
        with session_factory() as session:
            query = select(cls).where(
                and_(
                    cls.user_telegram_id == telegram_id,
                    extract('year', cls.created_at) == year,
                    extract('month', cls.created_at) == month,
                    extract('day', cls.created_at) == day,
                )
            )
            result = session.scalar(query)

            return result

    @classmethod
    def update_note_by_telegram_id(cls, note_id: int, weight: float):
        note = cls.get_note_by_id(note_id)
        if note:
            with session_factory() as session:
                note.value = weight

                session.add(note)
                session.commit()

                return True

    @classmethod
    def get_all_weight_notes_by_telegram_id(cls, telegram_id: int):
        with session_factory() as session:
            query = (
                select(cls.value, func.date(cls.created_at).label('date'))
                .filter(
                    cls.user_telegram_id == telegram_id  # Фильтрация по telegram_id
                )
                .order_by(func.date(cls.created_at))
            )

            result = session.execute(query).fetchall()

            return result
