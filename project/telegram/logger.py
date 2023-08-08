import logging


def get_loggs():
    logging.basicConfig(
        level=logging.WARNING,
        filename='bot.log',
        format='%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s',
        datefmt='%H:%M:%S',
    )
