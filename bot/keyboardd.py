from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# основная клавиатура
b1 = KeyboardButton('крипта')
b2 = KeyboardButton('погода')
b3 = KeyboardButton('фонда')
b4 = KeyboardButton('инфо о журнале')

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
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
b1 = KeyboardButton('инфо')
b2 = KeyboardButton('рынок')
b3 = KeyboardButton('назад')

kbf = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 
kbf.add(b1).insert(b2).add(b3)

# _______________________________________________________________________

# клавиатура раздела (команды) 'weatch'
b1 = KeyboardButton('Липецк')
b2 = KeyboardButton('Передать координаты', request_location=True)
b3 = KeyboardButton('назад')
kbw = ReplyKeyboardMarkup(resize_keyboard=True)
kbw.add(b1).add(b2).row(b3)

# ________________________________________________________________________
# клавиатура журнала тренировок
b1 = KeyboardButton('журнал')
b2 = KeyboardButton('добавить тренировку')
b3 = KeyboardButton('инфо о журнале')
b4 = KeyboardButton('назад')
kbtr = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kbtr.add(b1).insert(b2).add(b3).insert(b4)
# ________________________________________________________________________
# кнопка отмены
b1 = KeyboardButton('отмена')
cancelb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancelb.add(b1)