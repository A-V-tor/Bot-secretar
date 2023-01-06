import os
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from dotenv import find_dotenv, load_dotenv


def get_news():
    ses = requests.Session()
    response = ses.get(f'https://www.nytimes.com/international/section/world/europe', headers={"user-agent": os.getenv("headers")})

    soup = BeautifulSoup(response.text, 'html.parser')

    news = soup.find_all('div', class_='css-1l4spti')
    list_titles = [i.find('h2',class_='css-1kv6qi e15t083i0').text for i in news]
    list_short_news_description = []
    list_links = ['https://www.nytimes.com/'+i.find('a').get('href') for i in news]

    for i in news:
        try:
            item = i.find('p',class_='css-1pga48a e15t083i1').text
        except:
            item = 'нет текста'
        list_short_news_description.append(item)

    ready_data = zip(list_titles, list_short_news_description, list_links)
    res = ''

    for i in ready_data:
        res += f"<b>{i[0]}</b>\n<i>{i[1]}</i>\n{i[2]}\n\n"

    return res
