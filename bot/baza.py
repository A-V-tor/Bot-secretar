import sqlite3

with sqlite3.connect(r'Documents/TG_bot/bot/bot_bz.db') as base:
    cur = base.cursor()

base.execute('CREATE TABLE IF NOT EXISTS data(\
    the_date,\
    day TEXT,\
    biceps  INTEGER ,\
    waist   INTEGER,\
    chest   INTEGER ,\
    triceps INTEGER )')
base.commit()

def add_tren(data,day,bic,waist,chest,tric):
    '''добавляются нужные данные в бд'''
    cur.execute('INSERT INTO data VALUES(?,?,?,?,?,?)',(data,day,bic,waist,chest,tric))
    base.commit()


def get_workout_record(value, item):
    '''функция достает нужные значения и формирует таблицу на возврат'''
    data = cur.execute('SELECT * FROM data WHERE {} LIKE {}'.format(value,item)).fetchall()
    if data:
        res = ''
        lst = []
        res_lst = []
        head = f'     Дата        | День недели  |  бицепс  |  от пояса  |  от груди  |  трицепс  |'
        res_lst.append(head)
        for i in data:
            lst.append(i)
        while len(lst) > 0:
            data, day, bic, waist, chest, tric = lst[0]
            # в зависимости от дня недели подается соответствующая строка
            if day == 'понедельник' or day == 'воскресенье':
                response = f'{data}  |{day}   |      {str(bic)}      |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            elif day == 'вторник' or day == 'четверг' or day == 'пятница' or day == 'суббота':
                response = f'{data}  |{day}            |      {str(bic)}      |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            else:
                response = f'{data}  |{day}               |      {str(bic)}      |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            res_lst.append(response)
            lst = lst[1:]
        for v in res_lst:
            res += v
            res += '\n\n'
        return res
    else:
        result = 'Данные не найдены'
        return result

def get_workout_all_record(item):
    '''функция отдает лимитированое кол-во записей'''
    data_all = cur.execute('SELECT * FROM data ORDER BY rowid DESC LIMIT {} '.format(item)).fetchall()
    if data_all:
        res = ''
        lst = []
        res_lst = []
        head = f'     Дата        | День недели  |  бицепс  |  от пояса  |  от груди  |  трицепс  |'
        res_lst.append(head)
        for i in data_all:
            lst.append(i)
        while len(lst) > 0:
            data, day, bic, waist, chest, tric = lst[0]
            # в зависимости от дня недели подается соответствующая строка
            if day == 'понедельник' or day == 'воскресенье':
                response = f'{data}  |{day}   |      {str(bic)}      |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            elif day == 'вторник' or day == 'четверг' or day == 'пятница' or day == 'суббота':
                response = f'{data}  |{day}            |      {str(bic)}      |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            else:
                response = f'{data}  |{day}               |      {str(bic)}      |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            res_lst.append(response)
            lst = lst[1:]
        for v in res_lst:
            res += v
            res += '\n\n'
        return res
    else:
        result = 'Данные не найдены'
        return result

def update_tren(name_column, new_value, rowid):
    '''редактирование данных БД'''
    post = cur.execute('UPDATE data SET {} = {} WHERE rowid={}'.format(name_column, new_value,rowid))
    base.commit()
    message_ = 'Данные обновлены'
    return message_

def get_rowid(value):
    '''выдает rowid id'''
    data_all = cur.execute('SELECT rowid FROM data WHERE the_date LIKE {}'.format(value)).fetchone()
    try:
        row_id = data_all[0]
        result = f'ID равен {row_id}'
        return result
    except:
        result = 'Данные на этот день отсутствуют!\nУточни дату в журнале!'
        return result

