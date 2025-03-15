import datetime

from aiogram import types
from prettytable import PrettyTable

from src.database.models.expenses import Expenses


class ExpensesTelegramService:
    """Сервис для работы с сущностью расходов."""

    model = Expenses

    def __init__(self, message: types.Message | types.CallbackQuery):
        if isinstance(message, types.Message):
            self.telegram_id = message.chat.id
        else:
            self.telegram_id = message.message.chat.id

    async def get_expenses_for_day(self):
        today = datetime.date.today()
        year, month, day = today.year, today.month, today.day
        notes: list[Expenses] | list = self.model.get_expenses_for_day(self.telegram_id, day, month, year)

        flag_last_note = True if notes else False
        my_table = PrettyTable()
        my_table.field_names = ['Категория', 'Рублей']
        total = 0

        for note in notes:
            total += note[1]
            my_table.add_row([note[0].value, note[1]])

        my_table.add_row(['---------', '------'])
        my_table.add_row(['ИТОГО', total])

        return my_table, flag_last_note

    async def save_new_expenses(self, money: int, category: str) -> str:
        result = self.model.add_new_note(self.telegram_id, money, category)

        return 'Запись сохранена' if result else 'Что-то пошло не так'

    async def get_last_note(self):
        today = datetime.date.today()
        year, month, day = today.year, today.month, today.day
        last_note = self.model.get_last_note_for_current_day(year, month, day)

        return last_note

    async def update_last_note(self, note_id: int, money: int, category: str):
        result = self.model.update_last_note_for_current_day(note_id, money, category)

        msg = 'Запись обновлена' if result else 'Что-то пошло не так'

        return msg


class ExpensesDashbordService:
    """Сервис для работы с сущностью расходов."""

    model = Expenses

    def __init__(self, telegram_id: int):
        self.user_telegram_id = telegram_id

    def get_all_expenses_by_telegram_id(self):
        result = self.model.get_all_expenses_by_telegram_id(self.user_telegram_id)

        return result
