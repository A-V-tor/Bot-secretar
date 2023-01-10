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
    ENTER_CATEGORY = 1
    ENTER_MONEY = 2


def get_current_state():
    try:
        return sl["state"]
    except:
        return 0


def set_state(value):
    try:
        sl["state"] = value
        return True
    except:
        return False


def get_current_state_edit():
    try:
        return sl_edit["state"]
    except:
        return 0


def set_state_edit(value):
    try:
        sl_edit["state"] = value
        return True
    except:
        return False


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         МАШИНА СОСТОЯНИЙ ДЛЯ ВЕДЕНИЯ  ЗАПИСЕЙ ВЕСА
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

sl_weight = {}

class StateslWeight(Enum):
    START = 0
    END = 1


def get_current_statel_weight():
    try:
        return sl["state"]
    except:
        return 0


def set_state_weight(value):
    try:
        sl["state"] = value
        return True
    except:
        return False