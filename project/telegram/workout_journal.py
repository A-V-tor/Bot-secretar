from aiogram import types
import logging
from .keyboards import WorkoutInlineKeyboard
from .utils import (
    get_current_month_and_year,
    get_workout_days,
    get_msg_for_records_workout,
)
from project.database.database import db
from aiogram.dispatcher.filters.state import State, StatesGroup
from project.database.models import MyWorkout
from sqlalchemy import extract
import datetime
import calendar
from collections import deque


logger = logging.getLogger(__name__)


LIST_RECORDS_FOR_THE_DAY = deque()
DEL_RECORD = None


class NewRecordWorkout(StatesGroup):
    add_record = State()


async def workout_journal_root(callback: types.CallbackQuery):
    """Корень журнала тренировок."""
    kb = WorkoutInlineKeyboard()
    kb.button_start_menu()
    kb.add_button('журнал', 'show workout')
    kb.add_button('добавить', 'add workout')
    msg = 'Меню'
    await callback.message.delete()
    await callback.message.answer(msg, reply_markup=kb.keyboard)


async def get_workout_journal(callback: types.CallbackQuery):
    """Календарь текущего месяца."""
    today = datetime.date.today()
    year, month, day = str(today).split('-')
    await show_calendar(callback, int(year), int(month), day)


async def previous_month_of_workout(callback: types.CallbackQuery):
    """Назад по календарю."""
    month, year = callback.data[1:].split(' ')
    month, year = get_current_month_and_year(month, year, 'back')
    await callback.message.delete()
    await show_calendar(callback, int(year), int(month))


async def next_month_of_workout(callback: types.CallbackQuery):
    """Вперед по календарю."""
    month, year = callback.data[1:].split(' ')
    month, year = get_current_month_and_year(month, year, 'next')
    await callback.message.delete()
    await show_calendar(callback, int(year), int(month))


async def show_calendar(callback, year, month, selected_day=None):
    """Отображени календаря с записями тренировок."""
    cl = calendar.TextCalendar(firstweekday=0)

    # формирование календаря текущего месяца
    kb = WorkoutInlineKeyboard()
    kb.make_row_width(7)
    kb.insert_button('Пн', '_')
    kb.insert_button('Вт', '_')
    kb.insert_button('Ср', '_')
    kb.insert_button('Чт', '_')
    kb.insert_button('Пт', '_')
    kb.insert_button('Сб', '_')
    kb.insert_button('Вс', '_')

    days_current_month = [i for i in cl.itermonthdays(year, month)]

    workout_notes = (
        db.query(MyWorkout)
        .filter(
            extract('year', MyWorkout.date) == year,
            extract('month', MyWorkout.date) == month,
        )
        .all()
    )

    # дни тренировок
    workout_days = get_workout_days(workout_notes)

    for value in days_current_month:
        if value != 0:
            # если есть тренировка
            if str(value) in workout_days:
                kb.insert_button('💪', f'_{value}-{month}-{year}')
            else:
                kb.insert_button(f'{value}', f'_{value}-{month}-{year}')
        else:
            kb.insert_button(' ', '_')

    kb.get_buttons_cl(month, year)

    month_string = datetime.datetime(year, month, 1).strftime('%B')

    msg = (
        f'{selected_day} {month_string} {year} года'
        if selected_day
        else f'С 1 {month_string} {year} года'
    )
    kb.button_start_menu()
    kb.add_button('<<', 'workout journal')
    await callback.message.delete() if selected_day else None
    await callback.message.answer(msg, reply_markup=kb.keyboard)


async def get_workout_for_day(callback: types.CallbackQuery):
    """Записи текущего дня."""
    day, month, year = callback.data[1:].split('-')

    global LIST_RECORDS_FOR_THE_DAY
    global DEL_RECORD
    LIST_RECORDS_FOR_THE_DAY.clear()

    await callback.message.delete()

    workout_notes = (
        db.query(MyWorkout)
        .filter(
            extract('year', MyWorkout.date) == year,
            extract('month', MyWorkout.date) == month,
            extract('day', MyWorkout.date) == day,
        )
        .all()
    )
    if not workout_notes:
        await callback.message.answer('Нет записей!')
        return

    for i, value in enumerate(workout_notes):
        # нумерация с 1
        i += 1
        LIST_RECORDS_FOR_THE_DAY.append({i: value})
    #  получение записи и ее порядкового номера
    [record_db] = LIST_RECORDS_FOR_THE_DAY[0].values()
    text_record = record_db.value.replace('\r\n', '\n')
    [record_number] = LIST_RECORDS_FOR_THE_DAY[0].keys()
    records_amount = len(workout_notes)
    DEL_RECORD = record_db

    msg = get_msg_for_records_workout(
        record_number, records_amount, text_record
    )

    kb = WorkoutInlineKeyboard()
    kb.button_start_menu()
    kb.button_delete_record()
    if records_amount > 1:
        kb.get_buttons_next_or_back_record()
    await callback.message.answer(msg, reply_markup=kb.keyboard)


