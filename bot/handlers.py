import os
import time
import calendar, locale
import logging
import datetime
from collections import deque
from sqlalchemy import text, select
from flask import (
    request,
    abort,
    session,
    flash,
    redirect,
    url_for,
    render_template,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import telebot
from telebot import types
from dotenv import find_dotenv, load_dotenv
from admin.models import AdminUser
from finance.markets import (
    get_price_market_for_america,
    get_price_market_for_russia,
    lst_favorites,
    lst_finance,
    lst_medical,
    lst_production,
    lst_technologies,
)
from finance.crypto import get_crypto
from finance.other import get_product

from . import server, db, babel
from .other import (
    get_current_state,
    set_state,
    get_current_state_edit,
    set_state_edit,
    set_state_workout,
    get_current_state_weight,
    set_state_weight,
    get_current_state_notes,
    set_state_notes,
    get_current_date,
    get_current_state_workout,
    get_number_month,
    get_str_month,
    get_current_state_nutrition,
    set_state_nutrition,
    States,
    StatesEdit,
    StatesWeight,
    StatesNotes,
    StatesWorkout,
    StatesNutrition,
)
from .keyboards import (
    main_keyboard,
    market_keyboard,
    finance_keyboard,
    categories_finance_keyboard,
    current_state_keyboard,
    categories_edit_finance_keyboard,
    current_state_edit_keyboard,
    news_keyboard,
    notes_keyboard,
    piligrim__keyboard,
    trein_keyboard,
    nutrition_keyboard,
    nutrition_keyboard_piligrim,
)
from .models import MyWeight, MyNotes, MyWorkouts, MyNutrition
from finance.models import CurrentBalance
from news.news import get_news
from news.weather import get_current_weather


load_dotenv(find_dotenv())
login_manager = LoginManager(server)
login_manager.init_app(server)
login_manager.login_view = 'index_autorization'
bot = telebot.TeleBot(os.getenv('token'))

log_file = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'file.log')
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler(log_file))


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))


# константы обработки добавления записи расходов
SELECT_CATEGORY = None
MONEY_VALUE = None
TEXT_CATEGORY = None


# хранение id сообщений для чистки чата
DEL_MESSEGE_ID = []

#  хранение состояния заметок при их обходе
STATE_NOTE = {}

#  хранение состояния записей БЖУ
STATE_NUTRITION = {}

# хранение списка записей бжу
LIST_ENTRIES = {}


@bot.callback_query_handler(func=lambda callback: callback.data == 'start')
@bot.message_handler(commands=['start'])
def start_chat(message=None, callback=None):
    msg = 'Главное меню'
    if message:
        [bot.delete_message(message.from_user.id, id) for id in DEL_MESSEGE_ID]
        DEL_MESSEGE_ID.clear()
        item = bot.send_message(
            message.from_user.id, msg, reply_markup=main_keyboard
        )
        STATE_NOTE = {}
        DEL_MESSEGE_ID.append(item.message_id)
    else:
        [
            bot.delete_message(callback.message.chat.id, id)
            for id in DEL_MESSEGE_ID
        ]
        DEL_MESSEGE_ID.clear()
        item = bot.send_message(
            callback.message.chat.id, msg, reply_markup=main_keyboard
        )
        STATE_NOTE = {}
        DEL_MESSEGE_ID.append(item.message_id)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         ОБРАБОТКА  КЛАВИАТУР
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'reset-nutrition'
)
def reset_state_nutrition(callback):
    """Перезагрузка текущего состояния записи БЖУ."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id,
        'Что ж, начнём по-новой. БЕЛКИ: ',
        reply_markup=nutrition_keyboard,
    )
    set_state_nutrition(StatesNutrition.PROTEINS.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'cancel-nutrition'
)
def cancel_add_nutrition(callback):
    """Отмена добавления запсиси БЖУ."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id,
        'ОТМЕНЕНО',
        reply_markup=nutrition_keyboard,
    )
    set_state_nutrition(StatesNutrition.START.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'nutrition')
def get_nutrition_table(callback):
    """Получение клавиатуры ведения таблицы"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    keyboard = types.InlineKeyboardMarkup()
    but_add = types.InlineKeyboardButton(
        text='Добавить запись', callback_data='add-nutrition'
    )
    but_edit = types.InlineKeyboardButton(
        text='Редактировать запись', callback_data='edit-nutrition'
    )
    but_show = types.InlineKeyboardButton(
        text='Просмотр записей', callback_data='show-nutrition'
    )
    cur_balance = types.InlineKeyboardButton(
        text='сводка', callback_data='balance-nutrition'
    )
    close = types.InlineKeyboardButton(text='❌', callback_data='start')
    keyboard.add(but_add, but_edit).add(but_show, cur_balance).add(close)

    item = bot.send_message(
        callback.message.chat.id,
        'таблица БЖУ',
        parse_mode='HTML',
        reply_markup=keyboard,
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'training')
def get_training_keyboard(callback):
    """Получение клавиатуры с кнопками по тренировкам."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id, 'ТРЕНИРОВКИ', reply_markup=trein_keyboard
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'notes')
def get_notes_keyboard(callback):
    """Получение клавиатуры с кнопками по заметкам."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id, 'ЗАМЕТКИ', reply_markup=notes_keyboard
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'weight')
def make_entries_weight_keyboard(callback):
    """Получение клавиатуры записи веса в журнал"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(callback.message.chat.id, 'Сколько сегодня ?')
    set_state_weight(StatesWeight.START.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'market')
