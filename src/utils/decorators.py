import asyncio
import inspect
from typing import Callable

from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from aiohttp import ServerDisconnectedError

from config import settings

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
                try:
                    logger.info(f'Попытка {attempt + 1} для функции {func.__name__}')
                    return await func(*args, **filtered_kwargs)
                except (TelegramNetworkError, TelegramBadRequest, ServerDisconnectedError) as e:
                    logger.info(f'Ошибка сети Telegram при попытке {attempt + 1}: {e.__class__.__name__} - {e}')
                    if attempt < retry_count - 1:
                        await asyncio.sleep(delay)
                        delay = min(delay * 1.5, retry_max_delay)
                    else:
                        logger.info(f'Превышено количество попыток для функции {func.__name__}')
                        raise

        return inner

    return wrapper
