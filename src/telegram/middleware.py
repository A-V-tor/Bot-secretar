from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from aiogram.types.update import Update

from src.utils.custom_aiogram import MessageCustom, UpdateCustom
from src.utils.decorators import retry_on_connection_error
from src.utils.tools import clean_unsupported_tags


class UnsupportedTagCleanerMiddleware(BaseMiddleware):
    """
    Очиститель/валидатор текста сообщений.
    """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def __call__(
        self, handler: Callable[[Update, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]
    ) -> Any:
        if event.message:
            event = UpdateCustom(**event.dict())
            new_msg = MessageCustom(**event.message.dict())
            # связать бота с новым обьектом MessageCustom
            new_msg = new_msg.as_(self.bot)
            event.message = new_msg

            event.message.text = clean_unsupported_tags(event.message.text)

        decorated_handler = retry_on_connection_error()(handler)
        return await decorated_handler(event, data)
