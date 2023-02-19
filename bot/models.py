import datetime
from sqlalchemy import text
from prettytable import PrettyTable

from . import db


class MyWeight(db.Model):
    __tablename__ = 'myweight'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    value = db.Column(db.DECIMAL(2, 4), default=0)


class MyNotes(db.Model):
    __tablename__ = 'mynotes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    note = db.Column(db.String(500))


class MyWorkouts(db.Model):
    __tablename__ = 'myworkout'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    entries = db.Column(db.String(255))


class MyNutrition(db.Model):
    __tablename__ = 'nutrition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String,
    )
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    proteins = db.Column(db.Integer)
    fats = db.Column(db.Integer)
    carbohydrates = db.Column(db.Integer)
    energy = db.Column(db.Integer)

    @classmethod
    def get_values(cls):
        """Текущие значения таблицы"""
        data = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),SUM(proteins),SUM(fats),SUM(carbohydrates),SUM(energy) FROM  nutrition  GROUP BY strftime("%Y-%m-%d",date) ORDER BY date DESC'
                )
            )
        ][0]
        if len(data) < 1:
            return 'Нет записей за сегодня'
        else:
            mytable = PrettyTable()
            mytable.field_names = [
                'Категория',
                'Значение',
            ]

            mytable.add_row(['Белки', data[1]])
            mytable.add_row(['Жиры', data[2]])
            mytable.add_row(['Углеводы', data[3]])
            mytable.add_row(['Калории', data[4]])

            return f'<pre>{data[0]}\n{mytable}</pre>'
