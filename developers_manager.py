from multiprocessing import Process
from project.adminpanel import web_run
from project.telegram import bot_run
from project.database.database import engine
from project.database.models import Base


if __name__ == '__main__':
    # создание таблиц бд
    Base.metadata.create_all(bind=engine)

    tg = Process(target=bot_run)
    web = Process(target=web_run)

    web.start()
    tg.start()

    tg.join()
    web.join()
