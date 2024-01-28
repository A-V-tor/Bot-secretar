import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopConfig:
    DASHBOARD_EXPENSE = '/admin/analytics/expense/'
    DASHBOARD_WEIGHT = '/admin/analytics/weight/'
    SECRET_KEY = 'secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'database.db'
    )
    FLASK_ADMIN_SWATCH = 'lumen'

    # почему-то не работает
    JSON_AS_ASCII = False


class ProductionConfig:
    DASHBOARD_EXPENSE = '/admin/analytics/expense/'
    DASHBOARD_WEIGHT = '/admin/analytics/weight/'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'database.db'
    )
    FLASK_ADMIN_SWATCH = 'lumen'

    # почему-то не работает
    JSON_AS_ASCII = False
