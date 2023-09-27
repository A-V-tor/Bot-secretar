import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Integer,
    String,
    Column,
    DECIMAL,
    DateTime,
    Text,
    desc,
    event,
)


class Base(DeclarativeBase):
    pass


class MyWeight(Base):
    __tablename__ = 'myweight'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(), default=datetime.datetime.now)
    value = Column(DECIMAL(2, 4), default=0)


class MyWorkout(Base):
    __tablename__ = 'myworkout'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(), default=datetime.datetime.now)
    value = Column(Text)


class MyExpenses(Base):
    __tablename__ = 'myexpenses'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(), default=datetime.datetime.now)
    health = Column(Integer, default=0)
    transport = Column(Integer, default=0)
    food = Column(Integer, default=0)
    entertainment = Column(Integer, default=0)
    purchases = Column(Integer, default=0)
    present = Column(Integer, default=0)
    other = Column(Integer, default=0)


class DayReport(Base):
    __tablename__ = 'dayreport'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(), nullable=False)
    health = Column(Integer, default=0)
    transport = Column(Integer, default=0)
    food = Column(Integer, default=0)
    entertainment = Column(Integer, default=0)
    purchases = Column(Integer, default=0)
    present = Column(Integer, default=0)
    other = Column(Integer, default=0)


class MyNotes(Base):
    __tablename__ = 'mynotes'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(), nullable=False)
    note = Column(Text)

    def to_dict(self):
        return {
            key: value for key, value in self.__dict__.items() if key == 'note'
        }
