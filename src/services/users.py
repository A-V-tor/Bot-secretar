from aiogram import types

from src.database.models.users import User
from src.utils.text_templates import text_for_new_user
from src.utils.tools import generate_password


class UserTelegramService:
    """Сервис для работы с сущностью юзера в боте."""

    model = User

    def __init__(self, message: types.Message | types.CallbackQuery):
        if isinstance(message, types.Message):
            self.telegram_id = message.chat.id
            self.username = message.chat.username
            self.first_name = message.chat.first_name
            self.last_name = message.chat.last_name
        else:
            self.telegram_id = message.message.chat.id
            self.username = message.message.chat.username
            self.first_name = message.message.chat.first_name
            self.last_name = message.message.chat.last_name

    async def check_user_by_telegram(self):
        """Проверка наличия юзера в базе по tg_id."""
        user = self.model.get_user_by_telegram_id(self.telegram_id)

        return user, 'Главное меню' if user else False

    async def create_new_user(self):
        """Создание нового пользователя в бд."""
        user_psw = self.model.create_user(self.username, self.telegram_id, self.first_name, self.last_name)

        msg = text_for_new_user.format(username=self.username, user_psw=user_psw)
        result = msg if user_psw else 'Что-то пошло не так, попробуйте позже'

        return result

    async def change_password(self):
        """Создание нового пароля профиля."""
        password = generate_password()
        user_psw = self.model.set_new_password(password, self.telegram_id)

        msg = text_for_new_user.format(username=self.username, user_psw=user_psw)
        result = msg if user_psw else 'Что-то пошло не так, попробуйте позже'

        return result
