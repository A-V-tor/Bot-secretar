from telebot import types

# Кнопка возврата в главное меню
close_entries = types.InlineKeyboardButton(text="❌", callback_data="start")


""" Главная клавиатура. """
main_keyboard = types.InlineKeyboardMarkup()

market = types.InlineKeyboardButton(text="🎩 рынки", callback_data="market")
personal_finance = types.InlineKeyboardButton(
    text="✍ расходы", callback_data="personal_finance"
)
training = types.InlineKeyboardButton(text="🏃тренировки", callback_data="training")
news = types.InlineKeyboardButton(text="📰 новости", callback_data="news")
weight = types.InlineKeyboardButton(text="⚖ вес", callback_data="weight")
notes = types.InlineKeyboardButton(text="📃 заметки", callback_data="notes")

main_keyboard.add(market, personal_finance, training).add(news, weight, notes)


""" Клавиатура фондового рынка и крипты. """
market_keyboard = types.InlineKeyboardMarkup()

oil = types.InlineKeyboardButton(text="нефть/газ🛢", callback_data="oil_market")
rus = types.InlineKeyboardButton(text="рынок РФ😰", callback_data="rus_market")
crypto = types.InlineKeyboardButton(text="крипта⚡", callback_data="crypto_market")
favorites = types.InlineKeyboardButton(
    text="избранное🍀", callback_data="favorites_market"
)
finance = types.InlineKeyboardButton(text="банки🏦", callback_data="finance_market")
medical = types.InlineKeyboardButton(text="медицина🩺", callback_data="medical_market")
production = types.InlineKeyboardButton(
    text="производство🚨", callback_data="production_market"
)
technologies = types.InlineKeyboardButton(
    text="технологии⚛", callback_data="technologies_market"
)

market_keyboard.add(oil, rus, crypto, favorites).add(
    finance, medical, production, technologies
).add(close_entries)


""" Клавиатура ведения личных финансов. """
finance_keyboard = types.InlineKeyboardMarkup()

add_entries = types.InlineKeyboardButton(
    text="добавить запись", callback_data="add_entries"
)
update_entries = types.InlineKeyboardButton(
    text="редактировать", callback_data="update_entries"
)
get_entries = types.InlineKeyboardButton(text="баланс", callback_data="balance")

finance_keyboard.add(add_entries, update_entries).add(get_entries).add(close_entries)


""" Клавиатура сброса текушего состояния добавления записи расходов"""

current_state_keyboard = types.InlineKeyboardMarkup()

reset = types.InlineKeyboardButton(text="заново↩", callback_data="reset")
close_state_add_entries = types.InlineKeyboardButton(
    text="отменить запись ✘", callback_data="close-add-entries"
)

current_state_keyboard.add(reset, close_state_add_entries)


""" Клавиатура сброса текушего состояния изменения записи расходов"""

current_state_edit_keyboard = types.InlineKeyboardMarkup()

reset_edit = types.InlineKeyboardButton(text="заново↩", callback_data="reset-edit")

current_state_edit_keyboard.add(reset_edit, close_state_add_entries)


""" Клавиатура категорий записей личных финансов. """
categories_finance_keyboard = types.InlineKeyboardMarkup()

transport = types.InlineKeyboardButton(text="транспорт 🚕", callback_data="transport")
food = types.InlineKeyboardButton(text="еда 🍔", callback_data="food")
entertainment = types.InlineKeyboardButton(
    text="развлечения 🎉", callback_data="entertainment"
)
clothes = types.InlineKeyboardButton(text="одежда 🎽", callback_data="clothes")
present = types.InlineKeyboardButton(text="подарки 🎁", callback_data="present")
health = types.InlineKeyboardButton(text="здоровье 💉⚕", callback_data="health")
hobby = types.InlineKeyboardButton(text="хобби 💻", callback_data="hobby")
other = types.InlineKeyboardButton(text="прочее ⚒", callback_data="other")

categories_finance_keyboard.add(
    transport, food, entertainment, clothes, present, health, hobby, other
).add(close_state_add_entries)


""" Клавиатура категорий редактирования записей личных финансов. """
categories_edit_finance_keyboard = types.InlineKeyboardMarkup()

transport = types.InlineKeyboardButton(
    text="транспорт 🚕", callback_data="transport-edit"
)
food = types.InlineKeyboardButton(text="еда 🍔", callback_data="food-edit")
entertainment = types.InlineKeyboardButton(
    text="развлечения 🎉", callback_data="entertainment-edit"
)
clothes = types.InlineKeyboardButton(text="одежда 🎽", callback_data="clothes-edit")
present = types.InlineKeyboardButton(text="подарки 🎁", callback_data="present-edit")
health = types.InlineKeyboardButton(text="здоровье 💉⚕", callback_data="health-edit")
hobby = types.InlineKeyboardButton(text="хобби 💻", callback_data="hobby-edit")
other = types.InlineKeyboardButton(text="прочее ⚒", callback_data="other-edit")

categories_edit_finance_keyboard.add(
    transport, food, entertainment, clothes, present, health, hobby, other
).add(close_state_add_entries)


""" Клавиатура новостей. """
news_keyboard = types.InlineKeyboardMarkup()

news_keyboard.add(close_entries)