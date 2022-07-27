
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# основная клавиатура
kb = InlineKeyboardMarkup(row_width=2)
b1 = InlineKeyboardButton(text = 'крипта', callback_data='crypto')
b2 = InlineKeyboardButton(text = 'погода', callback_data='weatch')
b3 = InlineKeyboardButton(text = 'фонда', callback_data='fonda')
b4 = InlineKeyboardButton(text = 'журнал  тренировок', callback_data='infotren')
kb.add(b1).insert(b2).add(b3).insert(b4)
# ________________________________________________________________________

# клавиатура информации о компаниях
but1 = KeyboardButton('/BYND')
but2 = KeyboardButton('/EXEL')
but3 = KeyboardButton('/MU')

kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb2.add(but1, but2).insert(but3)

# ________________________________________________________________________

# клавиатура раздела (команды) 'fonda'
kbf = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text = 'рынок', callback_data='market')
b2 = InlineKeyboardButton(text='info', callback_data='info')
b3 = InlineKeyboardButton(text='календарь', callback_data='calendar' )
b4 = InlineKeyboardButton(text='назад', callback_data='back')
kbf.add(b1).insert(b2).add(b3).insert(b4)
# _______________________________________________________________________

# клавиатура раздела (команды) 'weatch'
b1 = KeyboardButton('Липецк')
b2 = KeyboardButton('Передать координаты', request_location=True)
b3 = KeyboardButton('назад')
kbw = ReplyKeyboardMarkup(resize_keyboard=True)
kbw.add(b1).add(b2).row(b3)

# ________________________________________________________________________

# клавиатура журнала тренировок
#b1 = KeyboardButton('журнал')
#b2 = KeyboardButton('добавить тренировку')
#b3 = KeyboardButton('получить лимит записей')
#b4 = KeyboardButton('назад')
#b5 = KeyboardButton('получить запись')
##b6 = KeyboardButton('получить powid id')
#b7 = KeyboardButton('редактировать журнал')
#kbtr = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#kbtr.add(b1).insert(b2).add(b3).insert(b5).insert(b7).add(b4).insert(b6)

kbtr = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text='журнал', callback_data='журнал')
b2 = InlineKeyboardButton(text='получить лимит записей', callback_data='journal')
b3 = InlineKeyboardButton(text='получить запись', callback_data='needed')
b4 = InlineKeyboardButton(text='получить powid id', callback_data='rowid')
b5 = InlineKeyboardButton(text='редактировать журнал',callback_data='update')
b6 = InlineKeyboardButton(text='добавить тренировку', callback_data='tren')
kbtr.add(b1).insert(b2).insert(b3).add(b4).insert(b5).add(b6)
# ________________________________________________________________________

# ситуативные клавиатуры

# кнопка отмены
b1 = KeyboardButton('отмена')
back_but = KeyboardButton('назад')
cancelb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancelb.add(b1).insert(back_but)



# клавиатура для отработки выбора столбца
b1 = KeyboardButton('назад')
b2 = KeyboardButton('day')
b3 = KeyboardButton('biceps')
b4 = KeyboardButton('waist')
b5 = KeyboardButton('chest ')
b6 = KeyboardButton('triceps')
b7 = KeyboardButton('отмена')
kbrecord = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kbrecord.add(b2).insert(b3).add(b4).insert(b5).insert(b6).add(b7).insert(b1)

#клавиатура ввода дня недели
b1 = KeyboardButton("'Понедельник'")
b2 = KeyboardButton("'Вторник'")
b3 = KeyboardButton("'Среда'")
b4 = KeyboardButton("'Четверг'")
b5 = KeyboardButton("'Пятница'")
b6 = KeyboardButton("'Суббота'")
b7 = KeyboardButton("'Воскресенье'")
b8 = KeyboardButton('отмена')
kbday = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kbday.add(b1).insert(b2).insert(b3).add(b4).insert(b5).insert(b6).add(b7).insert(b8)

urlkb = InlineKeyboardMarkup()
urlbut = InlineKeyboardButton(text='button',url = 'https://mastergroosha.github.io/telegram-tutorial-2/buttons/')
inbut = InlineKeyboardButton(text = 'рынок', callback_data='рынок')
urlkb.add(urlbut).insert(inbut)