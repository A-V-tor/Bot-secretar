from aiogram import Router, types, F
from ..keyboards.profile import profile_kb
from ..keyboards.base_kb import start_kb
from src.services.users import UserTelegramService
from aiogram.fsm.context import FSMContext

router = Router(name='profile')


@router.callback_query(F.data == 'profile')
async def root_profile(callback: types.CallbackQuery):
    """Меню профиля юзера."""

    user_service = UserTelegramService(callback)
    user, _ = await user_service.check_user_by_telegram()
    msg = f'Ваши Логин: {user.username}'

    await callback.message.delete()
    await callback.message.answer(
        msg, reply_markup=await profile_kb(), parse_mode='HTML'
    )


@router.callback_query(F.data == 'change-password')
async def new_password(callback: types.CallbackQuery):
    """Генерация нового пароля."""
    await callback.message.delete()

    user_service = UserTelegramService(callback)
    msg = await user_service.change_password()

    await callback.message.answer(
        msg, reply_markup=await start_kb(), parse_mode='HTML'
    )
