import calendar
import datetime

import pytz
from aiogram.types import (
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models.users import User
from src.utils.tools import get_next_month_and_year, get_prev_month_and_year


async def reminders_kb():
    keyboard = InlineKeyboardBuilder()
    root_menu = InlineKeyboardButton(text='🗂', callback_data='start')
    current_reminders = InlineKeyboardButton(text='добавить', callback_data='reminder-add')
    reminder_add = InlineKeyboardButton(text='текущие', callback_data='show-reminders')
    keyboard.row(root_menu).row(reminder_add).row(current_reminders)

    return keyboard.as_markup()


async def render_reminders_calendar(tg_id: int, month: int, year: int, reminder_days: list):
    """Отрисовка календаря напоминаний в клавиатуре для просмотра записей."""
    user = User.get_user_by_telegram_id(tg_id)
    user_tz = pytz.timezone(user.time_zones[0].time_zones.value)
    now = user_tz.localize(datetime.datetime.now())

    keyboard = InlineKeyboardBuilder()
    cl = calendar.TextCalendar(firstweekday=0)
    days_current_month = [day for day in cl.itermonthdays(year, month)]

    keyboard.row(
        InlineKeyboardButton(text='Пн', callback_data='-'),
        InlineKeyboardButton(text='Вт', callback_data='-'),
        InlineKeyboardButton(text='Ср', callback_data='-'),
        InlineKeyboardButton(text='Чт', callback_data='-'),
        InlineKeyboardButton(text='Пт', callback_data='-'),
        InlineKeyboardButton(text='Сб', callback_data='-'),
        InlineKeyboardButton(text='Вс', callback_data='-'),
    )

    count_days = 0

    for day in days_current_month:
        if day != 0:
            if str(day) in reminder_days:
                reminder_date = user_tz.localize(datetime.datetime(year, month, day))
                emoji = '⏰' if reminder_date > now else '⭕'

                reminder_button = InlineKeyboardButton(text=emoji, callback_data=f'rmndrs_show-{day}-{month}-{year}')
                if count_days % 7 == 0:
                    keyboard.row(reminder_button)
                else:
                    keyboard.add(reminder_button)
            else:
                not_reminder_button = InlineKeyboardButton(
                    text=f' {day} ',
                    callback_data=f'rmndrs{day}-{month}-{year}',
                )
                if count_days % 7 == 0:
                    keyboard.row(not_reminder_button)
                else:
                    keyboard.add(not_reminder_button)
        else:
            # заглушки дней других месяцев
            empty_button = InlineKeyboardButton(text=' ', callback_data='_')

            if count_days % 7 == 0:
                keyboard.row(empty_button)
            else:
                keyboard.add(empty_button)
        count_days += 1

    prev_month, prev_year = await get_prev_month_and_year(month, year)
    next_month, next_year = await get_next_month_and_year(month, year)
    keyboard.row(
        InlineKeyboardButton(text='<<', callback_data=f'rmndrs-{prev_month} {prev_year}'),
        InlineKeyboardButton(text='>>', callback_data=f'rmndrs+{next_month} {next_year}'),
    )
    keyboard.row(InlineKeyboardButton(text='назад', callback_data='reminders'))
    keyboard.row(InlineKeyboardButton(text='🗂', callback_data='start'))

    return keyboard.as_markup()


async def select_hour_timestamp():
    keyboard = InlineKeyboardBuilder()
    root_menu = InlineKeyboardButton(text='🗂', callback_data='start')

    for i in range(1, 25):
        hour = InlineKeyboardButton(text=f'{i}', callback_data=f'rmndr-hour-{i}')
        keyboard.add(hour)

    keyboard.row(root_menu)

    return keyboard.as_markup()


async def select_minutes_timestamp():
    keyboard = InlineKeyboardBuilder()
    root_menu = InlineKeyboardButton(text='🗂', callback_data='start')

    for i in range(0, 60):
        i = f'0{i}' if i < 10 else i
        minutes = InlineKeyboardButton(text=f'{i}', callback_data=f'rmndr-minutes-{i}')
        keyboard.add(minutes)

    keyboard.row(root_menu)

    return keyboard.as_markup()


async def render_reminders_calendar_for_input(month: int, year: int):
    """Отрисовка календаря напоминаний в клавиатуре для добавления записи."""
    keyboard = InlineKeyboardBuilder()
    cl = calendar.TextCalendar(firstweekday=0)
    days_current_month = [day for day in cl.itermonthdays(year, month)]

    keyboard.row(
        InlineKeyboardButton(text='Пн', callback_data='-'),
        InlineKeyboardButton(text='Вт', callback_data='-'),
        InlineKeyboardButton(text='Ср', callback_data='-'),
        InlineKeyboardButton(text='Чт', callback_data='-'),
        InlineKeyboardButton(text='Пт', callback_data='-'),
        InlineKeyboardButton(text='Сб', callback_data='-'),
        InlineKeyboardButton(text='Вс', callback_data='-'),
    )

    count_days = 0

    for day in days_current_month:
        if day != 0:
            not_reminder_button = InlineKeyboardButton(
                text=f' {day} ',
                callback_data=f'rmndrsnew-{day}-{month}-{year}',
            )
            if count_days % 7 == 0:
                keyboard.row(not_reminder_button)
            else:
                keyboard.add(not_reminder_button)
        else:
            # заглушки дней других месяцев
            empty_button = InlineKeyboardButton(text=' ', callback_data='_')

            if count_days % 7 == 0:
                keyboard.row(empty_button)
            else:
                keyboard.add(empty_button)
        count_days += 1

    prev_month, prev_year = await get_prev_month_and_year(month, year)
    next_month, next_year = await get_next_month_and_year(month, year)
    keyboard.row(
        InlineKeyboardButton(text='<<', callback_data=f'rmndrsbacknew-{prev_month}-{prev_year}'),
        InlineKeyboardButton(text='>>', callback_data=f'rmndrsnextnew+{next_month}+{next_year}'),
    )
    keyboard.row(InlineKeyboardButton(text='назад', callback_data='reminders'))
    keyboard.row(InlineKeyboardButton(text='🗂', callback_data='start'))

    return keyboard.as_markup()


async def rotation_reminders():
    """Проход по напоминанимя за день."""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text='<<', callback_data='<reminder'),
        InlineKeyboardButton(text='>>', callback_data='>reminder'),
    )
    keyboard.row(
        InlineKeyboardButton(text='🗂', callback_data='start'),
    )

    return keyboard.as_markup()
