import typing

from sqlalchemy import (
    ForeignKey,
    Integer,
    and_,
    desc,
    extract,
    func,
    select,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.utils.tools import TypeExpenses

from ..base import Base, session_factory

if typing.TYPE_CHECKING:
    from src.database.models.users import User


class Expenses(Base):
    __tablename__ = 'expenses'

    type_expenses: Mapped[TypeExpenses] = mapped_column(
        ENUM(TypeExpenses, name='typeexpenses'),
        nullable=False,
    )
    value: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), nullable=True)
    user: Mapped['User'] = relationship('User', back_populates='expenses')

    def __str__(self):
        return f'Трата: {self.type_expenses} | {self.value} | {self.updated_at}'

    @classmethod
    def get_note_by_id(cls, note_id: int):
        with session_factory() as session:
            result = session.get(cls, note_id)

            return result

    @classmethod
    def get_expenses_for_day(cls, telegram_id: int, day: int, month: int, year: int):
        with session_factory() as session:
            query = (
                select(cls.type_expenses, func.sum(cls.value).label('total_value'))
                .where(
                    and_(
                        cls.user_telegram_id == telegram_id,
                        extract('year', cls.created_at) == year,
                        extract('month', cls.created_at) == month,
                        extract('day', cls.created_at) == day,
                    )
                )
                .group_by(cls.type_expenses)
            )

            result = session.execute(query).fetchall()

            return result

    @classmethod
    def add_new_note(cls, telegram_id: int, money: int, type_expenses: str):
        with session_factory() as session:
            new_note = cls(
                type_expenses=type_expenses,
                user_telegram_id=telegram_id,
                value=money,
            )

            session.add(new_note)
            session.commit()

            return True

    @classmethod
    def get_last_note_for_current_day(cls, year: int, month: int, day: int):
        with session_factory() as session:
            query = (
                select(cls)
                .where(
                    and_(
                        extract('year', cls.created_at) == year,
                        extract('month', cls.created_at) == month,
                        extract('day', cls.created_at) == day,
                    )
                )
                .order_by(desc(cls.updated_at))
                .limit(1)
            )

            result = session.scalar(query)

            return result

    @classmethod
    def update_last_note_for_current_day(cls, note_id: int, money: int, category: str):
        note: cls = cls.get_note_by_id(note_id)
        if note:
            with session_factory() as session:
                note.value = money
                if category != 'current':
                    note.type_expenses = category.split('.')[-1]

                session.add(note)
                session.commit()

                return True

    @classmethod
    def get_all_expenses_by_telegram_id(cls, telegram_id: int):
        with session_factory() as session:
            query = (
                select(
                    cls.type_expenses,
                    func.date(cls.created_at).label('date'),  # Преобразуем created_at в дату (убираем время)
                    func.sum(cls.value).label('total_value_daily'),  # Сумма расходов за день
                )
                .filter(
                    cls.user_telegram_id == telegram_id  # Фильтрация по telegram_id
                )
                .group_by(
                    cls.type_expenses,  # Группируем по типу расходов
                    func.date(cls.created_at),  # И по дате (убираем время)
                )
                .order_by(
                    func.date(cls.created_at)  # .desc()  # Можно отсортировать по дате, если нужно
                )
            )

            result = session.execute(query).fetchall()

            return result
