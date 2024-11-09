import os
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from abc import ABC, abstractmethod


load_dotenv()
URL_ADMIN = os.getenv('URL_ADMIN')


class AbstractInlineKeyboard(ABC):
    def __init__(self):
        self.keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    def add_button(self, text, callback_data):
        self.keyboard.add(
            InlineKeyboardButton(text, callback_data=callback_data)
        )

    def insert_button(self, text, callback_data):
        self.keyboard.insert(
            InlineKeyboardButton(text, callback_data=callback_data)
        )

    def make_row_width(self, num):
        self.keyboard.row_width = num

    def button_start_menu(self):
        self.add_button('🗂️', 'start')

    def button_cancel(self):
        self.add_button('отмена', 'cancel')


class StartInlineKeyboard(AbstractInlineKeyboard):
    def __init__(self):
        """Конпка входа в админку."""
        super().__init__()
        kb_web = InlineKeyboardButton('📟 Админка 📟', url=URL_ADMIN)
        self.keyboard.add(kb_web)

async def start_kb(cancel: bool = False):
    keyboard = InlineKeyboardBuilder()

    weight = InlineKeyboardButton(text="журнал веса ⚖️", callback_data="workout journal")
    workout = InlineKeyboardButton(text="журнал тренировок 🏋️", callback_data="weight journal")
    expense = InlineKeyboardButton(text="журнал расходов 💵", callback_data="expencse journal")

    keyboard.row(weight).row(workout).row(expense)

    if cancel:
        kb_cancel = InlineKeyboardButton(text="отмена", callback_data="cancel")
        keyboard.row(kb_cancel)

    return keyboard.as_markup()


async def weight_journal_kb():
    keyboard = InlineKeyboardBuilder()

    change_weight = InlineKeyboardButton(text="изменить запись", callback_data="change weight")
    add_weight = InlineKeyboardButton(text="добавить запись", callback_data="add weight")


class WeightInlineKeyboard(AbstractInlineKeyboard):
    pass


class WorkoutInlineKeyboard(AbstractInlineKeyboard):
    def get_buttons_next_or_back_record(self):
        self.add_button('следующая', callback_data='& next workout')
        self.add_button('предыдущая', callback_data='& back workout')

    def button_delete_record(self):
        self.add_button('удалить', 'del workout')

    def get_buttons_cl(self, month, year):
        self.add_button('назад', f'-{month} {year}')
        self.insert_button('вперед', f'+{month} {year}')


class ExpenseInlineKeyboard(AbstractInlineKeyboard):
    def button_root_expense(self):
        self.add_button('<<', 'expencse journal')

    def expense_category_buttons(self):
        self.add_button('здоровье', '^ health')
        self.add_button('транспорт', '^ transport')
        self.add_button('еда', '^ food')
        self.add_button('развлечения', '^ entertainment')
        self.add_button('покупки', '^ purchases')
        self.add_button('подарки', '^ present')
        self.add_button('прочее', '^ other')
