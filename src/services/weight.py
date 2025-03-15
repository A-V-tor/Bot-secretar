import datetime

from aiogram import types

from src.database.models.weight import Weight


class WeightTelegramService:
    """Сервис для работы с сущностью веса в боте."""

    model = Weight

    def __init__(self, message: types.Message | types.CallbackQuery):
        if isinstance(message, types.Message):
            self.telegram_id = message.chat.id
        else:
            self.telegram_id = message.message.chat.id

    async def check_note(self):
        today = datetime.date.today()
        year, month, day = today.year, today.month, today.day
        result = self.model.check_note_by_telegram_id(self.telegram_id, year, month, day)

        return result

    async def save_change_weight(self, note_id: int, weight: float):
        result = self.model.update_note_by_telegram_id(note_id, weight)
        msg = 'Запись обновлена' if result else 'Что-то пошло не так'

        return msg

    async def save_weight(self, weight: float):
        result = self.model.new_note_weight(self.telegram_id, weight)

        msg = 'Запись сделана' if result else 'Что-то пошло не так'
        return msg


class WeightDashbordService:
    """Сервис для работы с сущностью расходов."""

    model = Weight

    def __init__(self, telegram_id: int):
        self.user_telegram_id = telegram_id

    def get_all_weight_by_telegram_id(self):
        result = self.model.get_all_weight_notes_by_telegram_id(self.user_telegram_id)

        return result
