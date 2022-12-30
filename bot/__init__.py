from flask import Flask


def create_app():
    """Создание основного приложения."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.TestConfig")

    with app.app_context():

        from . import handlers

        return app
