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
    def add_button(self, text, callback_data):
        self.keyboard.add(
            InlineKeyboardButton(text, callback_data=callback_data)
        )
