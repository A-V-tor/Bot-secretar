import subprocess
from concurrent.futures import ProcessPoolExecutor


def start_web():
    subprocess.call(
        ['gunicorn', '--bind', '0.0.0.0:5000', '-w 4', 'web_app:app']
    )


def start_bot():
    subprocess.call(['python', '-m', 'bot_app'])


def main():
    with ProcessPoolExecutor() as pool:
        pool.submit(start_bot)
        pool.submit(start_web)


if __name__ == '__main__':
    main()
