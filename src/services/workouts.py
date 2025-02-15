import datetime
from src.database.models.workouts import Workout
from aiogram import types
from src.utils.text_templates import note_workout
from collections import deque
from src.utils.tools import clean_unsupported_tags


class WorkoutTelegramService:
    """Сервис для работы с сущностью тренировок в боте."""

    model = Workout

    def __init__(self, message: types.Message | types.CallbackQuery):
        if isinstance(message, types.Message):
            self.telegram_id = message.chat.id
        else:
            self.telegram_id = message.message.chat.id

    async def get_workout_days_for_current_month(self, month: int, year: int):
        """Получение дней тренировок юзера в этом месяце."""

        month_string = datetime.datetime(year, month, 1).strftime('%B')
        msg = f'С 1 {month_string} {year} года'

        workout_days = self.model.get_workouts_for_month(
            self.telegram_id, month, year
        )

        return workout_days, msg

    async def get_workouts_current_day(self, day: int, month: int, year: int):
        """Получение дней тренировок юзера за выбранный день."""

        msg = 'Нет записей в этот день'
        workouts_day = self.model.get_workouts_for_timestamp(
            self.telegram_id, day, month, year
        )

        if workouts_day:
            msg = note_workout.format(
                date=workouts_day[0].created_at,
                len_workouts=len(workouts_day),
                text=workouts_day[0].text_value,
            )
            msg = clean_unsupported_tags(msg)

        return workouts_day, msg

    async def save_workout(self, text: str):
        check = self.model.new_workout(self.telegram_id, text)

        msg = (
            'Тренировка добавлена'
            if check
            else 'Запись не сохранена, попробуйте позже'
        )

        return msg

    @staticmethod
    async def show_workout(move: str, data: dict):
        current_workouts: deque = data.get('workouts')
        len_notes = len(current_workouts)

        current_workouts.rotate(
            -1
        ) if move == 'forward' else current_workouts.rotate(1)
        current_note = current_workouts[0]

        msg = note_workout.format(
            date=current_note.created_at,
            len_workouts=len_notes,
            text=current_note.text_value,
        )

        return current_workouts, msg

    @staticmethod
    async def delete_note(data: dict):
        current_workouts: deque = data.get('workouts')

        note_id: int = current_workouts[0].id
        result = Workout.delete_note(note_id)

        if result:
            msg = '<b>Запись удалена</b>\n'
            current_workouts.popleft()
        else:
            msg = 'Не удалось удалить запись\n'

        return current_workouts, msg
