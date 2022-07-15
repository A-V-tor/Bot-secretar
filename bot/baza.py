import sqlite3

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
    '''добавляются нужные данные в бд'''  
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
    else:
        day = 'Суббота'
    cur.execute('INSERT INTO data VALUES(?,?,?,?,?,?)',(data,day,bic,waist,chest,tric))
    base.commit()
    res = 'Данные успешно добавлены!'
    return res


def get_workout_record(value, item):
    '''функция достает нужные значения и формирует таблицу на возврат'''
    data = cur.execute('SELECT * FROM data WHERE {} LIKE {}'.format(value,item)).fetchall()
    if data:
        res = ''
        lst = []
        res_lst = []
        head = f'     Дата        |     День недели    |  бицепс  |  от пояса  |  от груди  |  трицепс  |'
        res_lst.append(head)
        for i in data:
            lst.append(i)
        while len(lst) > 0:
            data, day, bic, waist, chest, tric = lst[0]
            # в зависимости от дня недели подается соответствующая строка
            if day == 'понедельник' or day == 'воскресенье':
                response = f'{data}  |{day}   |   {str(bic)}     |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            elif day == 'вторник' or day == 'четверг' or day == 'пятница' or day == 'суббота':
                response = f'{data}  |{day}    |     {str(bic)}     |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            else:
                response = f'{data}  |{day}               |      {str(bic)}      |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            res_lst.append(response)
            lst = lst[1:]
        for v in res_lst:
            res += v
            res += '\n\n'
        res += '\n'
        res += 'Для корректного отображения разверни телефон'
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
        head = f'     Дата              | День недели  |  бицепс  |  от пояса  |  от груди  |  трицепс                      |'
        res_lst.append(head)
        for i in data_all:
            lst.append(i)
        while len(lst) > 0:
            data, day, bic, waist, chest, tric = lst[0]
            # в зависимости от дня недели подается соответствующая строка
            if day == 'Понедельник' or day == 'Воскресенье':
                response = f'{data}  |{day}   |      {str(bic)}      |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            elif day == 'Вторник' or day == 'Четверг' or day == 'Пятница' or day == 'Суббота':
                response = f'{data}  |{day}            |      {str(bic)}      |       {str(waist)}        |        {str(chest)}       |       {str(tric)}                     |'
            else:
                response = f'{data}  |{day}               |      {str(bic)}      |       {str(waist)}        |        {str(chest)}       |       {str(tric)}       |'
            res_lst.append(response)
            lst = lst[1:]
        for v in res_lst:
            res += v
            res += '\n\n'
        res += '\n'
        res += 'Для корректного отображения разверни телефон'
        return res
    else:
        result = 'Данные не найдены'
        return result

def update_tren(name_column, new_value, rowid):
    '''редактирование данных БД'''
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
    #return message_
    

def get_rowid(value):
    '''выдает rowid id'''
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
#print(get_rowid('2022-07-14'))