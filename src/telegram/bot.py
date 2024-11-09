import sys
import logging
import asyncio
from dotenv import find_dotenv, load_dotenv
from aiogram import Dispatcher, Bot
from src.telegram.handlers.base import router as base_router
from src.telegram.handlers.workout import router as workout_router
from src.telegram.handlers.expenses import router as expenses_router
from src.telegram.handlers.weight import router as weight_router

from config import settings
import locale

# установка родной локали, чтобы название месяца Python стал выводить кириллицей
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
load_dotenv(find_dotenv())


async def bot_run():
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt="%Y-%m-%d,%H:%M:%S",
    )
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(base_router)
    dp.include_router(workout_router)
    dp.include_router(expenses_router)
    dp.include_router(weight_router)

    await dp.start_polling(
        bot,
        skip_updates=True,
    )

if __name__ == '__main__':
    asyncio.run(bot_run())
