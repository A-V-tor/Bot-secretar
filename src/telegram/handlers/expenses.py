from aiogram import Router, types, F
from src.telegram.keyboards.expenses_kb import (
    root_menu_expanses_kb,
    category_expenses_kb,
    yes_or_no_save_expenses_kb,
    expanses_journal_kb,
    category_expenses_last_name_kb,
    yes_or_no_save_last_note_expenses_kb,
)
from src.service.expenses import ExpensesTelegramService
from aiogram.fsm.context import FSMContext
from src.telegram.states import AddExpenses, EditLastNoteExpenses
from src.telegram.keyboards.base_kb import cansel_kb, start_kb
from src.utils.tools import TypeExpenses


router = Router(name='expenses')


@router.callback_query(F.data == 'expense journal')
async def root_expenses_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    msg = 'Журнал ведения расходов'
    await callback.message.answer(
        msg, reply_markup=await root_menu_expanses_kb()
    )


@router.callback_query(F.data == 'show expanses')
async def show_expanses_for_day(callback: types.CallbackQuery):
    await callback.message.delete()

    expenses_service = ExpensesTelegramService(callback)
    my_table, flag_last_note = await expenses_service.get_expenses_for_day()

    await callback.message.answer(
        f'<pre>{my_table}</pre>',
        reply_markup=await expanses_journal_kb(flag_last_note),
        parse_mode='HTML',
    )


@router.callback_query(F.data == 'add expanses')
async def start_add_expenses_in_journal(
    callback: types.CallbackQuery, state: FSMContext
):
    msg = 'Выбери категорию трат'
    await callback.message.delete()
    await state.set_state(AddExpenses.start)
    await callback.message.answer(
        msg, reply_markup=await category_expenses_kb()
    )


@router.callback_query(AddExpenses.start)
async def get_category_for_expenses(
    callback: types.CallbackQuery, state: FSMContext
):
    category = callback.data.split('.')[-1]

    rus_category = getattr(TypeExpenses, category).value
    msg = f'Выбрана категория <b>{rus_category}</b>\nВведи сумму трат.'
    await callback.message.delete()
    await state.set_data({'category': category})
    await state.set_state(AddExpenses.end)
    await callback.message.answer(
        msg, reply_markup=await cansel_kb(), parse_mode='HTML'
    )


@router.message(AddExpenses.end)
async def get_money_for_expenses(message: types.Message, state: FSMContext):
    await message.delete()

    money: str = message.text
    if money.isdigit():
        state_data = await state.get_data()
        category = state_data['category']
        await state.update_data({'money': money})
        rus_category = getattr(TypeExpenses, category).value
        msg = f'Выбрана категория <b>{rus_category}</b>\nСумма трат: <b>{money}</b>\nСохранить?'
        keyboard = await yes_or_no_save_expenses_kb()
    else:
        msg = 'Неверный ввод!'
        keyboard = await cansel_kb()

    await message.answer(msg, reply_markup=keyboard, parse_mode='HTML')


@router.callback_query(F.data == 'yes_expenses')
async def save_expenses(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    state_data = await state.get_data()
    money = int(state_data['money'])
    category = state_data['category']

    expenses_service = ExpensesTelegramService(callback)
    msg = await expenses_service.save_new_expenses(money, category)
    await state.clear()

    await callback.message.answer(msg, reply_markup=await start_kb())


@router.callback_query(F.data == 'edit_last_expenses')
async def edit_last_note(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    expenses_service = ExpensesTelegramService(callback)

    last_note = await expenses_service.get_last_note()
    await state.set_data({'last_note': last_note})
    await state.set_state(EditLastNoteExpenses.category)

    rus_category = last_note.type_expenses.split('.')[-1]
    msg = f'Редактирование записи по категории <b>{rus_category}</b> - сумма: <b>{last_note.value}</b>\n\nОставь или измени категорию'

    await callback.message.answer(
        msg,
        reply_markup=await category_expenses_last_name_kb(),
        parse_mode='HTML',
    )


@router.callback_query(F.data == 'current_last_expenses')
async def edit_last_note_for_current_category(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.message.delete()
    await state.update_data({'category': 'current'})
    msg = 'Введи новое денежное значение для записи'
    await state.set_state(EditLastNoteExpenses.money)

    await callback.message.answer(
        msg, reply_markup=await cansel_kb(), parse_mode='HTML'
    )


@router.callback_query(F.data.startswith('last_'))
async def edit_last_note_for_new_choice_category(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.message.delete()
    category = callback.data.split('_')[1]
    rus_category = getattr(TypeExpenses, category.split('.')[-1]).value
    await state.update_data({'category': category})

    msg = f'Выбрана категория: <b>{rus_category}</b>\n\nВведи новое денежное значение для записи'
    await state.set_state(EditLastNoteExpenses.money)

    await callback.message.answer(
        msg, reply_markup=await cansel_kb(), parse_mode='HTML'
    )


@router.message(EditLastNoteExpenses.money)
async def edit_last_note_set_new_money_value(
    message: types.Message, state: FSMContext
):
    await message.delete()

    money: str = message.text
    if money.isdigit():
        await state.update_data({'money': money})

        msg = f'Сумма трат: <b>{money}</b>\nСохранить?'
        keyboard = await yes_or_no_save_last_note_expenses_kb()

    else:
        msg = 'Неверный ввод!'
        keyboard = await cansel_kb()

    await message.answer(msg, reply_markup=keyboard, parse_mode='HTML')


@router.callback_query(F.data == 'yes_last_expenses')
async def save_changes_last_note(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.message.delete()
    state_data = await state.get_data()

    expenses_service = ExpensesTelegramService(callback)
    note_id = state_data['last_note'].id
    category = state_data.get('category')
    money = state_data.get('money')
    msg = await expenses_service.update_last_note(
        note_id, int(money), category
    )

    await callback.message.answer(msg, reply_markup=await start_kb())
