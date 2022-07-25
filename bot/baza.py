import sqlite3
from prettytable import PrettyTable


# with sqlite3.connect(r'bot/bot_bz.db') as base: - путь при сборке пакета
with sqlite3.connect(r'Documents/TG_bot/bot/bot_bz.db') as base:
    cur = base.cursor()

# таблица журнала тренировок
base.execute('CREATE TABLE IF NOT EXISTS data(\
    the_date,\
    day TEXT,\
    biceps  INTEGER ,\
    waist   INTEGER,\
    chest   INTEGER ,\
    triceps INTEGER )')
base.commit()

def add_tren(data,day,bic,waist,chest,tric):
    '''Добавляются нужные данные в бд'''  
    if day == 'Sunday':
        day = 'Воскресенье'
    if day =='Monday':
        day ='Понедельник'
    if day == 'Tuesday':
        day = 'Вторник'
    if day =='Wednesday':
        day = 'Среда'
    if day =='Thursday':
        day = 'Четверг'
    elif day =='Friday':
        day = 'Пятница'
    elif day == 'Saturday':
        day = 'Суббота'
    else:
        day =='-'
    cur.execute('INSERT INTO data VALUES(?,?,?,?,?,?)',(data,day,bic,waist,chest,tric))
    base.commit()
    res = 'Данные успешно добавлены!'
    return res


def get_workout_record(value, item):
    '''Функция достает нужные значения и формирует таблицу на возврат'''
    data = cur.execute('SELECT * FROM data WHERE {} LIKE {}'.format(value,item)).fetchall()
    if data:
        mytable = PrettyTable()
        mytable.field_names = ["дата", "день", "бицепс", "пояс", "грудь", "трицепс"]
        for i in data:
            mytable.add_row(i)
        return f'<pre>{mytable}</pre>'
    else:
        result = 'Данные не найдены'
        return result



def get_workout_limit_record(item):
    '''Функция отдает лимитированое кол-во записей'''
    mytable = PrettyTable()
    mytable.field_names = ["дата", "день", "бицепс", "пояс", "грудь", "трицепс"]
    data_all = cur.execute('SELECT * FROM data ORDER BY rowid DESC LIMIT {} '.format(item)).fetchall()
    for i in data_all:
        mytable.add_row(i)
    return f'<pre>{mytable}</pre>'


def update_tren(name_column, new_value, rowid):
    '''Редактирование данных БД'''
    post = cur.execute('UPDATE data SET {} = {} WHERE rowid={}'.format(name_column, new_value,rowid))
    base.commit()
    message_ = 'Данные обновлены'
    data_string = cur.execute('SELECT * FROM data WHERE rowid={}'.format(rowid))
    print(data_string)
    head = '        Дата        |     День недели|бицепс|от пояса|от груди|трицепс|\n\n'
    res = ''
    res += head
    for i in data_string:
            for v in i:
                res += str(v)
                res += '          '
    return res
    

def get_rowid(value):
    '''Выдает rowid id'''
    data_all = cur.execute('SELECT rowid FROM data WHERE the_date LIKE {}'.format(value)).fetchall()
    try:
        res_str = f'ID равен: '
        for i in data_all:
            for v in i:
                res_str += str(v)
                res_str += ' '
        return res_str
    except:
        result = 'Данные на этот день отсутствуют!\nУточни дату в журнале!'
        return result


def get_sum_all_record_day():
    '''Суммирует значение всех записей в рамках одного дня'''
    mytable = PrettyTable()
    mytable.field_names = ["дата", "день", "бицепс", "пояс", "грудь", "трицепс"]
    data_the_date = cur.execute('SELECT the_date FROM data GROUP BY the_date')
    item = [v[0] for v in[i for i in data_the_date]] # список дат
    for i in item:
        data = cur.execute('SELECT the_date,day,sum(biceps),sum(waist),sum(chest),sum(triceps) FROM data WHERE the_date ="{item}"'.format(item=i))
        for value in data:
            mytable.add_row(value)
    return f'<pre>{mytable}</pre>'