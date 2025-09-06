import subprocess
from concurrent.futures import ProcessPoolExecutor

from config import settings

web_logger = settings.web_logger
bot_logger = settings.bot_logger


def start_web():
    subprocess.call(['gunicorn', '--bind', '0.0.0.0:5000', '-w 4', 'web_app:app'])


def start_bot():
    subprocess.call(['python', '-m', 'bot_app'])


def main():
    with ProcessPoolExecutor() as pool:
        pool.submit(start_bot)
        bot_logger.info('🔘 Запуск бота')
        pool.submit(start_web)
        web_logger.info('🌐 Запуск админки')


if __name__ == '__main__':
    main()
