import requests
from bs4 import BeautifulSoup
import time
from bot.tkn import h
import calendar
from datetime import date, datetime


lst = ['MU?p=MU&.tsrc=fin-srch', 'BYND?p=BYND&.tsrc=fin-srch', 'EXEL?p=EXEL&.tsrc=fin-srch']
def get_price_market(item):
    sl = {}
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
        sl.update({name: [price, changes, changes_]})
        time.sleep(1.5)
    result = ''
    for i in sl:
        res = f'{i} цена: {sl[i][0]} \u0024, изменения: {sl[i][1]} \u0024 {sl[i][2]}'
        result += res
        result += '\n\n'
    print('Скрепер сработал!')
    return result


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
    if calendar.day_name[data_.weekday()] == "Monday" and dt1<now<dt2:
        get_calendar()
    else:
        pass




