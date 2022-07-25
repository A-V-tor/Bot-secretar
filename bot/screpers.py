import time
import calendar
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from datetime import date, datetime
from bot.tkn import h


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
    f = open('/Users/user/Documents/TG_bot/bot/image/calendar.jpg', 'wb') # путь при сборке пакета нужно будет переделать!
    for i in down.iter_content(1024*1024):
        f.write(i)
        f.close()



def calendar_check():
    '''каждый понедельник календарь будет обновляться с помощью этой функции'''
    data_ = date.today()
    dt1=datetime.strptime('2021-01-29T10:00:04.836603Z', "%Y-%m-%dT%H:%M:%S.%fZ") # нижняя граница обновления календаря
    dt2=datetime.strptime('2021-01-29T10:01:04.836603Z', "%Y-%m-%dT%H:%M:%S.%fZ") # верхняя граница 
    now = datetime.now().time() # текущее время
    calendar.day_name[data_.weekday()]
    if calendar.day_name[data_.weekday()] == "Monday":# and now not in [dt1,dt2]:  требуеться корректировка функции https://ru.stackoverflow.com/questions/1378424/Сравнение-дат-времени-в-python
        get_calendar()
        print('calendar')
    else:
        pass




