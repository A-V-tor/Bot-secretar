import datetime
from collections import deque

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.services.workouts import WorkoutTelegramService
from src.telegram.states import DayWorkouts

from ..keyboards.base_kb import cansel_kb
from ..keyboards.workout_kb import (
    render_workout_calendar,
    root_menu_workout_kb,
    rotation_workout,
)

router = Router(name='workout')


@router.callback_query(F.data == 'workout journal')
async def root_workout_menu(callback: types.CallbackQuery):
    await callback.message.delete()

    msg = 'Журнал ведения тренировок'
    await callback.message.answer(msg, reply_markup=await root_menu_workout_kb())


@router.callback_query(F.data == 'add workout')
async def add_workout_in_journal(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(DayWorkouts.save_workout)

    await callback.message.delete()
    await callback.message.answer('Запиши тренировку: ', reply_markup=await cansel_kb())


@router.message(DayWorkouts.save_workout)
async def save_new_workout(message: types.Message, state: FSMContext):
    await message.bot.delete_message(message.chat.id, message.message_id - 1)

    text_workout = message.text
    workout_service = WorkoutTelegramService(message)

    msg = await workout_service.save_workout(text_workout)
    await state.clear()

    await message.answer(msg, reply_markup=await root_menu_workout_kb())


@router.callback_query(F.data == 'show workout')
async def get_workout_journal(callback: types.CallbackQuery):
    """Календарь текущего месяца."""
    today = datetime.date.today()
    year, month = today.year, today.month
    await callback.message.delete()

    workout_service = WorkoutTelegramService(callback)
    (
        workout_days,
        msg,
    ) = await workout_service.get_workout_days_for_current_month(month, year)

    await callback.message.answer(
        msg,
        reply_markup=await render_workout_calendar(month, year, workout_days),
    )


@router.callback_query(F.data.startswith('-'))
async def previous_month_of_workout(callback: types.CallbackQuery):
    """Назад по календарю."""
    month, year = callback.data[1:].split(' ')
    month, year = int(month), int(year)
    await callback.message.delete()

    workout_service = WorkoutTelegramService(callback)
    (
        workout_days,
        msg,
    ) = await workout_service.get_workout_days_for_current_month(month, year)

    await callback.message.answer(
        msg,
        reply_markup=await render_workout_calendar(month, year, workout_days),
    )


@router.callback_query(F.data.startswith('+'))
async def next_month_of_workout(callback: types.CallbackQuery):
    """Вперед по календарю."""
    month, year = callback.data[1:].split(' ')
    month, year = int(month), int(year)
    await callback.message.delete()

    workout_service = WorkoutTelegramService(callback)
    (
        workout_days,
        msg,
    ) = await workout_service.get_workout_days_for_current_month(month, year)

    await callback.message.answer(
        msg,
        reply_markup=await render_workout_calendar(month, year, workout_days),
    )


@router.callback_query(F.data.startswith('_'))
async def get_workout_for_day(callback: types.CallbackQuery, state: FSMContext):
    """Записи текущего дня."""
    day, month, year = callback.data[1:].split('-')
    day, month, year = int(day), int(month), int(year)
    await callback.message.delete()

    workout_service = WorkoutTelegramService(callback)
    workouts_current_day, msg = await workout_service.get_workouts_current_day(day, month, year)

    await state.set_state(DayWorkouts.save_workout)
    await state.set_data({'workouts': deque(workouts_current_day)})

    keyboard = await rotation_workout() if workouts_current_day else await root_menu_workout_kb()

    await callback.message.answer(msg, reply_markup=keyboard, parse_mode='HTML')


@router.callback_query(F.data.startswith('&'))
async def rotation_list_current_workouts(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    _, move = callback.data.split(' ')
    await callback.message.delete()

    workout_service = WorkoutTelegramService(callback)
    current_workouts, msg = await workout_service.show_workout(move, data)
    await state.set_data({'workouts': current_workouts})

    await callback.message.answer(msg, reply_markup=await rotation_workout(), parse_mode='HTML')


@router.callback_query(F.data == 'del workout')
async def delete_current_record(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.delete()

    workout_service = WorkoutTelegramService(callback)
    current_workouts, msg = await workout_service.delete_note(data)

    if len(current_workouts) == 0:
        # нет записей для отображения/удаления
        msg += 'Не записй на текущий день!'
        await callback.message.answer(msg, reply_markup=await root_menu_workout_kb(), parse_mode='HTML')
        return

    current_workouts, msg_ = await workout_service.show_workout('forward', {'workouts': current_workouts})
    await state.set_data({'workouts': current_workouts})

    await callback.message.answer(msg + msg_, reply_markup=await rotation_workout(), parse_mode='HTML')
