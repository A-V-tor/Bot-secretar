import logging

def get_loggs():
    logging.basicConfig(
        level=logging.WARNING,
        filename = r"bot/mylog.log",
        format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%H:%M:%S',
        )
    '''при сборке пакета изменить путь!!!'''

    logging.info('Hello')
# Documents/TG_bot/bot/mylog.log