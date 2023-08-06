from aiogram import types
import os
from aiogram.dispatcher.middlewares import BaseMiddleware
from dotenv import load_dotenv

load_dotenv()

env_values = os.getenv('owner_id')
values_list = env_values.split(',')

# Преобразуем список значений из строк в список чисел
allowed_user_id = [int(value) for value in values_list]


class NotAccessRights(Exception):
    def __init__(
        self,
        message='У вас нет прав доступа к этой команде: user ',
        user_id=None,
    ):
        self.message = message + str(user_id)
        super().__init__(self.message)


# Миддлвар для проверки прав доступа к командам
class AccessMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        if user_id not in allowed_user_id:

            # Если пользователь не имеет доступа
            raise NotAccessRights(user_id=user_id)
