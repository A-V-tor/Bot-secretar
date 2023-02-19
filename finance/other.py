import os
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from dotenv import find_dotenv, load_dotenv
from datetime import datetime

load_dotenv(find_dotenv())
headers = {'user-agent': os.getenv('headers')}


def get_product():
    """Получение цен на нефть и газ"""
    mytable = PrettyTable()
    mytable.field_names = ['товар', 'цена 💰', '📈 $', '📉 %']
    ses = requests.Session()

    try:
        response = ses.get(
            f'https://ru.tradingview.com/markets/futures/quotes-energy/',
            headers=headers,
        )
        soup = BeautifulSoup(response.text, 'html.parser')

        # список данных для извлечении имен
        data_list_names = soup.find_all(
            'sup', class_='apply-common-tooltip tickerDescription-hMpTPJiS'
        )
        # список имен
        list_names = [i.text for i in data_list_names][:10]
        # список данных
        list_data = [
            i.text
            for i in soup.find_all('td', class_='cell-TKkxf89L right-TKkxf89L')
        ]
        lst = []

        # разбивка данных на коллекции
        while len(list_data) > 0:
            item = list_data[:5]
            lst.append(item)
            list_data = list_data[5:]

        ready_data = zip(list_names, lst)
        # извлечение и добавлении данных в таблицу
        item = [i for i in ready_data]
        lst = []
        lst.append(item[0])
        lst.append(item[3])
        for i in lst:
            name = i[0]
            price = i[1][0]
            percent_change = i[1][1]
            rub_change = i[1][2]
            data_table = []
            data_table.extend([name, price, rub_change, percent_change])
            mytable.add_row(data_table)
    except Exception:
        mytable.add_row(['Что-то', 'пошло', 'не так', '!'])

    return f'<pre>{datetime.now()}\n{mytable}</pre>'
