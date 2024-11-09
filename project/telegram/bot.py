import os, sys
import asyncio
from dotenv import find_dotenv, load_dotenv
from aiogram import Router, F, Dispatcher, Bot, types
from aiogram.filters.command import CommandStart
from .keyboards import start_kb
from .weight_journal import router as weight_router
from .workout_journal import router as workout_router
from .expense_journal import router as expense_router
# from .middlewares import AccessMiddleware
import locale

from .logger import get_loggs

# установка родной локали, чтобы название месяца Python стал выводить кириллицей
locale.setlocale(locale.LC_ALL)   # 'ru_RU' сервак слетает
load_dotenv(find_dotenv())


API_TOKEN = os.getenv('token')

# dp.middleware.setup(AccessMiddleware())

router = Router(name = 'base')


@router.message(CommandStart())
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command.
    """

    await message.reply(f'Hi!\nman', reply_markup=await start_kb())


@router.callback_query(F.data == 'start')
async def root_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Главное меню', reply_markup=await start_kb())


@router.callback_query(F.data == 'cancel')
async def cancel_handler_inline(callback: types.CallbackQuery, state):
    """Сброс машины состояний."""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.delete()
    await callback.answer('Добавление записи отменено!')



async def bot_run():
    bot = Bot(API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(weight_router)
    dp.include_router(workout_router)
    dp.include_router(expense_router)

    await dp.start_polling(
        bot,
        skip_updates=True,
    )



if __name__ == '__main__':
    asyncio.run(bot_run())
