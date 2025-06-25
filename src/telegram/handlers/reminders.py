import datetime
from collections import deque

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.services.reminders import RemindersTelegramService
from src.telegram.states import AddReminder
from src.utils.tools import ReminderLevel

from ..keyboards.base_kb import cansel_kb, start_kb
from ..keyboards.reminders import (
    reminders_kb,
    render_reminders_calendar,
    render_reminders_calendar_for_input,
    rotation_reminders,
    select_hour_timestamp,
    select_minutes_timestamp,
)

router = Router(name='reminders')


@router.callback_query(F.data == 'reminders')
async def menu_reminders(callback: types.CallbackQuery):
    await callback.message.delete()

    msg = 'Меню напоминаний'

    await callback.message.answer(msg, reply_markup=await reminders_kb())


@router.callback_query(F.data == 'show-reminders')
async def get_reminders_journal(callback: types.CallbackQuery):
    """Календарь текущего месяца."""
    today = datetime.date.today()
    year, month = today.year, today.month
    await callback.message.delete()

    reminder_service = RemindersTelegramService(callback)
    (
        reminder_days,
        msg,
    ) = await reminder_service.get_reminders_days_for_current_month(month, year)

    await callback.message.answer(
        msg,
        reply_markup=await render_reminders_calendar(month, year, reminder_days),
    )


@router.callback_query(F.data.startswith('rmndrs-'))
async def previous_month_of_reminders(callback: types.CallbackQuery):
    """Назад по календарю."""
    month, year = callback.data[7:].split(' ')
    month, year = int(month), int(year)
    await callback.message.delete()

    reminder_service = RemindersTelegramService(callback)
    (
        reminder_days,
        msg,
    ) = await reminder_service.get_reminders_days_for_current_month(month, year)

    await callback.message.answer(
        msg,
        reply_markup=await render_reminders_calendar(month, year, reminder_days),
    )


@router.callback_query(F.data.startswith('rmndrs+'))
async def next_month_of_reminders(callback: types.CallbackQuery):
    """Вперед по календарю."""
    month, year = callback.data[7:].split(' ')
    month, year = int(month), int(year)
    await callback.message.delete()

    reminder_service = RemindersTelegramService(callback)
    (
        reminder_days,
        msg,
    ) = await reminder_service.get_reminders_days_for_current_month(month, year)

    await callback.message.answer(
        msg,
        reply_markup=await render_reminders_calendar(month, year, reminder_days),
    )


@router.callback_query(F.data == 'reminder-add')
async def add_reminder(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddReminder.start_save_reminder)

    await callback.message.delete()
    await callback.message.answer('Введи тест напоминания: ', reply_markup=await cansel_kb())


@router.message(AddReminder.start_save_reminder)
async def get_hour_for_reminder(message: types.Message, state: FSMContext):
    await message.bot.delete_message(message.chat.id, message.message_id - 1)

    text_reminder: str | None = message.text
    if text_reminder:
        msg = 'Выбери час напоминания'
        await state.set_state(AddReminder.add_timestamp)
        await state.set_data({'text_reminder': text_reminder})
        keyboard = await select_hour_timestamp()
    else:
        msg = 'Нужен текст напоминания'
        keyboard = await cansel_kb()

    await message.answer(msg, reply_markup=keyboard, parse_mode='HTML')