def get_market_keyboard(callback):
    """Получение клавиатуры с кнопками по рынкам."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id, 'Рынок акций', reply_markup=market_keyboard
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'personal_finance'
)
def get_finance_keyboard(callback):
    """Получение клавиатуры ведения личных финансов."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id,
        'Журнал расходов',
        reply_markup=finance_keyboard,
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'add_entries'
)
def get_categories_finance_keyboard(callback):
    """Получение клавиатуры категорий записей личных финансов."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id,
        'Выбор категории для записи',
        reply_markup=categories_finance_keyboard,
    )
    set_state(States.ENTER_CATEGORY.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'update_entries'
)
def get_categories_edit_finance_keyboard(callback):
    """Получение клавиатуры редактирования записей личных финансов."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id,
        'Выбор категории для редактирования',
        reply_markup=categories_edit_finance_keyboard,
    )
    set_state_edit(StatesEdit.ENTER_CATEGORY_EDIT.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'reset')
def reset_state(callback):
    """Перезагрузка текущего состояния записи расходов."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id,
        'Что ж, начнём по-новой. Выбор категории',
        reply_markup=categories_finance_keyboard,
    )
    set_state(States.ENTER_CATEGORY.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'reset-edit'
)
def reset_state_edit(callback):
    """Перезагрузка текущего состояния изменения расходов."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id,
        'Что ж, начнём по-новой. Выбор категории',
        reply_markup=categories_edit_finance_keyboard,
    )
    set_state_edit(StatesEdit.ENTER_CATEGORY_EDIT.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'close-add-entries'
)
def close_state(callback):
    """Отмена текущего состояния записи расходов."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id, 'Финансы', reply_markup=finance_keyboard
    )
    set_state(States.START.value)
    set_state_edit(StatesEdit.START.value)
    DEL_MESSEGE_ID.append(item.message_id)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         НОВОСТИ
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


@bot.callback_query_handler(func=lambda callback: callback.data == 'news')
def news(callback):
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    item = bot.send_message(
        callback.message.chat.id,
        get_news(),
        reply_markup=news_keyboard,
        parse_mode='HTML',
    )
    DEL_MESSEGE_ID.append(item.message_id)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         ЗАМЕТКИ
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


@bot.callback_query_handler(func=lambda callback: callback.data == 'add-note')
def add_note_start(callback):
    """Старт машины состояний по добавлению заметки в базу данных"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    msg = 'Ввести текст заметки: '
    item = bot.send_message(
        callback.message.chat.id,
        msg,
        reply_markup=news_keyboard,
        parse_mode='HTML',
    )
    set_state_notes(StatesNotes.START.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.message_handler(
    func=lambda message: get_current_state_notes() == StatesNotes.START.value
)
def add_note_end(message):
    """Добавлению заметки в базу данных или обработка исключений в случае неудачи"""
    try:
        text_note = message.text
        new_note = MyNotes(note=text_note)
        db.session.add(new_note)
        db.session.commit()
        msg = 'Запись сделана ⚡'
    except Exception:
        msg = '⚠ что-то пошло не так! ⚠'
    item = bot.send_message(message.chat.id, msg)
    DEL_MESSEGE_ID.append(item.message_id)
    set_state(StatesNotes.END.value)


@bot.callback_query_handler(func=lambda callback: callback.data == 'show-note')
def show_note(callback):
    """Показ заметки"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data_notes = MyNotes.query.filter_by().all()
    if data_notes:
        notes = deque(
            [(i.date.strftime('%Y-%m-%d'), i.note) for i in data_notes]
        )
        STATE_NOTE['notes'] = notes
        msg = f'Заметка от <b>{notes[0][0]}</b>\n <i>{notes[0][1]}</i>'
        item = bot.send_message(
            callback.message.chat.id,
            msg,
            reply_markup=piligrim__keyboard,
            parse_mode='HTML',
        )
    else:
        msg = 'нет заметок'
        item = bot.send_message(
            callback.message.chat.id, msg, parse_mode='HTML'
        )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'next-note')
def show_next_note(callback):
    """Проход по заметкам вперед"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    try:
        notes = STATE_NOTE['notes']
        notes.rotate(1)
        current_note = notes[0]
        msg = f'Заметка от {current_note[0]}\n {current_note[1]}'
        item = bot.send_message(
            callback.message.chat.id,
            msg,
            reply_markup=piligrim__keyboard,
            parse_mode='HTML',
        )
    except Exception:
        msg = 'нет доступых записей'
        item = bot.send_message(
            callback.message.chat.id, msg, parse_mode='HTML'
        )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'back-note')
