import os


basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig:
    SECRET_KEY = "secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")
    FLASK_ADMIN_SWATCH = 'lumen'
