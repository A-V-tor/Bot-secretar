#!/usr/bin/env python3
from cgitb import text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from bot.ScrepBot import function_screp, screp_iter, lst
from bot.Weather import get_weather
import json, string
import aiogram.utils.markdown as fmt
from bot.tkn import token_bot
from bot.keyboardd import kb, kb2, kbf, kbw, kbtr
from bot.baza import add_tren, get_workout_record, get_workout_all_record, update_tren, get_rowid



def main():
    bot = Bot(token = token_bot)
    dp = Dispatcher(bot)

    
    # отработка команды start
    @dp.message_handler(commands=['start', 'старт'])
    async def send_welcome(message: types.Message):
        await message.reply(f'Привет, {message.from_user.first_name} \U0001F464, я бот секретарь! \u270D\n\
    жми /help или воспользуйся клавиатурой,\
    чтобы подать мне команду!', reply_markup = kb)


    # отработка команды help
    @dp.message_handler(commands=['help', 'отмена'])
    async def send_help(message: types.Message):
        await message.reply('\u2193  Доступные команды бота: \u2193\n\n\
    /fonda - информация о фондовом рынке\n\n\
    /crypto - информация по криптовалютам\n\n\
    /weath - информация о погоде\n\n\
    /infotren -  информация о ведении журнала тренировок', reply_markup = kb)
        await message.delete()


    # отработка команды 'fonda'
    @dp.message_handler(commands=['fonda'])
    async def get_keyboard_info_fonda(message: types.Message):
        await message.reply('Выбери нужный раздел', reply_markup = kbf)


    # отработка команды market, отдает текущие цены
    @dp.message_handler(commands=['market'])
    async def send_fonda(message: types.Message):
        await message.answer('Жди, собираю информацию... \u23F3')
        await message.reply(screp_iter(function_screp(lst)))
        await message.delete()


    # отработка погоды
    @dp.message_handler(commands=['weath'])
    async def send_weath(message: types.Message):
        await message.reply('Отправьте свои координаты для определения погоды в вашем районе', reply_markup=kbw)
        @dp.message_handler(content_types=['location'])
        async def location(message: types.Message):
            lat = message.location.latitude
            lon = message.location.longitude
            await message.reply(f'широта:{lat}, долгота:{lon}')
            await message.reply(get_weather(lat, lon), reply_markup=ReplyKeyboardRemove())

      
    @dp.message_handler(commands=['Липецк'])
    async def send_weath(message: types.Message):
        await message.reply(get_weather(),reply_markup=ReplyKeyboardRemove())

    # отработка инфы о компаниях
    @dp.message_handler(commands=['info'])
    async def info_message(message : types.Message):
        message_text =f'Блок информации об представленых компаниях'
        await message.answer(message_text,reply_markup=kb2)
    
    # добавление тренировки в БД
    @dp.message_handler(commands=['tren','трен','Трен'])
    async def gt_tren(message : types.Message):
        data = message.text.split(',')[0][6:]
        day = message.text.split(',')[1].lower()
        bic = message.text.split(',')[2]
        waist = message.text.split(',')[3]
        chest = message.text.split(',')[4]
        tric = message.text.split(',')[5]
        await bot.send_message(message.chat.id,'Данные успешно добавлены!')
        await message.answer(add_tren(data,day,bic,waist,chest,tric))
    
        
    # получение журнала тренировок
    @dp.message_handler(commands=['get-jr'])
    async def gt_tren(message : types.Message):
        tabl = message.text.split(',')[0][8:]
        data = message.text.split(',')[1]
        await message.answer('Для корректного отображения разверни телефон')
        await bot.send_message(message.chat.id,f'{get_workout_record(tabl, data)}')


    # получение журнала тренировок
    @dp.message_handler(commands=['all-jr'])
    async def gt_tren(message : types.Message):
        item = message.text.split(',')[0][8:]
        await message.answer('Для корректного отображения разверни телефон')
        await message.answer(get_workout_all_record(item))

    # получение информации журнала тренировок
    @dp.message_handler(commands=['infotren'])
    async def gt_tren(message : types.Message):
        await message.answer('\
ПОСМОТРЕТЬ ЗАПИСЬ В ЖУРНАЛЕ ТРЕНИРОВОК:\n\n\
:/get-jr имя таблицы,кол-во повторов\n\
Пример:/get-jr biceps,23\n\
Пример выдает журнал тренировок  на бицепс с 23 повторениями.\n\
Имена таблиц:\n\
        the_data    дата\n        day         день\n        biceps   бицепс\n        waist      пояс\n        chest     грудь\n        triceps  трицепс\n\
ДЕНЬ НЕДЕЛИ УКАЗЫВАТЬ В \' КАВЫЧКАХ\' -- "вторник"\n\
\n\n\
ПОСМОТРЕТЬ ЖУРНАЛ ТРЕНИРОВОК\n\
Лимиритрованый запрос журнала:\n\
Команда: /all-jr *, где * - кол-во записей;отдает заданое кол-во записей\n\
Пример: /all-jr 2\n\n\
___________________________________________\n\n\
ДОБАВЛЕНИЕ ЗАПИСИ В ЖУРНАЛ:\n\n\
    : /tren дата,день,бицепс,пояс,грудь,трицепс\n\
Пример: /tren 3.01.22,среда,23,15,20,12\n\
При успешном добавлении,будет отображено соответствующее сообщение!\n\
___________________________________________\n\n\
ПОЛУЧЕНИЕ УНИКАЛЬНОГО ID ЗАПИСИ\
Команда rowid отдает "rowid id" по дате\n\
Синтаксис: /rowid "22.01.22" КАВЫЧКИ ОБЯЗАТЕЛЬНЫ\n\
___________________________________________\n\n\
РЕДАКТИРОВАНИЕ ЖУРНАЛА\
Команда update - вносит изменения в таблицу\n\
Синтаксис: /update day, "среда", 3\n\
где day-столбец, а среда его значение которое будет внесено,последнее значение - уникальное ID\n\
КАВЫЧКИ ОБЯЗАТЕЛЬНЫ',reply_markup = kbtr)

    # редактирование журнала тренировок
    @dp.message_handler(commands=['update'])
    async def gt_tren(message : types.Message):
        name_column = message.text.split(',')[0][8:]
        new_value = message.text.split(',')[1]
        rowid = message.text.split(',')[2]
        await message.answer(update_tren(name_column, new_value, rowid))

    # получение уникального айди
    @dp.message_handler(commands=['rowid'])
    async def gt_tren(message : types.Message):
        value = message.text.split(',')[0][7:]
        await bot.send_message(message.chat.id, get_rowid(value))

    #......................................................................................................................................
        
    # блок компаний

    @dp.message_handler(commands=['BYND'])
    async def info_BYND(message: types.Message):
        await message.reply('Beyond meat\nКомпания специализирующаяся на производстве растительного мяса.\n\
    В качестве сырья используется горох.\nВ 2019 компания вышла  на IPO с 25$ за акцию.\n\
    На территории США продукция Beyon meat используется в продуктах McDonald\'s и Burger King', reply_markup=ReplyKeyboardRemove())

    @dp.message_handler(commands=['EXEL'])
    async def info_EXEL(message: types.Message):
        await message.reply('Exelixis, Inc\nБиотех, специализирующийся на разработке лекарственых\n\
    препаратов от различных форм рака.\nОсновная молекула компании - кабозантиниб.\n\
    Сотрудничает со многими фармацептическими "монстрами".', reply_markup=ReplyKeyboardRemove())

    @dp.message_handler(commands=['MU'])
    async def info_MU(message: types.Message):
        await message.reply('Micron Technology, Inc\nИзготавливает полуппроводники(входит в ТОП 5 компаний)\
    , основная часть которых - различные виды памяти.', reply_markup=ReplyKeyboardRemove())


    executor.start_polling(dp, skip_updates=True, on_startup=print('Бот запущен'))


if __name__ == '__main__':
    main()
