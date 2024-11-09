from aiogram import Router, types, F
from aiogram.filters.command import CommandStart
from ..keyboards.base_kb import start_kb
from src.service.users import UserTelegramService
from aiogram.fsm.context import FSMContext

router = Router(name = 'base')


@router.message(CommandStart())
async def start_command(message: types.Message):
    """Стартовое меню."""

    user_service = UserTelegramService(message)
    user, msg = await user_service.check_user_by_telegram()

    if not user:
        msg = await user_service.create_new_user()

    await message.reply(msg, reply_markup=await start_kb(), parse_mode='HTML')


@router.callback_query(F.data == 'start')
async def root_menu(callback: types.CallbackQuery):
    """Стартовое меню для инлайна."""

    user_service = UserTelegramService(callback)
    user, msg = await user_service.check_user_by_telegram()

    if not user:
        msg = await user_service.create_new_user()

    await callback.message.delete()
    await callback.message.answer(msg, reply_markup=await start_kb(), parse_mode='HTML')


@router.callback_query(F.data == 'cancel')
async def cancel_handler_inline(callback: types.CallbackQuery, state: FSMContext):
    """Сброс машины состояний."""

    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Отменено', reply_markup=await start_kb())
