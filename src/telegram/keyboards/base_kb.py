import os
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import settings


async def start_kb():
    keyboard = InlineKeyboardBuilder()
    kb_web = InlineKeyboardButton(
        text='📟 Админка 📟',
        web_app=WebAppInfo(url=f'{settings.URL_ADMIN}'),
    )
    weight = InlineKeyboardButton(
        text='журнал веса ⚖️', callback_data='weight journal'
    )
    workout = InlineKeyboardButton(
        text='журнал тренировок 🏋️', callback_data='workout journal'
    )
    expense = InlineKeyboardButton(
        text='журнал расходов 💵', callback_data='expense journal'
    )
    profile = InlineKeyboardButton(text='профиль 👤', callback_data='profile')

    keyboard.row(kb_web).row(weight).row(workout).row(expense).row(profile)

    return keyboard.as_markup()


async def cansel_kb():
    keyboard = InlineKeyboardBuilder()

    kb_cancel = InlineKeyboardButton(text='отмена', callback_data='cancel')
    keyboard.row(kb_cancel)

    return keyboard.as_markup()
