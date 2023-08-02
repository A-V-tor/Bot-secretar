import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv
from .keyboards import StartInlineKeyboard
from .weight_journal import (
    weight_journal_root,
    add_in_weight_journal,
    add_new_value,
    change_value_weight,
    change_weight_value,
    NewJournalEntries,
    ChangeJournalEntries,
)


load_dotenv(find_dotenv())
API_TOKEN = os.getenv('token')

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
@dp.message_handler(Text(equals=['старт', 'start', 'Старт', 'Start']))
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command.
    """
    k = StartInlineKeyboard()
    k.add_button('журнал веса', 'weight journal')
    await message.reply(f'Hi!\nman', reply_markup=k.keyboard)


dp.register_callback_query_handler(weight_journal_root, text='weight journal')
dp.register_callback_query_handler(add_in_weight_journal, text='add weight')
dp.register_callback_query_handler(change_value_weight, text='change weight')
dp.register_message_handler(add_new_value, state=NewJournalEntries.add_value)
dp.register_message_handler(
    change_weight_value, state=ChangeJournalEntries.change_value
)


def bot_run():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
