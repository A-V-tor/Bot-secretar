from flask import Flask
from project.database.database import db
from project.database.models import MyWeight
from sqlalchemy import select


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopConfig')

    with app.app_context():
        return app


app = create_app()


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        weight, date = db.execute(select(MyWeight.value, MyWeight.date)).first()
        return f'На {date} вес составляет {weight} кг'
    except Exception:
        return 'Hi man'


def web_run():
    app.run()


if __name__ == '__main__':
    app.run()
