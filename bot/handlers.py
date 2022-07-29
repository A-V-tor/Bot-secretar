#!/usr/bin/env python3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from bot.screpers import get_price_market, calendar_check, get_price_crypto,lst
from bot.weather import get_weather
from bot.tkn import token_bot, USER_ID
from bot.keyboardd import kb, kb2, kbf, kbw, kbtr, cancelb, kbrecord, kbday
from bot.baza import add_tren, get_workout_record, get_workout_limit_record, update_tren, get_rowid, get_sum_all_record_day
from datetime import date
import calendar
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from bot.loggs_bot import get_loggs


def main():
    storage = MemoryStorage()
    bot = Bot(token = token_bot)
    dp = Dispatcher(bot, storage=storage)
     

# _____________________________________________________________________________________________________________
    

                                       # БЛОК НАЧАЛА РАБОТЫ БОТА

    # отработка команды start
    @dp.message_handler(commands=['start', 'старт'])
    @dp.message_handler(Text(equals=['старт','start','Старт','Start']))
    async def send_welcome(message: types.Message):
        if message.from_user.id == USER_ID:
            await message.reply(f'Привет, {message.from_user.first_name} \U0001F464, я бот секретарь! \u270D\n\
    жми /help или воспользуйся клавиатурой,\
    чтобы подать мне команду!', reply_markup = kb)
        else:
            await message.reply('У Вас нет доступа!!!\U0001F5CB')
    
    
    # отработка команды help
    @dp.message_handler(commands=['help'])
    @dp.message_handler(Text(equals=['помощь','Помощь','Help','help','back','Back','назад','Назад']))
    async def send_help(message: types.Message):
        if message.from_user.id == USER_ID:
            await message.reply('\u2193  Доступные команды бота: \u2193\n\n\
    фонда - информация о фондовом рынке\n\n\
    крипта - информация по криптовалютам\n\n\
    погода - информация о погоде\n\n\
    ведение журнала тренировок -  информация о ведении журнала тренировок', reply_markup = kb)
            await message.delete()
        else:
            await message.reply('У Вас нет доступа!!!')
        
    @dp.message_handler(commands=['delit'])
    @dp.message_handler(Text(equals=['delkey','делит'],ignore_case=True))
    async def sa(message: types.Message):
        await message.answer('Ok',reply_markup=ReplyKeyboardRemove())
        
# _____________________________________________________________________________________________________________


                                        # БЛОК ФИНАНСОВ

    # отработка команды 'fonda' 
    @dp.callback_query_handler(text='fonda')
    async def in_test(callback: types.CallbackQuery):
        await callback.message.delete()
        await callback.message.answer('Выбери нужный раздел', reply_markup = kbf)
        

    # отработка команды market, отдает текущие цены
    @dp.callback_query_handler(text='market')
    async def in_test(callback: types.CallbackQuery):
        await callback.message.delete()
        await callback.message.answer('Жди, собираю информацию... \u23F3')
        await callback.message.answer(get_price_market(lst), parse_mode='HTML')
    

    # календарь отчетностей
    @dp.callback_query_handler(text='calendar')
    async def in_test(callback: types.CallbackQuery):
        await callback.message.delete()
        await callback.bot.send_photo(chat_id=callback.message.chat.id, photo=open('/Users/user/Documents/TG_bot/bot/image/calendar.jpg', 'rb'),caption = "<b>Попсовые отчетности на текущей недели!</b>",parse_mode='HTML')  

    @dp.callback_query_handler(text='back')
    async def in_test(callback: types.CallbackQuery):
        await callback.message.delete()
        await callback.message.answer('help',reply_markup = kb)
        

    # ....................................информация о компаниях и токенах.........................................

    # отработка инфы о компаниях    
    @dp.callback_query_handler(text='info')
    async def in_test(callback: types.CallbackQuery):
        await callback.message.answer('Блок информации об представленых компаниях\U0001F4AB', reply_markup=kb2)
    
    # отработка комаманды 'crypto'
    @dp.callback_query_handler(text='crypto')
    async def in_test(callback: types.CallbackQuery):
        await callback.message.answer('Жди, собираю информацию... \u23F3')
        await callback.message.answer(get_price_crypto(), parse_mode='HTML')
    


