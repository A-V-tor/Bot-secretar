import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))


def get_config():
    """Получение настроек проекта."""

    env = os.getenv('FLASK_ENV', 'production')
    if env == 'development':
        return DevelopConfig
    else:
        return ProductionConfig


class DatabaseConfig:
    db_driver: str = os.getenv('DB_DRIVER')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('DB_PORT')
    db_name: str = os.getenv('DB_NAME')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')

    db_url = f'{db_driver}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'


class DevelopConfig:
    DASHBOARD_EXPENSE = os.getenv('DASHBOARD_EXPENSE')
    DASHBOARD_WEIGHT = os.getenv('DASHBOARD_WEIGHT')
    SECRET_KEY = 'secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'test-database.db'
    )
    BABEL_DEFAULT_LOCALE = 'ru'

    # почему-то не работает
    JSON_AS_ASCII = False

    BOT_TOKEN = os.getenv('token')
    URL_ADMIN = os.getenv('URL_ADMIN')


class ProductionConfig:
    DASHBOARD_EXPENSE = '/admin/analytics/expense/'
    DASHBOARD_WEIGHT = '/admin/analytics/weight/'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.db_url
    BABEL_DEFAULT_LOCALE = 'ru'

    # почему-то не работает
    JSON_AS_ASCII = False

    BOT_TOKEN = os.getenv('token')
    URL_ADMIN = os.getenv('URL_ADMIN')


settings = get_config()
