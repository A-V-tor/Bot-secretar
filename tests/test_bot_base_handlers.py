import re
from unittest.mock import AsyncMock

import pytest

from src.telegram.handlers.base import root_menu, start_command
from src.telegram.keyboards.base_kb import start_kb


class TestBase:
    """
    Тестирования базовых хендлеров бота.
    `src.telegram.handlers.base`
    """

    @pytest.mark.asyncio
    async def test_start_command_with_create_user(self, message, get_db, user):
        """
        Создание нового пользовател в бд при первом вызове `/start` юзером.
        """
        message.text = '/start'
        message.reply = AsyncMock()

        await start_command(message=message)

        message.reply.assert_called()
        actual_msg = message.reply.call_args[0][0]
        assert re.search(r'Вы добавлены в пользователи бота', actual_msg)

        # проверка других аргументов (reply_markup и parse_mode)
        actual_reply_markup = message.reply.call_args[1]['reply_markup']
        assert actual_reply_markup == await start_kb()
        assert message.reply.call_args[1]['parse_mode'] == 'HTML'

    @pytest.mark.asyncio
    async def test_start_command_with_existing_user(self, message, get_db, user):
        """
        Проверка и получение данных при вызове `/start` юзером.
        """
        message.text = '/start'
        message.reply = AsyncMock()

        await start_command(message=message)

        message.reply.assert_called_with('Главное меню', reply_markup=await start_kb(), parse_mode='HTML')

    @pytest.mark.asyncio
    async def test_callback_handler_root_menu(self, callback_query, user):
        """
        Проверка и получение данных при нажатии инлайн кнопки в главное меню.
        """

        callback_query.message.answer = AsyncMock()
        callback_query.message.delete = AsyncMock()

        await root_menu(callback_query)
        callback_query.message.delete.assert_called()
        callback_query.message.answer.assert_called_with(
            'Главное меню', reply_markup=await start_kb(), parse_mode='HTML'
        )
