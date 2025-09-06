from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.services.weight import WeightTelegramService
from src.telegram.keyboards.base_kb import cansel_kb, start_kb
from src.telegram.keyboards.weight_kb import (
    root_menu_weight_kb,
    yes_or_no_save_change_weight_kb,
    yes_or_no_save_weight_kb,
)
from src.telegram.states import ChangeValueWeight, NewValueWeight
from src.utils.tools import validate_weight

router = Router(name='weight')


@router.callback_query(F.data == 'weight journal')
async def root_weight_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()

    weight_manager = WeightTelegramService(callback)
    result = await weight_manager.check_note()
    presence_of_record = True if result else False
    msg = f'Твой вес сегодня: <b>{result.value}</b>' if result else 'Журнал веса на сегодня пуст'

    if presence_of_record:
        await state.set_data({'weight_note_id': result.id})

    await callback.message.answer(
        msg,
        reply_markup=await root_menu_weight_kb(presence_of_record),
        parse_mode='HTML',
    )


@router.callback_query(F.data == 'add weight')
async def new_note(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    msg = 'Введи значение веса'
    await state.set_state(NewValueWeight.start)

    await callback.message.answer(msg, reply_markup=await cansel_kb())


@router.message(NewValueWeight.start)
async def get_value_weight(message: types.Message, state: FSMContext):
    del_msg: int = message.message_id - 1
    await message.bot.delete_message(message.chat.id, del_msg)
    await message.delete()

    weight: str = message.text
    check_weight = await validate_weight(weight)
    if check_weight:
        msg = f'Вес сегодня: <b>{weight}</b>'
        keyboard = await yes_or_no_save_weight_kb()
        await state.set_data({'weight': check_weight})
    else:
        msg = 'Неверный ввод!'
        keyboard = await cansel_kb()

    await message.answer(msg, reply_markup=keyboard, parse_mode='HTML')


@router.callback_query(F.data == 'yes_weight')
async def save_weight(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    state_data = await state.get_data()
    weight = float(state_data['weight'])

    weight_manager = WeightTelegramService(callback)
    msg = await weight_manager.save_weight(weight)

    await callback.message.answer(msg, reply_markup=await start_kb())


@router.callback_query(F.data == 'change weight')
async def change_note(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    msg = 'Введи значение веса'
    await state.set_state(ChangeValueWeight.start)

    await callback.message.answer(msg, reply_markup=await cansel_kb())


@router.message(ChangeValueWeight.start)
async def get_change_value_weight(message: types.Message, state: FSMContext):
    await message.delete()

    weight: str = message.text
    check_weight = await validate_weight(weight)

    if check_weight:
        msg = f'Изменить вес на: <b>{weight}</b> ?'
        keyboard = await yes_or_no_save_change_weight_kb()
        await state.update_data({'weight': check_weight})
    else:
        msg = 'Неверный ввод!'
        keyboard = await cansel_kb()

    await message.answer(msg, reply_markup=keyboard, parse_mode='HTML')


@router.callback_query(F.data == 'yes_change_weight')
async def save_change_weight(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    state_data = await state.get_data()
    weight = float(state_data['weight'])

    state_data = await state.get_data()
    note_id = state_data['weight_note_id']

    weight_manager = WeightTelegramService(callback)
    msg = await weight_manager.save_change_weight(note_id, weight)

    await callback.message.answer(msg, reply_markup=await start_kb())