def show_back_note(callback):
    """Проход по заметкам назад"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    try:
        notes = STATE_NOTE['notes']
        notes.rotate(-1)
        current_note = notes[0]
        msg = f'Заметка от {current_note[0]}\n {current_note[1]}'
        item = bot.send_message(
            callback.message.chat.id,
            msg,
            reply_markup=piligrim__keyboard,
            parse_mode='HTML',
        )
    except Exception:
        msg = 'нет доступых записей'
        item = bot.send_message(
            callback.message.chat.id, msg, parse_mode='HTML'
        )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'del-note')
def show_del_note(callback):
    """Удаление заметки"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    notes = STATE_NOTE['notes']
    current_note = notes[0]
    del_note = MyNotes.query.filter_by(note=notes[0][1]).first()
    if del_note:
        db.session.delete(del_note)
        db.session.commit()
        msg = f'Заметка от {current_note[0]}\n {current_note[1]}\n\n Удалена'
        data_notes = MyNotes.query.filter_by().all()
        if len(data_notes) > 0:
            notes = deque(
                [(i.date.strftime('%Y-%m-%d'), i.note) for i in data_notes]
            )
            STATE_NOTE['notes'] = notes
        else:
            STATE_NOTE['notes'] = None
    else:
        msg = 'пусто'
    item = bot.send_message(
        callback.message.chat.id,
        msg,
        reply_markup=piligrim__keyboard,
        parse_mode='HTML',
    )
    DEL_MESSEGE_ID.append(item.message_id)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         ЗАПИСЬ     ВЕСА
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


@bot.message_handler(
    func=lambda message: get_current_state_weight() == StatesWeight.START.value
)
def change_weight(message):
    entries = MyWeight.query.filter_by().order_by(MyWeight.date.desc()).first()
    if entries is None or entries.date.strftime(
        '%Y-%m-%d'
    ) < datetime.datetime.now().strftime('%Y-%m-%d'):
        try:
            weight = message.text
            data_weight = MyWeight(value=weight)
            db.session.add(data_weight)
            db.session.commit()
            if float(weight) > 85:
                data_msg = 'Стоит подумать о диете...'
            else:
                data_msg = ' ...'
            item = bot.send_message(
                message.chat.id,
                f'Записано, текущий вес - {weight} кг\n\n{data_msg}',
            )
        except Exception:
            item = bot.send_message(
                message.chat.id, f"{'не корректный ввод!'}"
            )
    else:
        item = bot.send_message(
            message.chat.id, f'Запись на сегодня уже есть!!!'
        )
    set_state(StatesWeight.END.value)
    DEL_MESSEGE_ID.append(item.message_id)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         ОБРАБОТКА  ВЕДЕНИЯ ЗАПИСЕЙ РАСХОДОВ
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


