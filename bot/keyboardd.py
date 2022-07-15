
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
b3 = KeyboardButton('получить лимит записей')
b4 = KeyboardButton('назад')
b5 = KeyboardButton('получить запись')
b6 = KeyboardButton('получить powid id')
b7 = KeyboardButton('редактировать журнал')
kbtr = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kbtr.add(b1).insert(b2).add(b3).insert(b5).insert(b7).add(b4).insert(b6)

# ________________________________________________________________________

# ситуативные клавиатуры

# кнопка отмены
b1 = KeyboardButton('отмена')
cancelb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancelb.add(b1)

# клавиатура для отработки выбора столца
b1 = KeyboardButton('the_date')
b2 = KeyboardButton('day')
b3 = KeyboardButton('biceps')
b4 = KeyboardButton('waist')
b5 = KeyboardButton('chest ')
b6 = KeyboardButton('triceps')
b7 = KeyboardButton('отмена')
kbrecord = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kbrecord.add(b1).insert(b2).insert(b3).add(b4).insert(b5).insert(b6).add(b7)

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
