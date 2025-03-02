from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def profile_kb():
    keyboard = InlineKeyboardBuilder()
    change_psw = InlineKeyboardButton(
        text='сменить пароль', callback_data='change-password'
    )
    keyboard.row(change_psw)

    return keyboard.as_markup()