@bot.callback_query_handler(func=lambda callback: callback.data == 'balance')
def get_my_current_balance(callback):
    """Текуший баланс расходов."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    entries = (
        CurrentBalance.query.filter_by()
        .order_by(CurrentBalance.date.desc())
        .first()
    )

    if entries is None or entries.date.strftime(
        '%Y-%m-%d'
    ) < datetime.datetime.now().strftime('%Y-%m-%d'):
        msg = 'НЕТ данных на сегодня!'
    else:
        msg = entries.get_balance()
    item = bot.send_message(
        callback.message.chat.id,
        msg,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: get_current_state_edit()
    == StatesEdit.ENTER_CATEGORY_EDIT.value
)
def change_entries(callback):
    """Редактирование записи."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    global TEXT_CATEGORY
    if callback.data == 'transport-edit':
        TEXT_CATEGORY = '🚕 ТРАНСПОРТ 🚕'
    if callback.data == 'food-edit':
        TEXT_CATEGORY = '🍔 ЕДА 🍔'
    if callback.data == 'entertainment-edit':
        TEXT_CATEGORY = '🎉 РАЗВЛЕЧЕНИЯ🎉 '
    if callback.data == 'clothes-edit':
        TEXT_CATEGORY = '🎽 ОДЕЖДА 🎽'
    if callback.data == 'present-edit':
        TEXT_CATEGORY = '🎁 ПОДАРКИ 🎁'
    if callback.data == 'health-edit':
        TEXT_CATEGORY = '💉⚕ ЗДОРОВЬЕ ⚕💉'
    if callback.data == 'hobby-edit':
        TEXT_CATEGORY = '💻 ХОББИ 💻'
    if callback.data == 'other-edit':
        TEXT_CATEGORY = '⚒ ПРОЧЕЕ ⚒'

    global SELECT_CATEGORY
    SELECT_CATEGORY = callback.data
    msg = f'Выбрана категория {TEXT_CATEGORY}\nИзменить значение на: '
    item = bot.send_message(
        callback.message.chat.id, msg, reply_markup=current_state_edit_keyboard
    )
    set_state_edit(StatesEdit.ENTER_MONEY_EDIT.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.message_handler(
    func=lambda message: get_current_state_edit()
    == StatesEdit.ENTER_MONEY_EDIT.value
)
def change_money(message):
    """Добавлении суммы изменения"""
    [bot.delete_message(message.from_user.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    msg = message.text
    global SELECT_CATEGORY
    global TEXT_CATEGORY
    MONEY_VALUE = int(msg)
    entries = CurrentBalance.query.order_by(CurrentBalance.date.desc()).first()

    # если записи на текущий день нет,информирование сообщением
    if entries is None or entries.date.strftime(
        '%Y-%m-%d'
    ) < datetime.datetime.now().strftime('%Y-%m-%d'):
        msg = 'НЕТ данных на сегодня!'
        bot.send_message(message.chat.id, msg)

    # если запись за текущий день найдена, то в нее вносятся изменения
    else:
        setattr(entries, SELECT_CATEGORY[:-5], MONEY_VALUE)
        db.session.commit()
        item = bot.send_message(
            message.chat.id,
            f'Значение категория: {TEXT_CATEGORY}\nИзменена на: {MONEY_VALUE}',
            reply_markup=main_keyboard,
        )
    set_state_edit(StatesEdit.START.value)
    SELECT_CATEGORY = None
    MONEY_VALUE = None
    TEXT_CATEGORY = None
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: get_current_state() == States.ENTER_CATEGORY.value
)
def add_entries(callback):
    """Выбор категории расходов для записи в базу данных."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    global TEXT_CATEGORY
    if callback.data == 'transport':
        TEXT_CATEGORY = '🚕 ТРАНСПОРТ 🚕'
    if callback.data == 'food':
        TEXT_CATEGORY = '🍔 ЕДА 🍔'
    if callback.data == 'entertainment':
        TEXT_CATEGORY = '🎉 РАЗВЛЕЧЕНИЯ 🎉 '
    if callback.data == 'clothes':
        TEXT_CATEGORY = '🎽 ОДЕЖДА 🎽'
    if callback.data == 'present':
        TEXT_CATEGORY = '🎁 ПОДАРКИ 🎁'
    if callback.data == 'health':
        TEXT_CATEGORY = '💉⚕ ЗДОРОВЬЕ ⚕💉'
    if callback.data == 'hobby':
        TEXT_CATEGORY = '💻 ХОББИ 💻'
    if callback.data == 'other':
        TEXT_CATEGORY = '⚒ ПРОЧЕЕ ⚒'

    global SELECT_CATEGORY
    SELECT_CATEGORY = callback.data
    msg = f'Выбрана категория: {TEXT_CATEGORY}\nПотраченно: '
    item = bot.send_message(
        callback.message.chat.id, msg, reply_markup=current_state_keyboard
    )
    set_state(States.ENTER_MONEY.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.message_handler(
    func=lambda message: get_current_state() == States.ENTER_MONEY.value
)
def spend_money(message):
    """Добавлении суммы расходов"""
    [bot.delete_message(message.from_user.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    msg = message.text
    global SELECT_CATEGORY
    global TEXT_CATEGORY
    try:
        MONEY_VALUE = int(msg)
        entries = CurrentBalance.query.order_by(
            CurrentBalance.date.desc()
        ).first()

        # если записи на текущий день нет, то она создается, а затем вносятся изменения
        if entries is None or entries.date.strftime(
            '%Y-%m-%d'
        ) < datetime.datetime.now().strftime('%Y-%m-%d'):
            new_entries = CurrentBalance()
            db.session.add(new_entries)
            db.session.commit()
            entries = CurrentBalance.query.order_by(
                CurrentBalance.date.desc()
            ).first()
            setattr(entries, SELECT_CATEGORY, MONEY_VALUE)
            msg = f'Добалена новая запись\nКатегория: {TEXT_CATEGORY}\n Расход: {MONEY_VALUE}'

        # если запись за текущий день найдена, то в нее вносятся изменения
        else:
            value = getattr(entries, SELECT_CATEGORY) + MONEY_VALUE
            setattr(entries, SELECT_CATEGORY, value)
            msg = f'Категория: {TEXT_CATEGORY}\n Расход: {MONEY_VALUE}'
        db.session.commit()
        item = bot.send_message(
            message.chat.id, msg, reply_markup=main_keyboard
        )
    except Exception:
        msg = 'Что-то пошло не так!\n\nВвод только целого числа!!!'
        item = bot.send_message(
            message.chat.id, msg, reply_markup=main_keyboard
        )
    set_state(States.START.value)
    SELECT_CATEGORY = None
    MONEY_VALUE = None
    TEXT_CATEGORY = None
    DEL_MESSEGE_ID.append(item.message_id)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         ОБРАБОТКА  РЫНКОВ АКЦИЙ, КРИПТЫ И Т. Д.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'crypto_market'
)
def get_market_crypto(callback):
    """Криптовалюта."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = get_crypto()
    bot.send_message(
        callback.message.chat.id,
        data,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'oil_market'
)
def get_oil(callback):
    """Цена фьючерсов нефти и газа."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = get_product()
    bot.send_message(
        callback.message.chat.id,
        data,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'rus_market'
)
def get_market_rus(callback):
    """Цены акций российских компаний."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = get_price_market_for_russia()
    bot.send_message(
        callback.message.chat.id,
        data,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'favorites_market'
)
def get_market_favorites(callback):
    """Цены избранных акций."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = get_price_market_for_america(lst_favorites)
    bot.send_message(
        callback.message.chat.id,
        data,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'finance_market'
)
def get_market_finance(callback):
    """Цены на акции финансового сектора."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = get_price_market_for_america(lst_finance)
    bot.send_message(
        callback.message.chat.id,
        data,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'medical_market'
)
def get_market_medical(callback):
    """Цены на акции медецинского сектора."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = get_price_market_for_america(lst_medical)
    bot.send_message(
        callback.message.chat.id,
        data,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'production_market'
)
def get_market_production(callback):
    """Цены на акции производственного/промышленного сектора."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = get_price_market_for_america(lst_production)
    bot.send_message(
        callback.message.chat.id,
        data,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'technologies_market'
)
def get_market_technologies(callback):
    """Цены на акции технологического сектора."""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = get_price_market_for_america(lst_technologies)
    bot.send_message(
        callback.message.chat.id,
        data,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         ОБРАБОТКА  ВЕДЕНИЯ ЗАПИСЕЙ ТРЕНИРОВОК
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@bot.callback_query_handler(func=lambda callback: callback.data == 'add-trein')
def add_workout(callback):
    """Добавление записи тренировки"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    msg = 'Запиши нужные данные'
    item = bot.send_message(callback.message.chat.id, msg)
    DEL_MESSEGE_ID.append(item.message_id)
    set_state_workout(StatesWorkout.START.value)


@bot.message_handler(
    func=lambda message: get_current_state_workout()
    == StatesWorkout.START.value
)
def data_workout(message):
    """Ввод данных тренировки"""
    msg = message.text
    new_workout = MyWorkouts(entries=msg)
    db.session.add(new_workout)
    db.session.commit()
    item = bot.send_message(
        message.chat.id,
        f'ДОБАВЛЕНА ТРЕНИРОВКА\n {msg}',
        reply_markup=main_keyboard,
    )
    DEL_MESSEGE_ID.append(item.message_id)
    set_state(StatesWorkout.END.value)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'show-trein'
)
def show_workout(callback):
    """Просмотр тренировок в календаре"""

    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    chat_id = callback.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 7
    lst_but = []

    cl = calendar.TextCalendar(firstweekday=0)
    year, month = get_current_date(datetime.datetime.now().strftime('%Y,%m'))

    all_date = [
        i
        for i in db.engine.execute(
            text(
                'SELECT strftime("%Y-%m-%d", date) FROM myworkout GROUP BY date'
            )
        )
    ]
    lst_date = []
    for i in all_date:
        lst_date.append(i[0])

    # множество дат тренировок
    ready_date = set(lst_date)
    # список дней тренировок для последубщего сравнения
    data_num = [
        int(i.split('-')[2])
        for i in ready_date
        if i[:4] == str(year) and int(i[5:7]) == month
    ]

    for i in cl.itermonthdays(year, month):
        # итерация по текущему месяцу и создания кнопки с числом месяца или отображением записи трениновки
        if i != 0:
            if i in data_num:
                lst_but.append(
                    types.InlineKeyboardButton(
                        '💪', callback_data=f'workout_{i}_{month}_{year}'
                    )
                )
            else:
                lst_but.append(
                    types.InlineKeyboardButton(
                        i, callback_data=f'workout_{i}_{month}_{year}'
                    )
                )
        else:
            lst_but.append(
                types.InlineKeyboardButton(
                    ' ', callback_data=f'workout_{i}_{month}_{year}'
                )
            )

    # добавление кнопок в клавиатуру
    keyboard.add(
        types.InlineKeyboardButton('Пн', callback_data='_'),
        types.InlineKeyboardButton('Вт', callback_data='_'),
        types.InlineKeyboardButton('Ср', callback_data='_'),
        types.InlineKeyboardButton('Чт', callback_data='_'),
        types.InlineKeyboardButton('Пт', callback_data='_'),
        types.InlineKeyboardButton('Сб', callback_data='_'),
        types.InlineKeyboardButton('Вс', callback_data='_'),
    )
    keyboard.add(*lst_but)
    month = get_number_month(month)

    keyboard.add(
        types.InlineKeyboardButton('назад', callback_data=f'-{month} {year}'),
        types.InlineKeyboardButton('вперед', callback_data=f'+{month} {year}'),
    )
    keyboard.add(
        types.InlineKeyboardButton(text='❌', callback_data='start'),
    )
    item = bot.send_message(
        chat_id, f'{month} {year}', reply_markup=keyboard, parse_mode='HTML'
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(lambda callback: callback.data.startswith('-'))
def calendar_back(callback):
    """Проход по календарю назад"""

    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    chat_id = callback.message.chat.id
    data_date = []

    for i in callback.data[1:].split(' '):
        data_date.append(i)

    num_value_month = get_str_month(data_date[0])
    month = num_value_month - 1
    year = int(data_date[1])

    if month == 0:
        month = 12
        year -= 1

    lst_date = [
        i[0]
        for i in db.engine.execute(
            text(
                'SELECT strftime("%Y-%m-%d", date) FROM myworkout GROUP BY date'
            )
        )
    ]

    # множество дат тренировок
    ready_date = set(lst_date)
    # список дней тренировок для последубщего сравнения
    data_num = [
        int(i.split('-')[2])
        for i in ready_date
        if i[:4] == str(year) and int(i[5:7]) == month
    ]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 7
    lst_but = []

    cl = calendar.TextCalendar(firstweekday=0)

    for i in cl.itermonthdays(year, month):
        # итерация по текущему месяцу и создания кнопки с числом месяца
        if i != 0:
            if i in data_num:
                lst_but.append(
                    types.InlineKeyboardButton(
                        '💪', callback_data=f'workout_{i}_{month}_{year}'
                    )
                )
            else:
                lst_but.append(
                    types.InlineKeyboardButton(
                        i, callback_data=f'workout_{i}_{month}_{year}'
                    )
                )
        else:
            lst_but.append(
                types.InlineKeyboardButton(
                    ' ', callback_data=f'workout_{i}_{month}_{year}'
                )
            )

    # добавление кнопок в клавиатуру
    keyboard.add(
        types.InlineKeyboardButton('Пн', callback_data='_'),
        types.InlineKeyboardButton('Вт', callback_data='_'),
        types.InlineKeyboardButton('Ср', callback_data='_'),
        types.InlineKeyboardButton('Чт', callback_data='_'),
        types.InlineKeyboardButton('Пт', callback_data='_'),
        types.InlineKeyboardButton('Сб', callback_data='_'),
        types.InlineKeyboardButton('Вс', callback_data='_'),
    )
    keyboard.add(*lst_but)
    month = get_number_month(month)

    keyboard.add(
        types.InlineKeyboardButton('назад', callback_data=f'-{month} {year}'),
        types.InlineKeyboardButton('вперед', callback_data=f'+{month} {year}'),
    )
    keyboard.add(
        types.InlineKeyboardButton(text='❌', callback_data='start'),
    )
    item = bot.send_message(
        chat_id, f'{month} {year}', reply_markup=keyboard, parse_mode='HTML'
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(lambda callback: callback.data.startswith('+'))
def calendar_next(callback):
    """Проход по календарю вперед"""

    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    chat_id = callback.message.chat.id
    data_date = []

    for i in callback.data[1:].split(' '):
        data_date.append(i)

    num_value_month = get_str_month(data_date[0])
    month = num_value_month + 1
    year = int(data_date[1])

    if month > 12:
        month = 1
        year += 1

    lst_date = [
        i[0]
        for i in db.engine.execute(
            text(
                'SELECT strftime("%Y-%m-%d", date) FROM myworkout GROUP BY date'
            )
        )
    ]

    # множество дат тренировок
    ready_date = set(lst_date)
    # список дней тренировок для последубщего сравнения
    data_num = [
        int(i.split('-')[2])
        for i in ready_date
        if i[:4] == str(year) and int(i[5:7]) == month
    ]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 7
    lst_but = []

    cl = calendar.TextCalendar(firstweekday=0)

    for i in cl.itermonthdays(year, month):
        # итерация по текущему месяцу и создания кнопки с числом месяца
        if i != 0:
            if i in data_num:
                lst_but.append(
                    types.InlineKeyboardButton(
                        '💪', callback_data=f'workout_{i}_{month}_{year}'
                    )
                )
            else:
                lst_but.append(
                    types.InlineKeyboardButton(
                        i, callback_data=f'workout_{i}_{month}_{year}'
                    )
                )
        else:
            lst_but.append(
                types.InlineKeyboardButton(
                    ' ', callback_data=f'workout_{i}_{month}_{year}'
                )
            )

    # добавление кнопок в клавиатуру
    keyboard.add(
        types.InlineKeyboardButton('Пн', callback_data='_'),
        types.InlineKeyboardButton('Вт', callback_data='_'),
        types.InlineKeyboardButton('Ср', callback_data='_'),
        types.InlineKeyboardButton('Чт', callback_data='_'),
        types.InlineKeyboardButton('Пт', callback_data='_'),
        types.InlineKeyboardButton('Сб', callback_data='_'),
        types.InlineKeyboardButton('Вс', callback_data='_'),
    )
    keyboard.add(*lst_but)
    month = get_number_month(month)

    keyboard.add(
        types.InlineKeyboardButton('назад', callback_data=f'-{month} {year}'),
        types.InlineKeyboardButton('вперед', callback_data=f'+{month} {year}'),
    )
    keyboard.add(
        types.InlineKeyboardButton(text='❌', callback_data='start'),
    )
    item = bot.send_message(
        chat_id, f'{month} {year}', reply_markup=keyboard, parse_mode='HTML'
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    lambda callback: callback.data.startswith('workout')
)
def current_workout(callback):
    """Просмотр записей тренировок конкретного дня"""

    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    chat_id = callback.message.chat.id
    data = []

    for i in callback.data.split('_'):
        data.append(i)

    current_date_workout = datetime.date(
        int(data[3]), int(data[2]), int(data[1])
    )
    sql_query = [
        i
        for i in db.engine.execute(
            text(
                f'SELECT entries FROM myworkout WHERE date LIKE "{current_date_workout}%"'
            )
        )
    ]
    if sql_query:
        msg = ''
        for i in sql_query:
            msg += f'<b>ТРЕНИРОВКА ОТ {current_date_workout}</b>\n\n'
            msg += i[0]
            msg += '\n\n'
    else:
        msg = 'Нет записей'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='❌', callback_data='start'),
    )
    item = bot.send_message(
        chat_id, msg, parse_mode='HTML', reply_markup=keyboard
    )
    DEL_MESSEGE_ID.append(item.message_id)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                     ПОГОДА
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


@bot.callback_query_handler(func=lambda callback: callback.data == 'weather')
def get_weather(callback):
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    weather = get_current_weather()
    bot.send_message(
        callback.message.chat.id,
        weather,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                     БЖУ
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'show-nutrition'
)
def get_my_current_table_nutrition(callback):
    """Получение записей за текущий день"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()

    # выборка записей за текущую дату
    entries = [
        *db.engine.execute(
            text(
                f"SELECT * FROM nutrition WHERE date(date) = date('now') ORDER BY date DESC"
            )
        )
    ]

    if len(entries) < 1:
        msg = 'НЕТ данных на сегодня!'
    else:
        # сохранение списка и назначение текущей записи
        LIST_ENTRIES['nutrition'] = deque(entries)
        current_entries = LIST_ENTRIES['nutrition'][0]
        msg = f"""
    {current_entries[2]}
    продукт: {current_entries[1]}
    белки: {current_entries[3]}
    жиры: {current_entries[4]}
    углеводы: {current_entries[5]}
    калории: {current_entries[6]}
    """
    item = bot.send_message(
        callback.message.chat.id,
        msg,
        reply_markup=nutrition_keyboard_piligrim,
        parse_mode='HTML',
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'next-nutrition'
)
def get_next_current_entries(callback):
    """Получение следующей записи"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()

    list_entries = LIST_ENTRIES['nutrition']
    list_entries.rotate(1)
    current_entries = list_entries[0]
    msg = f"""
    {current_entries[2]}
    продукт: {current_entries[1]}
    белки: {current_entries[3]}
    жиры: {current_entries[4]}
    углеводы: {current_entries[5]}
    калории: {current_entries[6]}
    """
    item = bot.send_message(
        callback.message.chat.id,
        msg,
        reply_markup=nutrition_keyboard_piligrim,
        parse_mode='HTML',
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'back-nutrition'
)
def get_back_current_entries(callback):
    """Получение предыдущей записи"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()

    list_entries = LIST_ENTRIES['nutrition']
    list_entries.rotate(-1)
    current_entries = list_entries[0]
    msg = f"""
    {current_entries[2]}
    продукт: {current_entries[1]}
    белки: {current_entries[3]}
    жиры: {current_entries[4]}
    углеводы: {current_entries[5]}
    калории: {current_entries[6]}
    """
    item = bot.send_message(
        callback.message.chat.id,
        msg,
        reply_markup=nutrition_keyboard_piligrim,
        parse_mode='HTML',
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'rm-nutrition'
)
def remove_current_entries(callback):
    """Удаление текущей записи"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    try:
        list_entries = LIST_ENTRIES['nutrition']
        current_entries = list_entries[0]
        id_entries = current_entries[0]
        entries_for_del = MyNutrition.query.filter_by(id=id_entries).first()
        db.session.delete(entries_for_del)
        db.session.commit()

        entries = [
            *db.engine.execute(
                text(
                    f"SELECT * FROM nutrition WHERE date(date) = date('now') ORDER BY date DESC"
                )
            )
        ]

        if len(entries) < 1:
            msg = 'НЕТ данных на сегодня!'
        else:
            # сохранение списка и назначение текущей записи
            LIST_ENTRIES['nutrition'] = deque(entries)
            current_entries = LIST_ENTRIES['nutrition'][0]
            msg = f"""
        {current_entries[2]}
        продукт: {current_entries[1]}
        белки: {current_entries[3]}
        жиры: {current_entries[4]}
        углеводы: {current_entries[5]}
        калории: {current_entries[6]}
        """
    except:
        msg = 'Нет записей'
    item = bot.send_message(
        callback.message.chat.id,
        msg,
        reply_markup=nutrition_keyboard_piligrim,
        parse_mode='HTML',
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'balance-nutrition'
)
def get_current_balance_nutrition(callback):
    """Состояние таблицы за день на текущий момент"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()

    msg = MyNutrition.get_values()
    item = bot.send_message(
        callback.message.chat.id,
        msg,
        reply_markup=main_keyboard,
        parse_mode='HTML',
    )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.callback_query_handler(
    func=lambda callback: callback.data == 'add-nutrition'
)
def add_note_in_nutrition(callback):
    """Старт машины состояний по добавлению записи в таблицу БЖУ"""
    [bot.delete_message(callback.message.chat.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    msg = 'Белки: '
    item = bot.send_message(
        callback.message.chat.id,
        msg,
        reply_markup=nutrition_keyboard,
        parse_mode='HTML',
    )
    set_state_nutrition(StatesNutrition.PROTEINS.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.message_handler(
    func=lambda message: get_current_state_nutrition()
    == StatesNutrition.PROTEINS.value
)
def data_proteins(message):
    """Запись белков"""
    [bot.delete_message(message.from_user.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = message.text
    try:
        STATE_NUTRITION['protein'] = int(data)
        item = bot.send_message(
            message.chat.id,
            'Жиры: ',
            reply_markup=nutrition_keyboard,
        )
        set_state_nutrition(StatesNutrition.FATS.value)
    except:
        msg = 'не верное значение: ВВЕДИ ЦИФРЫ \nБЕЛКИ: '
        item = bot.send_message(
            message.chat.id,
            msg,
            reply_markup=nutrition_keyboard,
        )
        set_state_nutrition(StatesNutrition.PROTEINS.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.message_handler(
    func=lambda message: get_current_state_nutrition()
    == StatesNutrition.FATS.value
)
def data_fats(message):
    """Запись жиров"""
    [bot.delete_message(message.from_user.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = message.text
    try:
        STATE_NUTRITION['fat'] = int(data)
        item = bot.send_message(
            message.chat.id,
            'Углеводы: ',
            reply_markup=nutrition_keyboard,
        )
        set_state_nutrition(StatesNutrition.CARBOHYDRATES.value)
    except:
        msg = 'не верное значение: ВВЕДИ ЦИФРЫ \nЖИРЫ: '
        item = bot.send_message(
            message.chat.id,
            msg,
            reply_markup=nutrition_keyboard,
        )
        set_state_nutrition(StatesNutrition.FATS.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.message_handler(
    func=lambda message: get_current_state_nutrition()
    == StatesNutrition.CARBOHYDRATES.value
)
def data_carbohydrates(message):
    """Запись углеводов"""
    [bot.delete_message(message.from_user.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = message.text
    try:
        STATE_NUTRITION['carbohydrates'] = int(data)
        item = bot.send_message(
            message.chat.id,
            'Калорий: ',
            reply_markup=nutrition_keyboard,
        )
        set_state_nutrition(StatesNutrition.ENERGE.value)
    except:
        msg = 'не верное значение: ВВЕДИ ЦИФРЫ \nУГЛЕВОДЫ: '
        item = bot.send_message(
            message.chat.id,
            msg,
            reply_markup=nutrition_keyboard,
        )
        set_state_nutrition(StatesNutrition.CARBOHYDRATES.value)
    DEL_MESSEGE_ID.append(item.message_id)


@bot.message_handler(
    func=lambda message: get_current_state_nutrition()
    == StatesNutrition.ENERGE.value
)
def data_energe(message):
    """Запись калорий"""
    [bot.delete_message(message.from_user.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = message.text
    try:
        STATE_NUTRITION['energe'] = int(data)
        item = bot.send_message(
            message.chat.id,
            'Продукт: ',
            reply_markup=nutrition_keyboard,
        )
        set_state_nutrition(StatesNutrition.NAME.value)
    except:
        msg = 'не верное значение: ВВЕДИ ЦИФРЫ \nКАЛОРИИ: '
        set_state_nutrition(StatesNutrition.ENERGE.value)
        item = bot.send_message(
            message.chat.id,
            msg,
            reply_markup=nutrition_keyboard,
        )
    DEL_MESSEGE_ID.append(item.message_id)


@bot.message_handler(
    func=lambda message: get_current_state_nutrition()
    == StatesNutrition.NAME.value
)
def data_name(message):
    """Запись имени продукта"""
    [bot.delete_message(message.from_user.id, id) for id in DEL_MESSEGE_ID]
    DEL_MESSEGE_ID.clear()
    data = message.text
    try:
        name_product = data
        msg = f"""Запись сделана 
        {name_product}
        {STATE_NUTRITION['protein']}
        {STATE_NUTRITION['fat']}
        {STATE_NUTRITION['carbohydrates']}
        {STATE_NUTRITION['energe']}"""
        entries = MyNutrition(
            name=name_product,
            proteins=STATE_NUTRITION['protein'],
            fats=STATE_NUTRITION['fat'],
            carbohydrates=STATE_NUTRITION['carbohydrates'],
            energy=STATE_NUTRITION['energe'],
        )

        db.session.add(entries)
        db.session.commit()
    except:
        msg = 'что то пошло не так, придется начать сначала'
    item = bot.send_message(
        message.chat.id,
        msg,
        reply_markup=main_keyboard,
    )
    set_state_nutrition(StatesNutrition.START.value)
    DEL_MESSEGE_ID.append(item.message_id)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'ru')


@server.route('/', methods=['GET', 'POST'])
def receive_update():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK'
    else:
        abort(403)


@server.route('/login', methods=['POST', 'GET'])
def index_autorization():
    """Авторизация администратора"""
    if request.method == 'POST':
        admin = AdminUser.query.filter_by(
            name=request.form['name'], psw=request.form['psw']
        ).first()
        if admin:
            login_user(admin, remember=True)
            return redirect(url_for('admin.index'))
        else:
            flash('Неверный логин или пароль!')
    return render_template('autorization.html', title='Авторизация')


@server.route('/exit', methods=['POST', 'GET'])
@login_required
def user_exit():
    logout_user()
    print(current_user)
    return redirect(url_for('index_autorization'))


@server.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


# bot.polling()

bot.remove_webhook()
time.sleep(0.1)

bot.set_webhook(url='')
