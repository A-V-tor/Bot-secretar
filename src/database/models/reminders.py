import typing
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    and_,
    extract,
    select,
    update,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.utils.tools import ReminderLevel

from ..base import Base, session_factory

if typing.TYPE_CHECKING:
    from src.database.models.users import User


class Reminder(Base):
    __tablename__ = 'reminders'

    value: Mapped[Text] = mapped_column(Text, nullable=False)
    type_expenses: Mapped[ReminderLevel] = mapped_column(
        ENUM(ReminderLevel, name='reminderlevel'),
        nullable=False,
    )
    datetime_reminder: Mapped[datetime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='reminders')

    def __str__(self):
        return f'Напоминание: {self.datetime_reminder} - {self.user_telegram_id}'

    @classmethod
    def add_new_note(
        cls,
        telegram_id: int,
        value: str,
        type_expenses: ReminderLevel,
        datetime_reminder: datetime,
    ):
        with session_factory() as session:
            new_note = cls(
                user_telegram_id=telegram_id,
                value=value,
                type_expenses=type_expenses,
                datetime_reminder=datetime_reminder,
            )

            session.add(new_note)
            session.commit()

            return True

    @classmethod
    def get_reminders_for_month(cls, telegram_id: int, month: int, year: int):
        """Получить записи на текущий месяц (активные)."""
        with session_factory() as session:
            query = select(extract('day', cls.datetime_reminder)).where(
                and_(
                    cls.user_telegram_id == telegram_id,
                    extract('year', cls.datetime_reminder) == year,
                    extract('month', cls.datetime_reminder) == month,
                    cls.is_active.is_(True),
                )
            )
            result = session.execute(query).scalars().all()

            return [str(day) for day in result] if result else []

    @classmethod
    def get_reminders_for_current_minute(cls, day: int, month: int, year: int, hour: int, minutes: int):
        """Получение записей с напоминаниями на текущую минуту."""
        with session_factory() as session:
            query = select(cls).where(
                and_(
                    extract('day', cls.datetime_reminder) == day,
                    extract('month', cls.datetime_reminder) == month,
                    extract('year', cls.datetime_reminder) == year,
                    extract('hour', cls.datetime_reminder) == hour,
                    extract('minutes', cls.datetime_reminder) == minutes,
                    cls.is_active.is_(True),
                )
            )
            result = session.execute(query).scalars().all()

            return result

    @classmethod
    def disable_reminder(cls, id_note: int):
        """Изменить статус записи на неактивно."""
        with session_factory() as session:
            stmt = update(cls).where(cls.id == id_note).values(is_active=False).returning(cls.id, cls.is_active)
            result = session.execute(stmt)
            session.commit()

            return result
