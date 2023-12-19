import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError
from sqlalchemy import (
    Integer,
    String,
    Column,
    DECIMAL,
    DateTime,
    Date,
    Boolean,
    Text,
    Enum,
    extract,
    func,
)
from project.database.database import db


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

    @classmethod
    def get_total_category_values_for_the_current_day(cls):
        """Получить общие значения категорий за текущий день."""
        today = datetime.date.today()
        year, month, day = str(today).split('-')
        query_ = (
            db.query(
                func.sum(cls.health).label('total_health'),
                func.sum(cls.transport).label('total_transport'),
                func.sum(cls.food).label('total_food'),
                func.sum(cls.entertainment).label('total_entertainment'),
                func.sum(cls.purchases).label('total_purchases'),
                func.sum(cls.present).label('total_present'),
                func.sum(cls.other).label('total_other'),
            )
            .filter(
                extract('year', cls.date) == year,
                extract('month', cls.date) == month,
                extract('day', cls.date) == day,
            )
            .first()
        )

        return query_


class DayReport(Base):
    __tablename__ = 'dayreport'
    id = Column(Integer, primary_key=True)
    date = Column(Date(), nullable=False, unique=True)
    health = Column(Integer, default=0)
    transport = Column(Integer, default=0)
    food = Column(Integer, default=0)
    entertainment = Column(Integer, default=0)
    purchases = Column(Integer, default=0)
    present = Column(Integer, default=0)
    other = Column(Integer, default=0)

    @classmethod
    def make_record_to_day(cls, query_):
        new_report_the_day = DayReport(
            date=datetime.date.today(),
            health=query_.total_health,
            transport=query_.total_transport,
            food=query_.total_food,
            entertainment=query_.total_entertainment,
            purchases=query_.total_purchases,
            present=query_.total_present,
            other=query_.total_other,
        )
        try:
            db.add(new_report_the_day)
            db.commit()
        except IntegrityError:
            # Обработка нарушения уникальности 1 день - 1 запись
            db.rollback()


class MyNotes(Base):
    __tablename__ = 'mynotes'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(), nullable=False)
    note = Column(Text)

    def to_dict(self):
        return {
            key: value for key, value in self.__dict__.items() if key == 'note'
        }


class MyReminders(Base):
    __tablename__ = 'myreminders'
    id = Column(Integer, primary_key=True)
    createAt = Column(DateTime(), nullable=False)
    updateAt = Column(DateTime(), nullable=False)
    scheduledAt = Column(DateTime(), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    comment = Column(String)
    importance_level = Column(
        Enum('Very important', 'Important', "Don't miss it", "Doesn't matter")
    )

    @classmethod
    def get_reminder(cls):
        """Запрос напоминания на текущую минуту."""
        today = datetime.date.today()
        year, month, day = str(today).split('-')
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        reminder: MyReminders = (
            db.query(cls)
            .filter(
                extract('year', cls.scheduledAt) == year,
                extract('month', cls.scheduledAt) == month,
                extract('day', cls.scheduledAt) == day,
                cls.is_active == True,
                extract('hour', cls.scheduledAt) == hour,
                extract('minute', cls.scheduledAt) == minute,
            )
            .order_by(cls.scheduledAt)
            .first()
        )

        return reminder
