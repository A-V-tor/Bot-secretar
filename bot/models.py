import datetime
from . import db


class MyWeight(db.Model):
    __tablename__ = "myweight"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    value = db.Column(db.DECIMAL(2,4), default=0)