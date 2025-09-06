import enum
import html
import re
import secrets
import string


async def get_prev_month_and_year(month: int, year: int) -> tuple[int, int]:
    """Получение предыдущего месяца для инлайн календаря.

    Args:
        month: месяц целочисленным представлением
        year: год целочисленным представлением

    """
    if month != 1:
        month -= 1
    else:
        year -= 1
        month = 12

    return month, year


async def get_next_month_and_year(month: int, year: int) -> tuple[int, int]:
    """Получение следующего месяца для инлайн календаря.

    Args:
        month: месяц целочисленным представлением
        year: год целочисленным представлением

    """
    if month != 12:
        month += 1
    else:
        year += 1
        month = 1

    return month, year


async def validate_weight(string_value: str) -> str | bool:
    """Валидатор текстового отображения веса.

    Args:
        string_value: строковое представление веса

    """
    kg, gr = '', ''
    result = False

    if '.' in string_value:
        kg, gr = string_value.split('.')
        result = string_value

    elif ',' in string_value:
        kg, gr = string_value.split(',')
        result = f'{kg}.{gr}'

    elif string_value.isdigit():
        kg, gr = string_value, '00'
        result = f'{kg}.{gr}'

    if not kg.isdigit() or not gr.isdigit():
        result = False

    return result


def clean_unsupported_tags(html_text) -> str:
    """Очистка сообщения от неразрешеных в телеграм тегов.

    Args:
        html_text: входной текст для очистки от запрещенных тегов

    """
    # декодировать HTML сущности
    html_text = html.unescape(html_text)

    # Список поддерживаемых Telegram API тегов
    supported_tags = {
        'b',
        'strong',
        'i',
        'em',
        'u',
        'ins',
        's',
        'strike',
        'del',
        'code',
        'pre',
        'a',
        'br',
    }

    #  замена <p> на двойную новую строку и <br> на одну новую строку
    html_text = re.sub(r'</?p[^>]*>', '\n\n', html_text)
    html_text = re.sub(r'<br\s*/?>', '\n', html_text)

    # шаблон поиска HTML тегов
    tag_pattern = re.compile(r'<(/?)(\w+)([^>]*?)>')

    def replace_tag(match):
        slash, tag, rest = match.groups()
        if tag.lower() in supported_tags:
            # текста прошел проверку
            return match.group(0)
        else:
            # удаление тега и содержимого
            return ''

    # замена неподдерживаемых тегов с сохранением содержимого
    cleaned_text = re.sub(tag_pattern, replace_tag, html_text)

    # убрать лишние пробелы
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text.strip())

    return cleaned_text


def generate_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(20))


class TypeExpenses(str, enum.Enum):
    HEALTH = 'здоровье'
    TRANSPORT = 'транспорт'
    FOOD = 'еда'
    ENTERTAINMENT = 'развлечения'
    PRESENT = 'подарки'
    ELECTRONICS = 'электроника'
    CLOTH = 'одежда'
    TAXES = 'налоги'
    OTHER = 'прочее'


class UserPermissions(str, enum.Enum):
    user = 'Пользователь'
    moderator = 'Модератор'
    admin = 'Админ'
    owner = 'Владелец'


class ReminderLevel(str, enum.Enum):
    very_important = 'очень важно'
    important = 'важно'
    doesnot_matter = 'не важно'


class TimeZoneEnum(str, enum.Enum):
    offset_00 = 'Atlantic/Reykjavik'
    offset_01 = 'Europe/Berlin'
    offset_02 = 'Europe/Kaliningrad'
    offset_03 = 'Europe/Moscow'
    offset_04 = 'Europe/Samara'
    offset_05 = 'Asia/Yekaterinburg'
    offset_06 = 'Asia/Omsk'
    offset_07 = 'Asia/Novosibirsk'
    offset_08 = 'Asia/Irkutsk'
    offset_09 = 'Asia/Chita'
    offset_10 = 'Asia/Vladivostok'

    @classmethod
    def get_offset(cls, timezone_string: str):
        for tz in cls:
            if tz.value == timezone_string:
                return tz.value
        raise ValueError(f'Невалидный часовой пояс: {timezone_string}')


month_map = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}