# _____________________________________________________________________________________________________________


                                        # БЛОК ПОГОДЫ

    # получение текущей погоды по координатам
    @dp.callback_query_handler(text='weatch')
    async def in_test(callback: types.CallbackQuery):
        await callback.message.answer('Отправьте свои координаты для определения погоды в вашем районе',reply_markup = kbw)
        @dp.message_handler(content_types=['location'])
        async def location(message: types.Message):
            lat = message.location.latitude
            lon = message.location.longitude
            await message.reply(f'широта:{lat}, долгота:{lon}')
            await message.reply(get_weather(lat, lon), reply_markup=ReplyKeyboardRemove())
    

    # получение текущей погоды в Липецке
    @dp.message_handler(commands=['Липецк'])
    @dp.message_handler(Text(equals=['Липецк погода','Липецк']))
    async def send_weath(message: types.Message):
        if message.from_user.id == USER_ID:
            await message.reply(get_weather(),reply_markup=ReplyKeyboardRemove())
        else:
            await message.reply('У Вас нет доступа!!!')
# _____________________________________________________________________________________________________________


                                         # БЛОК ЖУРНАЛА ТРЕНИРОВОК

    # .....................................добавление тренировки в БД...........................................
    class Tren(StatesGroup):
            '''класс для хранения переменых машины состояний при добавлении записи'''
            bic = State()
            waist = State()
            chest = State()
            tric = State()
    
    # обработчик запускающий добавления записи (начало работы машины состояний)
    @dp.message_handler(commands=['tren','трен','Трен'])
    @dp.message_handler(Text(equals=['добавить тренировку','Добавить тренировку']))
    async def gt_tren(message : types.Message):
        if message.from_user.id == USER_ID:
            await Tren().bic.set()
            await message.reply('Введи кол-во повторов на бицепс:\nЕсли повторов нет введи:  -\nОтмена - чтобы прекратить заполнение и выйти.', reply_markup=cancelb)
        else:
            await message.reply('У Вас нет доступа!!!')

    # Добавляем возможность отмены, если пользователь передумал заполнять
    @dp.message_handler(state='*', commands='отмена')
    @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
    async def cancel_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('Добавление записи отменено!', reply_markup = kb)
    
    @dp.message_handler(state=Tren.bic)
    async def process_biceps(message: types.Message, state: FSMContext):
        async with state.proxy() as data_state:
            data_state['bic'] = message.text
        await Tren.next()
        await message.reply('Введи кол-во повторов от пояса:\nЕсли повторов нет введи:  -', reply_markup=cancelb)

    @dp.message_handler(state=Tren.waist)
    async def process_waist(message: types.Message, state: FSMContext):
        async with state.proxy() as data_state:
            data_state['waist'] = message.text
        await Tren.next()
        await message.reply('Введи кол-во повторов от груди:\nЕсли повторов нет введи:  -', reply_markup=cancelb)

    @dp.message_handler(state=Tren.chest)
    async def process_chest(message: types.Message, state: FSMContext):
        async with state.proxy() as data_state:
            data_state['chest'] = message.text
        await Tren.next()
        await message.reply('Введи кол-во повторов на трицепс:\nЕсли повторов нет введи:  -', reply_markup=cancelb)
    
    @dp.message_handler(state=Tren.tric)
    async def process_triceps(message: types.Message, state: FSMContext):
        async with state.proxy() as data_state:
            data_state['tric'] = message.text
            data_ = date.today()
            day = calendar.day_name[data_.weekday()]
            bic = data_state['bic']
            waist = data_state['waist']
            chest = data_state['chest']
            tric = data_state['tric']
        await state.finish()
        await message.answer(add_tren(data_,day,bic,waist,chest,tric))
    
            
    @dp.callback_query_handler(text='tren',state=None)
    async def in_test(callback: types.CallbackQuery):
        await Tren.bic.set()
        await callback.message.answer('Введи кол-во повторов на бицепс:\nЕсли повторов нет введи:  -\nОтмена - чтобы прекратить заполнение и выйти.', reply_markup=cancelb)
        
      
    
    # ............................................................................................    
            
    # .................................вывод записей журнала......................................

    # получение журнала тренировок по заданым данным

    class Record(StatesGroup):
        '''класс для хранения переменых машины состояний при получении записи'''
        tabl = State()
        data = State()

    @dp.message_handler(commands=['needed'])
    @dp.message_handler(Text(equals=['Получить запись журнала','получить запись','получить запись журнала', 'нужна запись','запись журнала','Запись журнала']))
    async def gt_tren(message : types.Message):
        if message.from_user.id == USER_ID:
            await Record.tabl.set()
            await message.reply('Введи название стобца: \n\nthe_date - дата\nday - день недели\nbiceps - бицепс\nwaist - пояс\nchest - грудь\ntriceps - трицепс',reply_markup=kbrecord)
        else:
            await message.reply('У Вас нет доступа!!!')

    @dp.message_handler(state=Record.tabl)
    async def process_biceps(message: types.Message, state: FSMContext):
        if message.text  in ['the_date','day','biceps','waist','chest','triceps']:
            async with state.proxy() as data_state:
                data_state['tabl'] = message.text
            await Record.next()
            await message.reply('Укажи нужное значение: \n\nЕсли столбцем выбран day то день недели вводить в кавычках: "Вторник"\n\nФормат даты: 2022-07-14', reply_markup=kbday)
        else:
            await message.reply('Неверное значение столбца')


    @dp.message_handler(state=Record.data)
    async def process_triceps(message: types.Message, state: FSMContext):
        async with state.proxy() as data_state:
            data_state['data'] = message.text
            data = data_state['data']
            tabl = data_state['tabl']
        await state.finish()
        try:
            await bot.send_message(message.chat.id,f'{get_workout_record(tabl, data)}', reply_markup=kbtr,parse_mode='HTML')
        except:
            await message.answer('Некорректный ввод данных.\n\nПРОВЕРЬ КАВЫЧКИ\n                ¯\_(ツ)_/¯')


    @dp.callback_query_handler(text='needed',state=None)
    async def in_test(callback: types.CallbackQuery):
        await Record.tabl.set()
        await callback.message.answer('Введи название стобца: \n\nthe_date - дата\nday - день недели\nbiceps - бицепс\nwaist - пояс\nchest - грудь\ntriceps - трицепс',reply_markup=kbrecord)


    # получение журнала тренировок лимитированое кол-во записей(показывается последние)
    class Journal(StatesGroup):
        item = State()
    
    @dp.message_handler(commands=['journal'])
    @dp.message_handler(Text(equals=['задать лимит записей','получить лимит записей','получить лимит', 'нужен лимит записей','лимит журнала']))
    async def gt_jornal_limit(message : types.Message):
        if message.from_user.id == USER_ID:
            await Journal.item.set()
            await message.answer('Введи задай нужное кол-во записей для вывода:')
        else:
            await message.reply('У Вас нет доступа!!!')
    
    @dp.message_handler(state=Journal.item)
    async def process_journal(message: types.Message, state: FSMContext):
        async with state.proxy() as data_state:
            data_state['item'] = message.text
        await state.finish()
        item = data_state['item']
        await message.answer(get_workout_limit_record(item),parse_mode='HTML')
    
    @dp.callback_query_handler(text='journal',state=None)
    async def in_test(callback: types.CallbackQuery):
        await Journal.item.set()
        await callback.message.answer('Введи задай нужное кол-во записей для вывода:')
    
    

    # получение журнала с записями
    @dp.message_handler(commands=['журнал'])
    @dp.message_handler(Text(equals=['журнал','Журнал']))
    async def gt_journal(message : types.Message):
        if message.from_user.id == USER_ID:
            await bot.send_message(message.chat.id, get_sum_all_record_day(),parse_mode='HTML',reply_markup='')
        else:
            await message.reply('У Вас нет доступа!!!')
    
    @dp.callback_query_handler(text='журнал')
    async def in_test(callback: types.CallbackQuery):
        await callback.message.delete()
        await callback.message.answer('журнал тренировок')
        await callback.message.bot.send_message(callback.message.chat.id, get_sum_all_record_day(),parse_mode='HTML',reply_markup='')
    
    # получение уникального айди

    class Rowid(StatesGroup):
        value = State()
    

    @dp.message_handler(commands=['rowid'])
    @dp.message_handler(Text(equals=['получить ровид ID','получить айди', 'получить powid id']))
    async def gt_rowid(message : types.Message):
        if message.from_user.id == USER_ID:
            await Rowid.value.set()
            await message.answer('Задай дату записи в формате: "2022-07-14"\n\nКАВЫЧКИ ОБЯЗАТЕЛЬНЫ! ')
        else:
            await message.reply('У Вас нет доступа!!!')
    
    @dp.message_handler(state=Rowid.value)
    async def process_rowid(message: types.Message, state: FSMContext):
        async with state.proxy() as data_state:
            data_state['value'] = message.text
        await state.finish()
        value = data_state['value']
        await bot.send_message(message.chat.id, get_rowid(value))
    
    @dp.callback_query_handler(text='rowid',state=None)
    async def in_test(callback: types.CallbackQuery):
        await Rowid.value.set()
        await callback.message.answer('Задай дату записи в формате: "2022-07-14"\n\nКАВЫЧКИ ОБЯЗАТЕЛЬНЫ! ')
    


    #........................................редактирование журнала................................


    # редактирование журнала тренировок

    class Update_journal(StatesGroup):
        name_column = State()
        new_value = State()
        rowid = State()

    @dp.message_handler(commands=['update'])
    @dp.message_handler(Text(equals=['редактировать журнал']))
    async def update_journal(message : types.Message):
        if message.from_user.id == USER_ID:
            await Update_journal.name_column.set()
            await message.answer('Введи название стобца: \n\nday - день недели\nbiceps - бицепс\nwaist - пояс\nchest - грудь\ntriceps - трицепс',reply_markup=kbrecord)
        else:
            await message.reply('У Вас нет доступа!!!')


    @dp.message_handler(state=Update_journal.name_column)
    async def process_rowid(message: types.Message, state: FSMContext):
        async with state.proxy() as data_state:
            data_state['name_column'] = message.text
        await Update_journal.next()
        await message.reply('Введи новое значение для записи: ', reply_markup=kbday)
    
    @dp.message_handler(state=Update_journal.new_value)
    async def process_rowid(message: types.Message, state: FSMContext):
        async with state.proxy() as data_state:
            data_state['new_value'] = message.text
        await Update_journal.next()
        await message.reply('Введи rowid ID записи : ', reply_markup=cancelb)
    
    @dp.message_handler(state=Update_journal.rowid)
    async def process_rowid(message: types.Message, state: FSMContext):
        async with state.proxy() as data_state:
            data_state['rowid'] = message.text
        await state.finish()
        name_column = data_state['name_column']
        new_value = data_state['new_value']
        rowid = data_state['rowid']
        await message.reply(update_tren(name_column, new_value, rowid))
    
    @dp.callback_query_handler(text='update',state=None)
    async def in_test(callback: types.CallbackQuery):
        await Update_journal.name_column.set()
        await callback.message.answer('Введи название стобца: \n\nday - день недели\nbiceps - бицепс\nwaist - пояс\nchest - грудь\ntriceps - трицепс',reply_markup=kbrecord)

        


    #........................................информация о работе с журналом........................

    # получение информации  о работе с журналом тренировок
    @dp.callback_query_handler(text='infotren')
    async def in_test(callback: types.CallbackQuery):
        await callback.message.delete()
        await callback.message.answer('\
КОМАНДА журнал :\nПоказывает  записи тренировок.\n\
___________________________________________\n\n\
КОМАНДА добавить тренировку:\nдобавляет новую запись.\n\
___________________________________________\n\n\
КОМАНДА лимит записей:\nПоказывает заданное кол-во записей от начала ведения журнала.\n\
___________________________________________\n\n\
КОМАНДА получить запись:\nВыдает нужную запись.\n\
___________________________________________\n\n\
КОМАНДА редактировать журнал: Редактирование нужной записи.',reply_markup = kbtr)
# _____________________________________________________________________________________________________________      
    calendar_check()
    get_loggs()
    executor.start_polling(dp, skip_updates=True, on_startup=print('Бот запущен'))


if __name__ == '__main__':
    main()
