import requests

from celery import shared_task

import os
from project.database.database import db
from project.database.models import MyReminders
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


API_TOKEN = os.getenv('token')
CHAT_ID = os.getenv('CHAT_ID')


@shared_task()
def make_check_for_reminders():
    """Проверка напоминаний и их отправка в телеграм."""
    reminder = MyReminders.get_reminder()

    if reminder:
        status = True
        while status:
            msg = attach_tags_to_message(
                reminder.importance_level, reminder.comment
            )
            res = requests.get(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}'
            )
            if res.status_code == 200:
                status = False
                reminder.is_active = status
                db.commit()


def attach_tags_to_message(importance_level, msg):
    """Дополнение сообщения в зависимсоти от уровня важности."""
    title = ' НАПОМИНАНИЕ\n\n'
    if importance_level == 'Very important':
        tags = f'❗️ ❗️ ❗️ ❗️ ❗️️\n ```{msg}```\n️❗️ ❗️ ❗️ ❗️ ❗'
    if importance_level == 'Important':
        tags = f'❓️ ❓ ❓ ❓ ❓\n ```{msg}```\n️❓ ❓ ❓ ❓ ❓'
    if importance_level == "Don't miss it":
        tags = f'❕️ ❕ ❕ ❕ ❕\n ```{msg}```\n️❕ ❕ ❕ ❕ ❕'
    if importance_level == "Doesn't matter":
        tags = f'\n ```{msg}```\n️'

    reminder = title + tags

    return reminder
