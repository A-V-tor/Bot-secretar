import datetime

import pytz
from aiogram import Bot, types

from config import settings
from src.database.models.reminders import Reminder
from src.database.models.users import User
from src.utils.tools import ReminderLevel

logger = settings.bot_logger


class RemindersTelegramService:
    """Сервис для работы с сущностью напоминаний."""

    model = Reminder

    def __init__(self, message: types.Message | types.CallbackQuery):
        if isinstance(message, types.Message):
            self.telegram_id = message.chat.id
        else:
            self.telegram_id = message.message.chat.id

    async def new_reminder(self, value: str, type_expenses: ReminderLevel, datetime_str: str) -> str:
        timestamp = datetime.datetime.strptime(datetime_str, '%d.%m.%Y %H:%M')
        user = User.get_user_by_telegram_id(self.telegram_id)
        user_tz = pytz.timezone(user.time_zones[0].time_zones.value)
        localized_time = user_tz.localize(timestamp)
        res = self.model.add_new_note(self.telegram_id, value, type_expenses, localized_time)
        msg = 'Напоминание добавлено' if res else 'Что-то пошло не так'

        return msg

    async def get_reminders_days_for_current_month(self, month: int, year: int):
        """Получение дней напоминаний юзера в этом месяце."""
        month_string = datetime.datetime(year, month, 1).strftime('%B')
        msg = f'С 1 {month_string} {year} года'

        reminder_days = self.model.get_reminders_for_month(self.telegram_id, month, year)

        return reminder_days, msg

    async def get_note_by_date(self, telegram_id: int, day: int, month: int, year: int):
        notes = self.model.get_note_by_date(telegram_id, day, month, year)
        return notes if notes else None


class RemindersScheduleService:
    """Сервис для работы с сущностью напоминаний в шедулере."""

    model = Reminder

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_messages_reminders(self, current_reminder: Reminder):
        reminder = str(current_reminder.value)
        msg = f'Напоминание\n✖️ ✖️ ✖️ ✖️ ✖️ ✖️\n{reminder}'

        response = await self.bot.send_message(current_reminder.user_telegram_id, msg)
        if getattr(response, 'message_id', None):
            res = self.model.disable_reminder(current_reminder.id).first()
            telegram_id = current_reminder.user_telegram_id
            res_msg = (
                f'Запись № {res[0]} помечена отправленной: <{telegram_id}>'
                if res
                else f'Запись № {current_reminder.id} не помечена отправленной: <{telegram_id}>'
            )
            logger.info(f'{res_msg}')
        else:
            logger.info(f'Нет message_id для: {response}')

    async def check_reminders(self):
        """Проверка напоминаний и рассылка по ним."""
        today = datetime.datetime.today()
        year, month, day, hour, minute = (
            today.year,
            today.month,
            today.day,
            today.hour,
            today.minute,
        )
        reminders = self.model.get_reminders_for_current_minute(day, month, year, hour, minute)

        for reminder_note in reminders:
            # TODO: нужна будет проверка на уровень важности и разделение логики в send_messages_reminders
            # если очень важно - допустим не исключать запись, а переносить на какое то время в будущее
            # пока она напрямую не будет снята
            await self.send_messages_reminders(reminder_note)
