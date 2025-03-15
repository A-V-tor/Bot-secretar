from aiogram.types import (
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def profile_kb():
    keyboard = InlineKeyboardBuilder()
    root_menu = InlineKeyboardButton(text='🗂', callback_data='start')
    change_psw = InlineKeyboardButton(text='сменить пароль', callback_data='change-password')
    keyboard.row(root_menu).row(change_psw)

    return keyboard.as_markup()
