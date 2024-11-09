import asyncio
import subprocess
from concurrent.futures import ProcessPoolExecutor
from project.adminpanel import web_run
from project.telegram import bot_run


def start_fastapp():
    subprocess.call(['python', '-m', 'app'])


def start_bot():
    subprocess.call(['python', '-m', 'app_bot'])


if __name__ == '__main__':
    with ProcessPoolExecutor() as pool:
        pool.submit(start_bot)
        pool.submit(start_fastapp)
