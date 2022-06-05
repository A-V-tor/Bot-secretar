#!/usr/bin/python3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from ScrepBot import function_screp ,screp_iter, lst
from Weather import get_weather
import json, string 
import aiogram.utils.markdown as fmt



bot = Bot(token= 'toc:en')
dp = Dispatcher(bot)


# отработка команды start
@dp.message_handler(commands=['start', 'старт'])
async def send_welcome(message: types.Message):
    await message.reply(f'Привет, {message.from_user.first_name} \U0001F464, я бот секретарь! \u270D\n\
жми /help или воспользуйся клавиатурой,\
чтобы подать мне команду!', reply_markup = kb)
    
    
# отработка команды help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply('\u2193  Доступные команды бота: \u2193\n\n\
/fonda - посмотреть текущие цены акций\n\n\
/info - информация по компаниям\n\n\
/weath - информация о погоде', reply_markup = kb )
    await message.delete()


# отработка команды fonda
@dp.message_handler(commands=['fonda'])
async def send_fonda(message: types.Message):
    await message.answer('Жди, собираю информацию... \u23F3')
    await message.reply(screp_iter(function_screp(lst)))
    await message.delete()


# отработка погоды
@dp.message_handler(commands=['weath'])
async def send_weath(message: types.Message):
    await message.reply(get_weather())
    await message.delete()
    

# отработка инфы о компаниях
@dp.message_handler(commands=['info'])
async def info_message(message : types.Message):
    message_text =f'Блок информации об представленых компаниях'
    await message.answer(message_text,reply_markup=kb2)
    

#......................................................................................................................................
    
# Блок компаний

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
            await message.reply(fmt.text(fmt.hbold('\u26A0 Мат запрещен! \u26A0')),parse_mode="HTML")
            await message.delete()
            
          
#обозначение кнопок и их команд
b1 = KeyboardButton('/info')
b2 = KeyboardButton('/weath')
b3 = KeyboardButton('/fonda')

kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True) 
kb.add(b1).insert(b2).add(b3)


# клавиатура с кнопками-компаниями
but1 = KeyboardButton('/BYND')
but2 = KeyboardButton('/EXEL')
but3 = KeyboardButton('/MU')
kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb2.add(but1, but2).insert(but3)



executor.start_polling(dp, skip_updates=True, on_startup=print('Бот запущен'))




