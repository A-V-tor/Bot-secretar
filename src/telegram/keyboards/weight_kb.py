import os
import datetime
from src.database.models.workouts import Workout
import calendar
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.utils.tools import get_next_month_and_year, get_prev_month_and_year


async def root_menu_weight_kb(presence_of_record=False):
    keyboard = InlineKeyboardBuilder()

    root_menu = InlineKeyboardButton(text='🗂', callback_data='start')
    journal = InlineKeyboardButton(text='журнал', callback_data='show weight')
    new_note = InlineKeyboardButton(
        text='добавить', callback_data='add weight'
    )
    change_note = InlineKeyboardButton(
        text='✍️ изменить', callback_data='change weight'
    )

    keyboard.row(root_menu).row(journal)

    if not presence_of_record:
        keyboard.row(new_note)
    else:
        keyboard.row(change_note)

    return keyboard.as_markup()


async def yes_or_no_save_weight_kb():
    keyboard = InlineKeyboardBuilder()

    kb_no = InlineKeyboardButton(text='отмена', callback_data='cancel')
    kb_yes = InlineKeyboardButton(text='да', callback_data='yes_weight')
    keyboard.row(kb_no).row(kb_yes)

    return keyboard.as_markup()


async def yes_or_no_save_change_weight_kb():
    keyboard = InlineKeyboardBuilder()

    kb_no = InlineKeyboardButton(text='отмена', callback_data='cancel')
    kb_yes = InlineKeyboardButton(text='да', callback_data='yes_change_weight')
    keyboard.row(kb_no).row(kb_yes)

    return keyboard.as_markup()
