import calendar

from aiogram.types import (
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils.tools import get_next_month_and_year, get_prev_month_and_year


async def root_menu_workout_kb():
    keyboard = InlineKeyboardBuilder()

    root_menu = InlineKeyboardButton(text='🗂', callback_data='start')
    journal = InlineKeyboardButton(text='журнал', callback_data='show workout')
    new_note = InlineKeyboardButton(text='добавить', callback_data='add workout')

    keyboard.row(root_menu).row(journal).row(new_note)

    return keyboard.as_markup()


async def rotation_workout():
    keyboard = InlineKeyboardBuilder()

    prev = InlineKeyboardButton(text='<<<', callback_data='& back')
    forward = InlineKeyboardButton(text='>>>', callback_data='& forward')
    back = InlineKeyboardButton(text='назад', callback_data='show workout')
    delete_note = InlineKeyboardButton(text='удалить', callback_data='del workout')
    root_menu = InlineKeyboardButton(text='🗂', callback_data='start')

    keyboard.row(prev, forward).row(delete_note).row(back).row(root_menu)

    return keyboard.as_markup()


async def render_workout_calendar(month: int, year: int, workout_days: list):
    """Отрисовка календаря тренировок в клавиатуре."""
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
            if str(day) in workout_days:
                # если есть тренировка
                workout_button = InlineKeyboardButton(text='💪', callback_data=f'_{day}-{month}-{year}')
                if count_days % 7 == 0:
                    keyboard.row(workout_button)
                else:
                    keyboard.add(workout_button)
            else:
                not_workout_button = InlineKeyboardButton(text=f' {day} ', callback_data=f'_{day}-{month}-{year}')
                if count_days % 7 == 0:
                    keyboard.row(not_workout_button)
                else:
                    keyboard.add(not_workout_button)
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
        InlineKeyboardButton(text='<<', callback_data=f'-{prev_month} {prev_year}'),
        InlineKeyboardButton(text='>>', callback_data=f'+{next_month} {next_year}'),
    )
    keyboard.row(InlineKeyboardButton(text='назад', callback_data='workout journal'))
    keyboard.row(InlineKeyboardButton(text='🗂', callback_data='start'))

    return keyboard.as_markup()
