import time
import calendar
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from datetime import date, datetime
from bot.tkn import h, wbot


lst = ['MU?p=MU&.tsrc=fin-srch', 'BYND?p=BYND&.tsrc=fin-srch', 'EXEL?p=EXEL&.tsrc=fin-srch']
def get_price_market(item):
    mytable = PrettyTable()
    mytable.field_names = ["компания", "цена", "изменение $", "изменение %"]
    for i in item:
        url = f'https://finance.yahoo.com/quote/{i}'
        ses = requests.Session()

        respons = ses.get(url, headers=h)
        soup = BeautifulSoup(respons.text, 'html.parser')

        name = soup.find('h1', class_='D(ib) Fz(18px)').text
        price = soup.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text
        changes = soup.find_all('fin-streamer', class_='Fw(500) Pstart(8px) Fz(24px)')
        lst_changes = [i.text for i in changes if i.find('span')]
        changes = lst_changes[0]
        changes_ = lst_changes[1]
        lst=[]
        lst.extend([name,price,changes,changes_])
        mytable.add_row(lst)
        time.sleep(1.5)
    print('Скрепер сработал!')
    return f'<pre>{mytable}</pre>'

def get_calendar():
    url = 'https://www.reddit.com/r/wallstreetbets/search?q=flair_name%3A%22Earnings%20Thread%22&restrict_sr=1&sort=new'

    ses = requests.Session()
    respons = ses.get(url, headers=h)
    soup = BeautifulSoup(respons.text, 'html.parser')
    data = soup.find('div', class_='_2MkcR85HDnYngvlVW2gMMa').find('a').get('href')

    down = requests.get(data, stream = True)
    f = open('/bot/image/calendar.jpg', 'wb') 
    for i in down.iter_content(1024*1024):
        f.write(i)
        f.close()



def calendar_check():
    '''каждый понедельник календарь будет обновляться с помощью этой функции'''
    data_ = date.today()
    dt1=datetime.strptime('10::00::05', '%H::%M::%S').time() # нижняя граница обновления календаря
    dt2=datetime.strptime('10::03::00', '%H::%M::%S').time() # верхняя граница 
    now = datetime.now().time() # текущее время
    calendar.day_name[data_.weekday()]
    if calendar.day_name[data_.weekday()] == "Monday" and dt1<now<dt2:
        get_calendar()
        time.sleep(60)
    else:
        pass


def get_price_crypto():
    url = 'https://bitinfocharts.com/ru/crypto-kurs/'
    respons = requests.get(url,headers=h)
    soup = BeautifulSoup(respons.text, 'lxml')
    data = soup.find_all('div', class_='i_div')

    lst_name = [i.next_element for i in data] # список названий монет
    lst_name = lst_name[:11]
    data = soup.find_all('a', class_='conv_cur')

    lst_price =[i.text.replace(',',' ') for i in data] # список цен
    lst_price = lst_price[:11]

    changes = soup.find_all('span', class_='text-success')
    data_changes = [i.find('b') for i in changes]
    lst_changes = [i.text for i in data_changes]
    lst_changes = lst_changes[:11] # список измениний цен

    mytable = PrettyTable()
    mytable.field_names = ["монета", "цена", 'изменение']
    lst = []
    lst.append(lst_name[0])
    lst.append(lst_price[0])
    lst_price = [i.replace(' ','') for i in lst_price]
    lst_name = [i.replace("'",'') for i in lst_name]
    data = zip(lst_name, lst_price, lst_changes)
    for i in data:
        mytable.add_row(i)
    return f'<pre>{mytable}</pre>'

token = wbot

