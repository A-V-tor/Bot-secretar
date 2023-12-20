"""Импорты задач дся Celery используються неявно при запуске."""
import datetime
from celery import Celery
import os
import urllib

from celery.schedules import crontab

from .expense_journal import make_a_report_for_the_day
from .reminders_journal import make_check_for_reminders

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
password_redis = os.environ.get('REDIS_KEY')
encoded_password = urllib.parse.quote(password_redis, safe='')


app = Celery(
    'tasks',
    broker=f'redis://:{encoded_password}@localhost:6379',
    backend=f'redis://:{encoded_password}@localhost:6379',
)
app.conf.update(
    task_ignore_result=False,
    timezone='Europe/Moscow',
)
app.conf.beat_schedule = {
    'task-reminders': {
        'task': 'project.telegram.reminders_journal.make_check_for_reminders',
        'schedule': 60.0,
    },
    'task-report': {
        'task': 'project.telegram.expense_journal.make_a_report_for_the_day',
        'schedule': crontab(hour=23, minute=55),
    },
}
