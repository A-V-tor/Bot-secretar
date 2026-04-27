from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base, session_factory


class Variables(Base):
    """Модель переменных для сервисов и API.

    provider_auth_key: ключ провайдера модели нейросети
    telegram_proxy: url прокси для работы с API  телеграм
    """

    __tablename__ = 'variables'

    provider_auth_key: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    telegram_proxy: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)

    @classmethod
    def get_variables(cls):
        with session_factory() as session:
            query = select(cls)
            result = session.execute(query).scalar_one_or_none()

            return result
