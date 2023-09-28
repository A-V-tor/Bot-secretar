import logging
from aiogram import types
from .keyboards import ExpenseInlineKeyboard
from prettytable import PrettyTable
from project.database.database import db
from project.telegram.utils import get_russian_category_name, get_non_zero_keys
from aiogram.dispatcher.filters.state import State, StatesGroup
from project.database.models import MyExpenses
from sqlalchemy import extract, func
import datetime


SELECT_CATEGORY = None
CHANGE_CATEGORY = None


logger = logging.getLogger(__name__)


class NewRecordExpense(StatesGroup):
    add_record = State()


class ChangeRecordExpense(StatesGroup):
    change_record = State()


async def expencse_journal_root(callback: types.CallbackQuery):
    kb = ExpenseInlineKeyboard()
    kb.button_start_menu()
    kb.add_button('журнал', 'get current table')
    kb.add_button('новая запись', 'add  expense')
    kb.add_button('изменить значение', 'change expence')
    await callback.message.delete()
    await callback.message.answer('Журнал расходов', reply_markup=kb.keyboard)


async def get_expenses_for_day(callback: types.CallbackQuery):
    today = datetime.date.today()
    year, month, day = str(today).split('-')

    kb = ExpenseInlineKeyboard()
    kb.button_start_menu()
    kb.button_root_expense()

    await callback.message.delete()

    try:
        query_ = (
            db.query(
                func.sum(MyExpenses.health).label('total_health'),
                func.sum(MyExpenses.transport).label('total_transport'),
                func.sum(MyExpenses.food).label('total_food'),
                func.sum(MyExpenses.entertainment).label(
                    'total_entertainment'
                ),
                func.sum(MyExpenses.purchases).label('total_purchases'),
                func.sum(MyExpenses.present).label('total_present'),
                func.sum(MyExpenses.other).label('total_other'),
            )
            .filter(
                extract('year', MyExpenses.date) == year,
                extract('month', MyExpenses.date) == month,
                extract('day', MyExpenses.date) == day,
            )
            .first()
        )

        # общее число потраченых едениц
        total = sum(query_)

        mytable = PrettyTable()
        mytable.field_names = ['Категория', 'Рублей']
        mytable.add_row(['Транспорт', query_.total_transport])
        mytable.add_row(['Развлечения', query_.total_entertainment])
        mytable.add_row(['Здоровье', query_.total_health])
        mytable.add_row(['Покупки', query_.total_purchases])
        mytable.add_row(['Подарки', query_.total_present])
        mytable.add_row(['Еда', query_.total_food])
        mytable.add_row(['Прочее', query_.total_other])
        mytable.add_row(['---------', '------'])
        mytable.add_row(['Всего', total])

        msg = mytable
    except TypeError as e:
        logger.exception(f'Ошибка- журнал пуст: {str(e)}')
        msg = 'Журнал пуст!'
    except Exception as e:
        logger.exception(f'Ошибка: {str(e)}')
        msg = 'Что-то пошло не так'

    await callback.message.answer(
        f'<pre>{msg}</pre>', parse_mode='HTML', reply_markup=kb.keyboard
    )


async def add_expenses_in_journal(callback: types.CallbackQuery):
    kb = ExpenseInlineKeyboard()
    kb.expense_category_buttons()
    kb.button_start_menu()
    kb.button_root_expense()
    msg = 'Выбери категорию трат'
    await callback.message.delete()
    await callback.message.answer(msg, reply_markup=kb.keyboard)


async def parse_categories_for_expenses(callback: types.CallbackQuery):
    global SELECT_CATEGORY
    _, category = callback.data.split(' ')
    SELECT_CATEGORY = category
    category = get_russian_category_name(category)
    await NewRecordExpense.add_record.set()
    msg = f'Выбрана категория: {category}\nВведи сумму: '
    kb = ExpenseInlineKeyboard()
    kb.button_start_menu()
    kb.button_root_expense()
    kb.button_cancel()
    await callback.message.delete()
    await callback.message.answer(msg, reply_markup=kb.keyboard)


async def write_to_database_new_expense(
    message: types.Message, state: NewRecordExpense
):
    global SELECT_CATEGORY
    value = message.text
    await state.finish()

    # удаление предыдущего сообщения
    message.message_id -= 1
    await message.delete()

    try:
        new_record = MyExpenses()
        setattr(new_record, SELECT_CATEGORY, int(value))
        db.add(new_record)
        db.commit()
        msg = 'Запись сделана!'
    except ValueError as e:
        db.rollback()
        logger.exception(f'Ошибка значения: {str(e)}')
        msg = 'Ошибка\n Значение должно быть числом!'
    except Exception as e:
        db.rollback()
        logger.exception(f'Ошибка значения: {str(e)}')
        msg = 'Ошибка\n Что то случилось и все сломалось'

    SELECT_CATEGORY = None
    kb = ExpenseInlineKeyboard()
    kb.button_start_menu()
    kb.button_root_expense()

    await message.answer(msg, reply_markup=kb.keyboard)


async def change_last_record(callback: types.CallbackQuery):
    global CHANGE_CATEGORY
    kb = ExpenseInlineKeyboard()
    kb.button_cancel()
    kb.button_start_menu()
    kb.button_root_expense()

    note = db.query(MyExpenses).first()
    category = get_non_zero_keys(vars(note))
    CHANGE_CATEGORY = category
    category = get_russian_category_name(category)
    msg = f'Введи значение для последней записи категории: {category}'

    await callback.message.delete()
    await ChangeRecordExpense.change_record.set()
    await callback.message.answer(msg, reply_markup=kb.keyboard)


async def write_to_database_change_expense(
    message: types.Message, state: ChangeRecordExpense
):
    global CHANGE_CATEGORY
    value = message.text
    await state.finish()

    # удаление предыдущего сообщения
    message.message_id -= 1
    await message.delete()

    kb = ExpenseInlineKeyboard()
    kb.button_start_menu()
    kb.button_root_expense()

    note = db.query(MyExpenses).first()
    try:
        setattr(note, CHANGE_CATEGORY, int(value))
        db.add(note)
        db.commit()
        msg = 'Запись сделана!'
    except ValueError as e:
        db.rollback()
        logger.exception(f'Ошибка значения: {str(e)}')
        msg = 'Ошибка\n Значение должно быть числом!'
    except Exception as e:
        db.rollback()
        logger.exception(f'Ошибка значения: {str(e)}')
        msg = 'Ошибка\n Что то случилось и все сломалось'

    CHANGE_CATEGORY = None

    await message.answer(msg, reply_markup=kb.keyboard)
