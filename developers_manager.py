from multiprocessing import Process
from project.adminpanel import web_run
from project.telegram import bot_run


if __name__ == '__main__':

    tg = Process(target=bot_run)
    web = Process(target=web_run)

    web.start()
    tg.start()

    tg.join()
    web.join()
