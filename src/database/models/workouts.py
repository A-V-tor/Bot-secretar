from ..base import Base, session_factory
from sqlalchemy import BigInteger, String, Text, Boolean, and_, select, event, ForeignKey, extract
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload


class Workout(Base):
    __tablename__ = 'workouts'

    text_value: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey('users.telegram_id'), nullable=True
    )
    user: Mapped['User'] = relationship(
        'User', back_populates='workouts'
    )

    def __str__(self):
        return f"Тренировка: {self.updated_at} - {self.text_value}"

    @classmethod
    def new_workout(cls, telegram_id: int, text: str):
        with session_factory() as session:
            new_note = cls(value=text, user_telegram_id=telegram_id)

            session.add(new_note)
            session.commit()

            return True

    @classmethod
    def delete_note(cls, note_id: int):
        with session_factory() as session:
            query = select(cls).where(cls.id.is_(note_id))
            note =  session.scalar(query)
            if note:
                session.delete(note)
                session.commit()

                return True

            return False

    @classmethod
    def get_workouts_for_month(cls, telegram_id: int, month: int, year: int):

        with session_factory() as session:
            query = select(extract('day', cls.created_at)).where(
                and_(
                    cls.user_telegram_id == telegram_id,
                    extract('year', cls.created_at) == year,
                    extract('month', cls.created_at) == month,
                    cls.is_active.is_(True)
                )
            )
            result = session.execute(query).scalars().all()

            return [str(day) for day in result] if result else []

    @classmethod
    def get_workouts_for_timestamp(cls, telegram_id: int, day: int, month: int, year: int):
        with session_factory() as session:
            query = select(cls).where(
                and_(
                    cls.user_telegram_id == telegram_id,
                    extract('year', cls.created_at) == year,
                    extract('month', cls.created_at) == month,
                    extract('day', cls.created_at) == day,
                    cls.is_active.is_(True)
                )
            )
            result = session.execute(query).scalars().all()

            return result