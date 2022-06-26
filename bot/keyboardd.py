from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


# основная клавиатура
b1 = KeyboardButton('/crypto')
b2 = KeyboardButton('/weath')
b3 = KeyboardButton('/fonda')

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb.add(b1).insert(b2).add(b3)
# ________________________________________________________________________

# клавиатура информации о компаниях
but1 = KeyboardButton('/BYND')
but2 = KeyboardButton('/EXEL')
but3 = KeyboardButton('/MU')

kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb2.add(but1, but2).insert(but3)

# ________________________________________________________________________

# клавиатура раздела (команды) 'fonda'
b1 = KeyboardButton('/info')
b2 = KeyboardButton('/market')
b3 = KeyboardButton('/отмена')

kbf = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 
kbf.add(b1).insert(b2).add(b3)

# _______________________________________________________________________

# клавиатура раздела (команды) 'weatch'
b1 = KeyboardButton('/Липецк')
b2 = KeyboardButton('Передать координаты', request_location=True)
b3 = KeyboardButton('/отмена')
kbw = ReplyKeyboardMarkup(resize_keyboard=True)
kbw.add(b1).add(b2).row(b3)
