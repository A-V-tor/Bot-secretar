import asyncio
import inspect
from typing import Callable

from aiogram import types
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from aiohttp import ServerDisconnectedError

from config import settings
from src.utils.text_templates import retry_logs

logger = settings.bot_logger


def retry_on_connection_error(
    retry_count: int = 5,
    retry_min_delay: int | float = 0.2,
    retry_max_delay: int | float = 1,
) -> Callable:
    """Декоратор для повторных попыток при ошибке TelegramNetworkError или TelegramBadRequest.

    :param retry_count: Количество попыток
    :param retry_min_delay: Начальная задержка между попытками в секундах
    :param retry_max_delay: Максимальная задержка между попытками в секундах
    :return: Обернутая функция
    """

    def wrapper(func: Callable):
        func_args = inspect.signature(func).parameters

        async def inner(*args, **kwargs):
            delay = retry_min_delay
            filtered_kwargs = {name: value for name, value in kwargs.items() if name in func_args}
            for attempt in range(retry_count):
                event = args[0]
                try:
                    if isinstance(event.message, types.Message):
                        log_msg = retry_logs.format(
                            attempt=attempt + 1,
                            event=event.update_id,
                            chat_id=event.message.chat.id,
                            username=event.message.chat.username,
                            text=event.message.text,
                        )
                    else:
                        log_msg = retry_logs.format(
                            attempt=attempt + 1,
                            event=event.update_id,
                            chat_id=event.callback_query.from_user.id,
                            username=event.callback_query.from_user.username,
                            text=event.callback_query.message.text,
                        )
                    logger.info(log_msg)
                    return await func(*args, **filtered_kwargs)
                except (TelegramNetworkError, TelegramBadRequest, ServerDisconnectedError) as e:
                    logger.info(f'Ошибка сети Telegram при попытке {attempt + 1}: {e.__class__.__name__} - {e}')
                    if attempt < retry_count - 1:
                        await asyncio.sleep(delay)
                        delay = min(delay * 1.5, retry_max_delay)
                    else:
                        logger.info(f'Превышено количество попыток для события {event.update_id}')
                        raise

        return inner

    return wrapper
