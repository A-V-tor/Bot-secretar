import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
API_TOKEN = os.getenv('token')


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command.
    """
    await message.reply(f'Hi!\nman')


def bot_run():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
