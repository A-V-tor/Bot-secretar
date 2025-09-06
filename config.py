import inspect
import logging
import os
import sys
from typing import Optional, Union

from dotenv import find_dotenv, load_dotenv
from loguru import logger

load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))


class InterceptHandler(logging.Handler):
    """
    Обработчик (из документации `loguru`) ловит все сообщения от стандартного `logging` и передаёт их в `loguru`.
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: Union[str, int]
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def get_config():
    """Получение настроек проекта."""
    env = os.getenv('FLASK_ENV', 'production')
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    if env == 'development':
        return DevelopConfig()
    else:
        return ProductionConfig()


class LoggerConfig:
    logger = logger

    def custom_filter(self, record: dict):
        """
        Фильтрация записи в файл.
        """
        return True if self.file_name == record.get('extra').get('logger') else False

    def __init__(
        self,
        file_name,
        extra_format='{extra[logger]} {message}',
    ) -> None:
        self.file_name = file_name

        custom_filter = self.custom_filter

        self.logger.add(
            f'logs/{file_name}.log',
            backtrace=True,
            diagnose=True,
            rotation='20 MB',
            retention=5,
            format=extra_format,
            filter=custom_filter,
            enqueue=True,
        )


class DatabaseConfig:
    dokku_deploy: str | None = os.getenv('IS_DOKKU') or None
    db_driver: str = os.getenv('DB_DRIVER') or 'postgresql+psycopg2'
    db_host: str = os.getenv('DB_HOST') or 'localhost'
    db_port: str = os.getenv('DB_PORT') or '5432'
    db_name: str = os.getenv('DB_NAME') or 'postgres'
    db_user: str = os.getenv('DB_USER') or 'postgres'
    db_pass: str = os.getenv('DB_PASS') or 'postgres'

    db_url = (
        f'{db_driver}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
        if not dokku_deploy
        else os.getenv('DATABASE_URL')
    )


class DevelopConfig:
    DASHBOARD_EXPENSE = os.getenv('DASHBOARD_EXPENSE')
    DASHBOARD_WEIGHT = os.getenv('DASHBOARD_WEIGHT')
    SECRET_KEY = 'secret-key'
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.db_url
    BABEL_DEFAULT_LOCALE = 'ru'

    # почему-то не работает
    JSON_AS_ASCII = False

    BOT_TOKEN = os.getenv('token')
    URL_ADMIN = os.getenv('URL_ADMIN')

    def __name__(self):
        return 'DevelopConfig'

    def __init__(self) -> None:
        self.web_logger = LoggerConfig('web', '{extra[logger]} {message}').logger.bind(logger='web')
        self.bot_logger = LoggerConfig('bot', '{extra[logger]} {message}').logger.bind(logger='bot')


class ProductionConfig:
    DASHBOARD_EXPENSE = os.getenv('DASHBOARD_EXPENSE')
    DASHBOARD_WEIGHT = os.getenv('DASHBOARD_WEIGHT')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.db_url
    BABEL_DEFAULT_LOCALE = 'ru'

    # почему-то не работает
    JSON_AS_ASCII = False

    BOT_TOKEN = os.getenv('token')
    URL_ADMIN = os.getenv('URL_ADMIN')

    def __name__(self):
        return 'ProductionConfig'

    def __init__(self) -> None:
        self.web_logger = LoggerConfig('web', '{extra[logger]} {message}').logger.bind(logger='web')
        self.bot_logger = LoggerConfig('bot', '{extra[logger]} {message}').logger.bind(logger='bot')


settings = get_config()