async def delete_current_record(callback: types.CallbackQuery):
    """Удаление записи тренировки."""
    global DEL_RECORD
    global LIST_RECORDS_FOR_THE_DAY
    # удаляем из бд
    db.delete(DEL_RECORD)
    db.commit()

    # удаляем из дневного списка
    for i in LIST_RECORDS_FOR_THE_DAY:
        [cur] = i.values()
        if cur == DEL_RECORD:
            LIST_RECORDS_FOR_THE_DAY.remove(i)
            break

    DEL_RECORD = None

    kb = WorkoutInlineKeyboard()
    kb.button_start_menu()

    # если запись не единственая
    if LIST_RECORDS_FOR_THE_DAY:
        LIST_RECORDS_FOR_THE_DAY.rotate(1)
        [record_db] = LIST_RECORDS_FOR_THE_DAY[0].values()
        text_record = record_db.value.replace('\r\n', '\n')
        [record_number] = LIST_RECORDS_FOR_THE_DAY[0].keys()
        records_amount = len(LIST_RECORDS_FOR_THE_DAY)
        DEL_RECORD = record_db
        msg = get_msg_for_records_workout(
            record_number, records_amount, text_record
        )
        kb.button_delete_record()
        kb.get_buttons_next_or_back_record()
    else:
        msg = 'Нет записей'
        LIST_RECORDS_FOR_THE_DAY = None
        DEL_RECORD = None

    await callback.message.delete()
    await callback.message.answer(msg, reply_markup=kb.keyboard)


async def get_workout_record_next_or_back(callback: types.CallbackQuery):
    """Вперед/назад по записям текущего дня."""
    global DEL_RECORD
    global LIST_RECORDS_FOR_THE_DAY

    _, move, __ = callback.data.split(' ')
    if move == 'next':
        LIST_RECORDS_FOR_THE_DAY.rotate(1)
    else:
        LIST_RECORDS_FOR_THE_DAY.rotate(-1)

    [record_db] = LIST_RECORDS_FOR_THE_DAY[0].values()
    text_record = record_db.value.replace('\r\n', '\n')
    [record_number] = LIST_RECORDS_FOR_THE_DAY[0].keys()
    records_amount = len(LIST_RECORDS_FOR_THE_DAY)

    DEL_RECORD = record_db

    msg = get_msg_for_records_workout(
        record_number, records_amount, text_record
    )

    kb = WorkoutInlineKeyboard()
    kb.button_start_menu()
    kb.button_delete_record()
    if records_amount > 1:
        kb.get_buttons_next_or_back_record()

    await callback.message.delete()
    await callback.message.answer(msg, reply_markup=kb.keyboard)


async def add_workout_in_journal(callback: types.CallbackQuery):
    kb = WorkoutInlineKeyboard()
    kb.button_start_menu()
    kb.button_cancel()
    await NewRecordWorkout.add_record.set()
    await callback.message.delete()
    await callback.message.answer(
        'Запиши тренировку: ', reply_markup=kb.keyboard
    )


async def write_to_database_new_value_workout(
    message: types.Message, state: NewRecordWorkout
):
    # Получаем текст записи
    text_record = message.text
    await state.finish()

    # удаление предыдущего сообщения
    message.message_id -= 1
    await message.delete()

    try:
        new_note = MyWorkout(value=text_record)
        db.add(new_note)
        db.commit()
        msg = 'Тренировка добавлена'
    except ValueError as e:
        logger.exception(f'Ошибка значения: {str(e)}')
        msg = 'Ошибка\n Значение должно быть числом!'

    await message.answer(msg)
