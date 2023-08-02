from aiogram import types
from .keyboards import WeightInlineKeyboard
from project.database.database import db
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime

from project.database.models import MyWeight
from sqlalchemy import desc


class NewJournalEntries(StatesGroup):
    add_value = State()


class ChangeJournalEntries(StatesGroup):
    change_value = State()


async def weight_journal_root(callback: types.CallbackQuery):
    """Корень журнала веса."""
    kb = WeightInlineKeyboard()
    today = datetime.date.today()
    today_record = db.query(MyWeight).order_by(desc(MyWeight.date)).first()

    # если присутствует запись за сегодня
    if today_record is not None and today_record.date.date() == today:
        msg = f'Вес сегодня ({today}): {str(today_record.value)[:-2]} кг'
        kb.add_button('изменить запись', 'change weight')
    else:
        msg = f'Нет записи на {today}'
        kb.add_button('добавить запись', 'add weight')
    await callback.message.delete()
    await callback.message.answer(msg, reply_markup=kb.keyboard)


async def add_in_weight_journal(callback: types.CallbackQuery):
    """Запуск автомата по добавлению значения веса."""
    await NewJournalEntries.add_value.set()
    await callback.message.reply('Введи текущий вес: ')


async def change_value_weight(callback: types.CallbackQuery):
    """Запуск автомата по добавлению значения веса."""
    await ChangeJournalEntries.change_value.set()
    await callback.message.reply('Введи значение веса: ')


async def add_new_value(message: types.Message, state: NewJournalEntries):
    """Запись веса в бд."""
    # Получаем введенный вес
    value_weight = message.text
    if ',' in value_weight:
        value_weight = value_weight.replace(',', '.')

    await state.finish()

    try:
        if MyWeight.check_note():
            new_note = MyWeight(value=float(value_weight))
            db.add(new_note)
            db.commit()
            msg = f'Текущий вес: {str(new_note.value)[:-2]}  кг'
    except Exception as e:
        # позже записать ошибку в лог-файл
        msg = 'Некорректное значение!'
    await message.reply(msg)


async def change_weight_value(
    message: types.Message, state: ChangeJournalEntries
):
    # Получаем введенный вес
    value_weight = message.text
    if ',' in value_weight:
        value_weight = value_weight.replace(',', '.')

    await state.finish()
    try:

        today_record = db.query(MyWeight).order_by(desc(MyWeight.date)).first()
        today_record.value = float(value_weight)
        today_record.date = datetime.datetime.now()
        db.commit()
        msg = f'{str(today_record.value)[:-2]} кг'
    except Exception as e:
        # позже записать ошибку в лог-файл
        msg = 'Некорректное значение!'
    await message.reply(msg)
