import logging
from aiogram import types
from .keyboards import WeightInlineKeyboard
from project.database.database import db
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime

from project.database.models import MyWeight
from sqlalchemy import desc


logger = logging.getLogger(__name__)


class NewJournalEntries(StatesGroup):
    add_value = State()


class ChangeJournalEntries(StatesGroup):
    change_value = State()
    cancel = State()


async def weight_journal_root(callback: types.CallbackQuery):
    """Корень журнала веса."""
    kb = WeightInlineKeyboard()
    today = datetime.date.today()
    today_record = db.query(MyWeight).order_by(desc(MyWeight.date)).first()

    # если присутствует запись за сегодня
    if today_record is not None and today_record.date.date() == today:
        msg = f'Вес сегодня ({today}): {str(today_record.value)[:-2]} кг'
        kb.add_button('изменить запись', 'change weight')
        kb.button_start_menu()
    else:
        msg = f'Нет записи на {today}'
        kb.add_button('добавить запись', 'add weight')
        kb.button_start_menu()
    await callback.message.delete()
    await callback.message.answer(msg, reply_markup=kb.keyboard)


async def add_in_weight_journal(callback: types.CallbackQuery):
    """Запуск автомата по добавлению значения веса."""
    kb = WeightInlineKeyboard()
    kb.add_button('отмена', 'cancel')
    await NewJournalEntries.add_value.set()
    await callback.message.delete()
    await callback.message.answer(
        'Введи текущий вес: ', reply_markup=kb.keyboard
    )
    await callback.message.delete()


async def change_value_weight(callback: types.CallbackQuery):
    """Запуск автомата по добавлению значения веса."""
    kb = WeightInlineKeyboard()
    kb.add_button('отмена', 'cancel')
    await ChangeJournalEntries.change_value.set()
    await callback.message.delete()
    await callback.message.answer(
        'Введи значение веса: ', reply_markup=kb.keyboard
    )


async def write_to_database_new_value_weight(
    message: types.Message, state: NewJournalEntries
):
    """Запись веса в бд."""
    # Получаем введенный вес
    value_weight = message.text
    if ',' in value_weight:
        value_weight = value_weight.replace(',', '.')

    await state.finish()
    kb = WeightInlineKeyboard()
    kb.button_start_menu()

    # удаление предыдущего сообщения
    message.message_id -= 1
    await message.delete()

    try:
        if MyWeight():
            new_note = MyWeight(value=float(value_weight))
            db.add(new_note)
            db.commit()
            msg = f'Текущий вес: {str(new_note.value)[:-2]}  кг'
    except ValueError as e:
        db.rollback()
        logger.exception(f'Ошибка значения: {str(e)}')
        msg = 'Ошибка\n Значение должно быть числом!'
    except Exception as e:
        db.rollback()
        logger.exception(f'Ошибка значения: {str(e)}')
        msg = 'Ошибка\n Что то случилось и все сломалось'

    await message.answer(msg, reply_markup=kb.keyboard)


async def change_weight_value(
    message: types.Message, state: ChangeJournalEntries
):
    # Получаем введенный вес
    value_weight = message.text
    if ',' in value_weight:
        value_weight = value_weight.replace(',', '.')

    await state.finish()
    kb = WeightInlineKeyboard()
    kb.button_start_menu()

    # удаление предыдущего сообщения
    message.message_id -= 1
    await message.delete()

    try:
        today_record = db.query(MyWeight).order_by(desc(MyWeight.date)).first()
        today_record.value = float(value_weight)
        today_record.date = datetime.datetime.now()
        db.commit()
        msg = f'{str(today_record.value)[:-2]} кг'
    except ValueError as e:
        db.rollback()
        logger.exception(f'Ошибка записи значения: {str(e)}')
        msg = 'Ошибка\n Значение должно быть числом!'
    except Exception as e:
        db.rollback()
        logger.exception(f'Ошибка значения: {str(e)}')
        msg = 'Ошибка\n Что то случилось и все сломалось'

    await message.answer(msg, reply_markup=kb.keyboard)
