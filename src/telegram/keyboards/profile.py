from aiogram.types import (
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils.tools import TimeZoneEnum


async def profile_kb():
    keyboard = InlineKeyboardBuilder()
    root_menu = InlineKeyboardButton(text='🗂', callback_data='start')
    change_psw = InlineKeyboardButton(text='сменить пароль', callback_data='change-password')
    time_zone = InlineKeyboardButton(text='таймзона', callback_data='user-timezone')
    keyboard.row(root_menu).row(change_psw).row(time_zone)

    return keyboard.as_markup()


async def timezone_kb():
    keyboard = InlineKeyboardBuilder()
    for time_zone in TimeZoneEnum:
        keyboard.row(InlineKeyboardButton(text=time_zone.value, callback_data=f'timezone_user-{time_zone.value}'))
    root_menu = InlineKeyboardButton(text='🗂', callback_data='start')
    keyboard.row(root_menu)

    return keyboard.as_markup()
