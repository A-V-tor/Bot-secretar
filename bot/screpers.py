import requests
from bs4 import BeautifulSoup
import lxml
import time
from bot.tkn import h

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


if __name__ == '__main__':
    get_price_market(lst)
