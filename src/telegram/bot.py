import asyncio
import locale
import logging
import sys

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import find_dotenv, load_dotenv

from config import settings
from src.services.reminders import RemindersScheduleService
from src.telegram.handlers.base import router as base_router
from src.telegram.handlers.expenses import router as expenses_router
from src.telegram.handlers.profile import router as profile_router
from src.telegram.handlers.reminders import router as reminder_router
from src.telegram.handlers.weight import router as weight_router
from src.telegram.handlers.workout import router as workout_router
from src.telegram.middleware import UnsupportedTagCleanerMiddleware

# установка родной локали, чтобы название месяца Python стал выводить кириллицей
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
load_dotenv(find_dotenv())


async def bot_run():
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s',
        datefmt='%Y-%m-%d,%H:%M:%S',
    )

    if not settings.BOT_TOKEN:
        raise ValueError('Отсутствует токен для бота')

    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.update.outer_middleware(UnsupportedTagCleanerMiddleware(bot))

    dp.include_router(base_router)
    dp.include_router(workout_router)
    dp.include_router(expenses_router)
    dp.include_router(weight_router)
    dp.include_router(profile_router)
    dp.include_router(reminder_router)

    scheduler = AsyncIOScheduler()
    scheduler_service = RemindersScheduleService(bot)
    scheduler.add_job(
        scheduler_service.check_reminders,
        trigger=IntervalTrigger(minutes=1),
        id='check_db_of_reminders',
        replace_existing=True,
    )
    scheduler.start()

    await dp.start_polling(
        bot,
        skip_updates=True,
    )


if __name__ == '__main__':
    asyncio.run(bot_run())