@router.callback_query(F.data.startswith('rmndr-hour'))
async def get_minutes_for_reminder(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    hour = callback.data.split('-')[-1]
    await state.update_data({'hour': hour})

    keyboard = await select_minutes_timestamp()
    await callback.message.answer('Выбери минуты напоминания', reply_markup=keyboard, parse_mode='HTML')


@router.callback_query(F.data.startswith('rmndr-minutes'))
async def get_date_for_reminder(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    minutes = callback.data.split('-')[-1]
    await state.update_data({'minutes': minutes})

    today = datetime.date.today()
    year, month = today.year, today.month

    msg = 'Выбери дату'
    keyboard = await render_reminders_calendar_for_input(month, year)
    await callback.message.answer(msg, reply_markup=keyboard, parse_mode='HTML')


@router.callback_query(F.data.startswith('rmndrsnew'))
async def set_data_for_reminder(callback: types.CallbackQuery, state: FSMContext):
    """Создание/сохранение напоминания."""
    await callback.message.delete()
    month, day, year = callback.data.split('-')[1:]

    data = await state.get_data()
    value = data['text_reminder']
    hour = data['hour']
    minutes = data['minutes']
    timestamp = f'{month}.{day}.{year} {hour}:{minutes}'

    reminder_service = RemindersTelegramService(callback)
    msg = await reminder_service.new_reminder(value, ReminderLevel.important, timestamp)

    await callback.message.answer(msg, reply_markup=await start_kb(), parse_mode='HTML')


@router.callback_query(F.data.startswith('rmndrsbacknew-'))
async def previous_month_of_new_reminder(callback: types.CallbackQuery):
    """Назад по календарю - выбор даты новой записи."""
    await callback.message.delete()

    _, month, year = callback.data.split('-')
    month, year = int(month), int(year)

    month_string = datetime.datetime(year, month, 1).strftime('%B')
    msg = f'С 1 {month_string} {year} года'

    await callback.message.answer(
        msg,
        reply_markup=await render_reminders_calendar_for_input(month, year),
    )


@router.callback_query(F.data.startswith('rmndrsnextnew+'))
async def next_month_of_new_reminder(callback: types.CallbackQuery):
    """Вперед по календарю - выбор даты новой записи."""
    await callback.message.delete()

    _, month, year = callback.data.split('+')
    month, year = int(month), int(year)

    month_string = datetime.datetime(year, month, 1).strftime('%B')
    msg = f'С 1 {month_string} {year} года'

    await callback.message.answer(
        msg,
        reply_markup=await render_reminders_calendar_for_input(month, year),
    )


@router.callback_query(F.data.startswith('rmndrs_show-'))
async def show_reminders_for_current_day(callback: types.CallbackQuery, state: FSMContext):
    """Показать напоминания на текущий день."""
    await callback.message.delete()
    _, day, month, year = callback.data.split('-')

    reminder_service = RemindersTelegramService(callback)
    notes = await reminder_service.get_note_by_date(callback.from_user.id, int(day), int(month), int(year))
    msg = f'{day.zfill(2)}-{month.zfill(2)}-{year}\n' + str(notes[0].value) if notes else 'Нет напоминаний'
    notes = notes if notes else []
    await state.set_data({'remiinders_to_day': notes, 'timestamp_reminder': f'{day}-{month}-{year}'})
    await callback.message.answer(
        str(msg),
        reply_markup=await rotation_reminders(),
    )


@router.callback_query(F.data.startswith('>reminder'))
async def show_next_reminders_for_current_day(callback: types.CallbackQuery, state: FSMContext):
    """Вперед по списку напоминаний за текущий день."""
    await callback.message.delete()
    data = await state.get_data()
    day, month, year = data['timestamp_reminder'].split('-')

    notes = data['remiinders_to_day']
    notes = deque(notes)
    notes.rotate(-1)

    msg = f'{day.zfill(2)}-{month.zfill(2)}-{year}\n' + str(notes[0].value) if notes else 'Нет напоминаний'
    notes = notes if notes else []
    await state.set_data({'remiinders_to_day': notes, 'timestamp_reminder': f'{day}-{month}-{year}'})
    await callback.message.answer(
        str(msg),
        reply_markup=await rotation_reminders(),
    )


@router.callback_query(F.data.startswith('<reminder'))
async def show_back_reminders_for_current_day(callback: types.CallbackQuery, state: FSMContext):
    """Назад по списку напоминаний за текущий день."""
    await callback.message.delete()
    data = await state.get_data()
    day, month, year = data['timestamp_reminder'].split('-')

    notes = data['remiinders_to_day']
    notes = deque(notes)
    notes.rotate(1)

    msg = f'{day.zfill(2)}-{month.zfill(2)}-{year}\n' + str(notes[0].value) if notes else 'Нет напоминаний'
    notes = notes if notes else []
    await state.set_data({'remiinders_to_day': notes, 'timestamp_reminder': f'{day}-{month}-{year}'})
    await callback.message.answer(
        str(msg),
        reply_markup=await rotation_reminders(),
    )
