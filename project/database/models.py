import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Column, DECIMAL, DateTime, desc


class Base(DeclarativeBase):
    pass


class MyWeight(Base):
    __tablename__ = 'myweight'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(), default=datetime.datetime.now)
    value = Column(DECIMAL(2, 4), default=0)
