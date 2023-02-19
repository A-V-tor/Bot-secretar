import os
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from dotenv import find_dotenv, load_dotenv
from datetime import datetime


load_dotenv(find_dotenv())
headers = {'user-agent': os.getenv('headers')}


def get_current_weather():
    """Текщая погода в Липецке"""

    try:
        url = 'https://www.gismeteo.ru/weather-lipetsk-4437/now/'
        ses = requests.Session()
        respons = ses.get(url, headers=headers)
        soup = BeautifulSoup(respons.text, 'html.parser')

        current_temperature = soup.find(
            'span', class_='unit unit_temperature_c'
        ).text
        description = soup.find('div', class_='now-desc').text
        wind = soup.find('div', class_='unit unit_wind_m_s').text
        pressure = soup.find('div', class_='unit unit_pressure_mm_hg_atm').text
        humidity = soup.find('div', class_='now-info-item humidity').text

        data = f"""
        ⚠ {description}
        {current_temperature}
        {wind[:4]} {wind[4:]}
        {pressure}
        {humidity[:9]} {humidity[9:]}
        """
    except:
        data = 'нет данных'

    return data
