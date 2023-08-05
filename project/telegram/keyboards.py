from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from abc import ABC, abstractmethod


class AbstractInlineKeyboard(ABC):
    def __init__(self):
        self.keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    @abstractmethod
    def add_button(self, text, callback_data):
        pass


class StartInlineKeyboard(AbstractInlineKeyboard):
    def add_button(self, text, callback_data):
        self.keyboard.add(
            InlineKeyboardButton(text, callback_data=callback_data)
        )


class WeightInlineKeyboard(AbstractInlineKeyboard):
    def __init__(self):
        super().__init__()
        self.add_button('/', 'start')

    def add_button(self, text, callback_data):
        self.keyboard.add(
            InlineKeyboardButton(text, callback_data=callback_data)
        )


class WorkoutInlineKeyboard(AbstractInlineKeyboard):
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

    def get_buttons_next_or_back_record(self):
        self.add_button('следующая', callback_data='& next workout')
        self.add_button('предыдущая', callback_data='& back workout')

    def button_delete_record(self):
        self.add_button('удалить', 'del workout')

    def get_buttons_cl(self, month, year):
        self.add_button('назад', f'-{month} {year}')
        self.insert_button('вперед', f'+{month} {year}')

    def button_start_menu(self):
        self.add_button('/', 'start')

    def button_cancel(self):
        self.add_button('отмена', 'cancel')
