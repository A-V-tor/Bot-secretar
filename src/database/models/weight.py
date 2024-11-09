from ..base import Base, session_factory
from sqlalchemy import Integer, DECIMAL, Text, desc, and_, select, func, ForeignKey, extract
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload



class Weight(Base):
    __tablename__ = 'weight'

    value: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey('users.telegram_id'), nullable=True
    )
    user: Mapped['User'] = relationship(
        'User', back_populates='weight'
    )

    def __str__(self):
        return f"Вес: {self.value}"

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
                note.text_value = weight

                session.add(note)
                session.commit()

                return True
