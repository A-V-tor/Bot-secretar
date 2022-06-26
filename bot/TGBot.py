#!/usr/bin/env python3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from bot.ScrepBot import function_screp, screp_iter, lst
from bot.Weather import get_weather
import json, string
import aiogram.utils.markdown as fmt
from bot.tkn import token_bot
from bot.keyboardd import kb, kb2, kbf, kbw


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
    /weath - информация о погоде', reply_markup = kb)
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


    #......................................................................................................................................    

    # обработка мата
    @dp.message_handler()
    async def sl_ban(message : types.Message):
        if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
            .intersection(set(json.load(open('cenz.json')))) != set():
                await message.reply(fmt.text(fmt.hbold('\u26A0 Мат запрещен! \u26A0')), parse_mode="HTML")
                await message.delete()

    executor.start_polling(dp, skip_updates=True, on_startup=print('Бот запущен'))


if __name__ == '__main__':
    main()
