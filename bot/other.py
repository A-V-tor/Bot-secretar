from enum import Enum


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         МАШИНА СОСТОЯНИЙ ДЛЯ ВЕДЕНИЯ РАСХОДОВ
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

sl = {}
sl_edit = {}


class States(Enum):
    START = 0
    ENTER_CATEGORY = 1
    ENTER_MONEY = 2


class StatesEdit(Enum):
    START = 0
    ENTER_CATEGORY_EDIT = 6
    ENTER_MONEY_EDIT = 8


def get_current_state():
    try:
        return sl['state']
    except:
        return 0


def set_state(value):
    try:
        sl['state'] = value
        return True
    except:
        return False


def get_current_state_edit():
    try:
        return sl_edit['state']
    except:
        return 0


def set_state_edit(value):
    try:
        sl_edit['state'] = value
        return True
    except:
        return False


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         МАШИНА СОСТОЯНИЙ ДЛЯ ВЕДЕНИЯ  ЗАПИСЕЙ ВЕСА
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

sl_weight = {}


class StatesWeight(Enum):
    START = 65
    END = 3


def get_current_state_weight():
    try:
        return sl_weight['state']
    except:
        return 98


def set_state_weight(value):
    try:
        sl_weight['state'] = value
        return True
    except:
        return False


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         МАШИНА СОСТОЯНИЙ ДЛЯ ВЕДЕНИЯ  ЗАМЕТОК
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

sl_notes = {}


class StatesNotes(Enum):
    START = 5
    END = 4


def get_current_state_notes():
    try:
        return sl_notes['state']
    except:
        return 99


def set_state_notes(value):
    try:
        sl_notes['state'] = value
        return True
    except:
        return False


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         МАШИНА СОСТОЯНИЙ ДЛЯ ВЕДЕНИЯ  ТРЕНИРОВОК
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


sl_workout = {}


class StatesWorkout(Enum):
    START = 97
    END = 44


def get_current_state_workout():
    try:
        return sl_workout['state']
    except:
        return 95


def set_state_workout(value):
    try:
        sl_workout['state'] = value
        return True
    except:
        return False


def get_current_date(str_data):
    """Прием строки год, месяц и возврат списка с int: годом и int: месяцем"""

    data = str_data.split(',')
    lst = []
    for i in data:
        lst.append(int(i))
    return lst


def get_number_month(month):
    """Отдача str: месяца по порядковому номеру"""

    if month == 1:
        month = 'ЯНВАРЬ'
    if month == 2:
        month = 'ФЕВРАЛЬ'
    if month == 3:
        month = 'МАРТ'
    if month == 4:
        month = 'АПРЕЛЬ'
    if month == 5:
        month = 'МАЙ'
    if month == 6:
        month = 'ИЮНЬ'
    if month == 7:
        month = 'ИЮЛЬ'
    if month == 8:
        month = 'АВГУСТ'
    if month == 9:
        month = 'СЕНТЯБРЬ'
    if month == 10:
        month = 'ОКТЯБРЬ'
    if month == 11:
        month = 'НОЯБРЬ'
    if month == 12:
        month = 'ДЕКАБРЬ'

    return month


def get_str_month(date_month):
    """Отдача порядкового номенра int: в зависимости от месяца"""

    if date_month == 'ЯНВАРЬ':
        value_month = 1
    if date_month == 'ФЕВРАЛЬ':
        value_month = 2
    if date_month == 'МАРТ':
        value_month = 3
    if date_month == 'АПРЕЛЬ':
        value_month = 4
    if date_month == 'МАЙ':
        value_month = 5
    if date_month == 'ИЮНЬ':
        value_month = 6
    if date_month == 'ИЮЛЬ':
        value_month = 7
    if date_month == 'АВГУСТ':
        value_month = 8
    if date_month == 'СЕНТЯБРЬ':
        value_month = 9
    if date_month == 'ОКТЯБРЬ':
        value_month = 10
    if date_month == 'НОЯБРЬ':
        value_month = 11
    if date_month == 'ДЕКАБРЬ':
        value_month = 12

    return value_month


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         МАШИНА СОСТОЯНИЙ ДЛЯ ВЕДЕНИЯ  БЖУ
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


sl_nutrition = {}


class StatesNutrition(Enum):
    START = 100
    PROTEINS = 101
    FATS = 102
    CARBOHYDRATES = 103
    ENERGE = 104
    NAME = 105


def get_current_state_nutrition():
    try:
        return sl_nutrition['state']
    except:
        return 100


def set_state_nutrition(value):
    try:
        sl_nutrition['state'] = value
        return True
    except:
        return False
