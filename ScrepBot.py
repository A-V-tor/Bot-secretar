import requests
from bs4 import BeautifulSoup
import lxml
import time

# список нужных акий
lst = ['exelixis-inc', 'beyond-meat-inc', 'micron-tech']



def function_screp(item):
    slov = {}
    headers = {

}
    ses = requests.Session()
    
    for i in item:
        response = ses.get(f'https://ru.investing.com/equities/{i}', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
    # вылавливаю нужные данные
        name = soup.find('h1').text
        price = soup.find('span', class_='text-2xl').text
        ticer = soup.find('h2', class_= 'text-lg font-semibold').text
        ticer = ticer[6:]
        
        try:
            change = soup.find('span', class_='instrument-price_change-value__jkuml ml-2.5 text-negative-main').text
            change_ = soup.find('span', class_='instrument-price_change-percent__19cas ml-2.5 text-negative-main').text
            sl = f'Компания {name}\nЦена {price}\U0001F4B2\nИзменение цены к закрытию {change}\u0024 {change_}\n\n'
            slov[ticer] = sl
            time.sleep(3)
    # сайт то и дело меняет значение class, делаю исключение
        except:
            change = soup.find('span', class_='instrument-price_change-value__jkuml ml-2.5 text-positive-main').text
            change_ = soup.find('span', class_='instrument-price_change-percent__19cas ml-2.5 text-positive-main').text
            sl = f'Компания {name}\nЦена {price}\U0001F4B2\nИзменение цены к закрытию {change}\u0024 {change_}\n\n'
            slov[ticer] = sl
            time.sleep(3)     
    print('скрапер сработал')
    # при успешном сценарии формируется словарь с данными
    return slov


# функция вынимает значения из словаря и ложит в переменые (пока вручную) 
def screp_iter(a):
    comp1 = a['EXEL']
    comp2 = a['BYND']
    comp3 = a['MU']
    ot = f'{comp1}\n{comp2}\n{comp3}\n'
    return ot

    

if __name__ == '__main__':
    print(screp_iter(function_screp(lst)))
    

