import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv
from .keyboards import StartInlineKeyboard
from .weight_journal import (
    weight_journal_root,
    add_in_weight_journal,
    write_to_database_new_value_weight,
    change_value_weight,
    change_weight_value,
    NewJournalEntries,
    ChangeJournalEntries,
)
from .workout_journal import (
    workout_journal_root,
    get_workout_journal,
    previous_month_of_workout,
    next_month_of_workout,
    get_workout_for_day,
    delete_current_record,
    get_workout_record_next_or_back,
    add_workout_in_journal,
    write_to_database_new_value_workout,
    NewRecordWorkout,
)
from .expense_journal import (
    expencse_journal_root,
    get_expenses_for_day,
    add_expenses_in_journal,
    parse_categories_for_expenses,
    NewRecordExpense,
    ChangeRecordExpense,
    write_to_database_new_expense,
    change_last_record,
    write_to_database_change_expense,
)
from .middlewares import AccessMiddleware
import locale

from .logger import get_loggs

# установка родной локали, чтобы название месяца Python стал выводить кириллицей
locale.setlocale(locale.LC_ALL)   # 'ru_RU' сервак слетает

load_dotenv(find_dotenv())


API_TOKEN = os.getenv('token')

storage = MemoryStorage()
mybot = Bot(token=API_TOKEN)
dp = Dispatcher(mybot, storage=storage)


dp.middleware.setup(AccessMiddleware())


k = StartInlineKeyboard()
k.add_button('журнал веса ⚖️', 'weight journal')
k.add_button('журнал тренировок 🏋️', 'workout journal')
k.add_button('журнал расходов 💵', 'expencse journal')


@dp.message_handler(commands=['start', 'help'])
@dp.message_handler(Text(equals=['старт', 'start', 'Старт', 'Start']))
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command.
    """
    await message.reply(f'Hi!\nman', reply_markup=k.keyboard)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == 'start'
)
async def root_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Главное меню', reply_markup=k.keyboard)


async def cancel_handler_inline(callback: types.CallbackQuery, state):
    """Сброс машины состояний."""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.delete()
    await callback.answer('Добавление записи отменено!')


dp.register_callback_query_handler(
    cancel_handler_inline, text='cancel', state='*'
)

# хендлеры журнала веса
dp.register_callback_query_handler(weight_journal_root, text='weight journal')
dp.register_callback_query_handler(add_in_weight_journal, text='add weight')
dp.register_callback_query_handler(change_value_weight, text='change weight')
dp.register_message_handler(
    write_to_database_new_value_weight, state=NewJournalEntries.add_value
)
dp.register_message_handler(
    change_weight_value, state=ChangeJournalEntries.change_value
)

# хендлеры журнала тренировок
dp.register_callback_query_handler(
    workout_journal_root, text='workout journal'
)
dp.register_callback_query_handler(get_workout_journal, text='show workout')
dp.register_callback_query_handler(
    previous_month_of_workout, lambda callback: callback.data.startswith('-')
)
dp.register_callback_query_handler(
    next_month_of_workout, lambda callback: callback.data.startswith('+')
)
dp.register_callback_query_handler(
    get_workout_for_day, lambda callback: callback.data.startswith('_')
)
dp.register_callback_query_handler(delete_current_record, text='del workout')
dp.register_callback_query_handler(
    get_workout_record_next_or_back,
    lambda callback: callback.data.startswith('&'),
)
dp.register_callback_query_handler(add_workout_in_journal, text='add workout')
dp.register_message_handler(
    write_to_database_new_value_workout, state=NewRecordWorkout.add_record
)

# хендлеры журнала расходов
dp.register_callback_query_handler(
    expencse_journal_root, text='expencse journal'
)
dp.register_callback_query_handler(
    get_expenses_for_day, text='get current table'
)
dp.register_callback_query_handler(
    add_expenses_in_journal, text='add  expense'
)
dp.register_callback_query_handler(
    parse_categories_for_expenses,
    lambda callback: callback.data.startswith('^'),
)
dp.register_message_handler(
    write_to_database_new_expense, state=NewRecordExpense.add_record
)
dp.register_message_handler(
    write_to_database_change_expense, state=ChangeRecordExpense.change_record
)
dp.register_callback_query_handler(change_last_record, text='change expence')


def bot_run():
    get_loggs()
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    get_loggs()
    executor.start_polling(dp, skip_updates=True)
