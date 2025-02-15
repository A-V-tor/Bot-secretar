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
from src.utils.tools import TypeExpenses


async def root_menu_expanses_kb():
    keyboard = InlineKeyboardBuilder()

    root_menu = InlineKeyboardButton(text="🗂", callback_data="start")
    journal = InlineKeyboardButton(text="журнал", callback_data="show expanses")
    new_note = InlineKeyboardButton(text="добавить", callback_data="add expanses")


    keyboard.row(root_menu).row(journal).row(new_note)

    return keyboard.as_markup()


async def category_expenses_kb():
    keyboard = InlineKeyboardBuilder()
    root_menu = InlineKeyboardButton(text="🗂", callback_data="start")
    back = InlineKeyboardButton(text="назад", callback_data="expense journal")
    keyboard.row(root_menu)

    for field in TypeExpenses:
        keyboard.row(InlineKeyboardButton(text=f"{field.value}", callback_data=f"{field}"))

    keyboard.row(back)

    return keyboard.as_markup()


async def yes_or_no_save_expenses_kb():
    keyboard = InlineKeyboardBuilder()

    kb_no = InlineKeyboardButton(text="отмена", callback_data="cancel")
    kb_yes = InlineKeyboardButton(text="да", callback_data="yes_expenses")
    keyboard.row(kb_no).row(kb_yes)

    return keyboard.as_markup()


async def expanses_journal_kb(flag_last_note = False):
    keyboard = InlineKeyboardBuilder()

    root_menu = InlineKeyboardButton(text="🗂", callback_data="start")
    back = InlineKeyboardButton(text="назад", callback_data="expense journal")

    keyboard.row(root_menu).row(back)

    if flag_last_note:
        keyboard.row(
            InlineKeyboardButton(text="✏️ последняя запись", callback_data="edit_last_expenses")
        )

    return keyboard.as_markup()


async def category_expenses_last_name_kb():
    keyboard = InlineKeyboardBuilder()
    kb_cancel = InlineKeyboardButton(text="отмена", callback_data="cancel")
    keyboard.row(kb_cancel)

    for field in TypeExpenses:
        keyboard.row(InlineKeyboardButton(text=f"{field.value}", callback_data=f"last_{field}"))

    keyboard.row(
        InlineKeyboardButton(text="оставить", callback_data="current_last_expenses")
    )

    return keyboard.as_markup()

async def yes_or_no_save_last_note_expenses_kb():
    keyboard = InlineKeyboardBuilder()

    kb_no = InlineKeyboardButton(text="отмена", callback_data="cancel")
    kb_yes = InlineKeyboardButton(text="да", callback_data="yes_last_expenses")
    keyboard.row(kb_no).row(kb_yes)

    return keyboard.as_markup()
