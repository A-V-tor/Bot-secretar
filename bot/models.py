import datetime
from . import db


class MyWeight(db.Model):
    __tablename__ = "myweight"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    value = db.Column(db.DECIMAL(2, 4), default=0)


class MyNotes(db.Model):
    __tablename__ = "mynotes"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    note = db.Column(db.String(500))


class MyWorkouts(db.Model):
    __tablename__ = "myworkout"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    entries = db.Column(db.String(255))
