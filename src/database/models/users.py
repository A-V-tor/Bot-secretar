import typing

from src.database.models.reminders import Reminder
from ..base import Base, session_factory
from flask_login import UserMixin
from sqlalchemy import BigInteger, String, Text, Boolean, select, event
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.utils.tools import UserPermissions, generate_password
from sqlalchemy.dialects.postgresql import ENUM

if typing.TYPE_CHECKING:
    from src.database.models.expenses import Expenses
    from src.database.models.workouts import Workout
    from src.database.models.weight import Weight


class User(Base, UserMixin):
    """
    Модель пользователя.

    username: никнейм пользователя
    psw: пароль пользователя
    first_surname: фамилия
    last_surname: отчество
    description: описание
    telegram_id: идентификатор телеграм
    is_active: флаг актуальности записи
    """

    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    psw: Mapped[str] = mapped_column(String(255))
    permission: Mapped[UserPermissions] = mapped_column(
        ENUM(UserPermissions), default=UserPermissions.user, nullable=True
    )
    first_surname: Mapped[str] = mapped_column(String(255), nullable=True)
    last_surname: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger(), nullable=False, index=True, unique=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    workouts: Mapped[list['Workout']] = relationship(
        'Workout', back_populates='user', uselist=True
    )
    expenses: Mapped[list['Expenses']] = relationship(
        'Expenses', back_populates='user', uselist=True
    )
    weight: Mapped[list['Weight']] = relationship(
        'Weight', back_populates='user', uselist=True
    )
    reminders: Mapped[list['Reminder']] = relationship(
        'Reminder', back_populates='user', uselist=True
    )

    def __str__(self):
        return f'Пользователь: {self.username} - {self.telegram_id}'

    @classmethod
    def create_user(
        cls,
        username: str,
        telegram_id: int,
        first_surname: str | None = None,
        last_surname: str | None = None,
    ):
        generate_psw = generate_password()

        with session_factory() as session:
            stmt = cls(
                username=username,
                psw=generate_psw,
                telegram_id=telegram_id,
                first_surname=first_surname,
                last_surname=last_surname,
            )

            session.add(stmt)
            session.commit()

            return generate_psw

    @classmethod
    def get_user_by_telegram_id(cls, telegram_id: int):

        with session_factory() as session:
            query = select(cls).where(cls.telegram_id == telegram_id)
            result = session.execute(query).scalar_one_or_none()

            return result

    @classmethod
    def get_user_by_username(cls, username: str):
        with session_factory() as session:
            query = select(cls).where(cls.username == username)
            result = session.execute(query).scalar_one_or_none()

            return result

    @classmethod
    def get_user_by_id(cls, note_id: int):
        with session_factory() as session:
            result = session.get(cls, note_id)

            return result

    @classmethod
    def set_new_password(cls, password: str, telegram_id: int):
        with session_factory() as session:
            user = cls.get_user_by_telegram_id(telegram_id)
            if user:
                user.psw = generate_password_hash(password)
                session.add(user)
                session.commit()

                return password


# хеширование пароля перед записью в бд
@event.listens_for(User, 'before_insert')
def hash_password(mapper, connection, target):
    """Хеширование пароля перед записью в бд."""

    target.psw = generate_password_hash(target.psw)
