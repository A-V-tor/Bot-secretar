import os
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from dotenv import find_dotenv, load_dotenv
from datetime import datetime


load_dotenv(find_dotenv())
headers = {"user-agent": os.getenv("headers")}

allow_name = [
    "ПАО НК РОСНЕФТЬ",
    "Газпром",
    'ПАО "НОВАТЭК" АО',
    "Сбербанк",
    "ЛУКОЙЛ",
    'ГМК "НОР.НИКЕЛЬ" ПАО АО',
    "ФОСАГРО ПАО АО",
    'ПАО "НЛМК" АО',
    "АКРОН ПАО АО",
    "United Company RUSAL PLC",
    "Магнит",
    "АЛРОСА ПАО АО",
    "ПИК СЗ (ПАО) АО",
    "ГРУППА ПОЗИТИВ АО",
    "СЕГЕЖА АО",
    "ПАО ДЕТСКИЙ МИР",
]


lst_technologies = [
    "NVDA?p=NVDA&.tsrc=fin-srch",
    "TSM?p=TSM&.tsrc=fin-srch",
    "QCOM?p=QCOM&.tsrc=fin-srch",
    "AMD?p=AMD&.tsrc=fin-srch",
    "TSLA?p=TSLA&.tsrc=fin-srch",
    "GOOG?p=GOOG&.tsrc=fin-srch",
    "META?p=META&.tsrc=fin-srch",
    "AMZN?p=AMZN&.tsrc=fin-srch",
    "AAPL?p=AAPL&.tsrc=fin-srch",
    "NFLX?p=NFLX&.tsrc=fin-srch",
]

lst_production = [
    "F?p=F&.tsrc=fin-srch",
    "GM?p=GM&.tsrc=fin-srch",
    "BA?p=BA&.tsrc=fin-srch",
    "TM?p=TM&.tsrc=fin-srch",
    "LMT?p=LMT&.tsrc=fin-srch",
    "HON?p=HON&.tsrc=fin-srch",
    "CVX?p=CVX&.tsrc=fin-srch",
    "SHEL?p=SHEL&.tsrc=fin-srch",
    "BP?p=BP&.tsrc=fin-srch",
    "XOM?p=XOM&.tsrc=fin-srch",
]

lst_finance = [
    "JPM?p=JPM&.tsrc=fin-srch",
    "C?p=C&.tsrc=fin-srch",
    "BAC?p=BAC&.tsrc=fin-srch",
    "WFC?p=WFC&.tsrc=fin-srch",
    "GS?p=GS&.tsrc=fin-srch",
]

lst_medical = [
    "MRK?p=MRK&.tsrc=fin-srch",
    "PFE?p=PFE&.tsrc=fin-srch",
    "JNJ?p=JNJ&.tsrc=fin-srch",
    "BMY?p=BMY&.tsrc=fin-srch",
    "LLY?p=LLY&.tsrc=fin-srch",
]

lst_favorites = [
    "MU?p=MU&.tsrc=fin-srch",
    "TSM?p=TSM&.tsrc=fin-srch",
    "BYND?p=BYND&.tsrc=fin-srch",
    "EXEL?p=EXEL&.tsrc=fin-srch",
    "MRK?p=MRK&.tsrc=fin-srch",
    "LLY?p=LLY&.tsrc=fin-srch",
]


def get_normalized_name(name):
    if name == "Taiwan Semiconductor Manufacturing Company Limited (TSM)":
        name = "TSMS"
    if name == "Micron Technology, Inc. (MU)":
        name = "Micron"
    if name == "Beyond Meat, Inc. (BYND)":
        name = "Beyond Meat"
    if name == "Exelixis, Inc. (EXEL)":
        name = "Exelixis"
    if name == "Merck & Co., Inc. (MRK)":
        name = "Merck & Co"
    if name == "Eli Lilly and Company (LLY)":
        name = "Eli Lilly"
    if name == "JPMorgan Chase & Co. (JPM)":
        name = "JPMorgan"
    if name == "Citigroup Inc. (C)":
        name = "Citigroup"
    if name == "Bank of America Corporation (BAC)":
        name = "Bank of America"
    if name == "Wells Fargo & Company (WFC)":
        name = "Wells Fargo"
    if name == "The Goldman Sachs Group, Inc. (GS)":
        name = "Goldman Sachs"
    if name == "Pfizer Inc. (PFE)":
        name = "Pfizer"
    if name == "Johnson & Johnson (JNJ)":
        name = "Johnson & Johnson"
    if name == "Bristol-Myers Squibb Company (BMY)":
        name = "Bristol-Myers"
    if name == "Ford Motor Company (F)":
        name = "Ford"
    if name == "General Motors Company (GM)":
        name = "General Motors"
    if name == "The Boeing Company (BA)":
        name = "Boeing"
    if name == "Toyota Motor Corporation (TM)":
        name = "Toyota"
    if name == "Lockheed Martin Corporation (LMT)":
        name = "Lockheed Martin"
    if name == "Honeywell International Inc. (HON)":
        name = "Honeywell"
    if name == "Chevron Corporation (CVX)":
        name = "Chevron"
    if name == "Shell plc (SHEL)":
        name = "Shell"
    if name == "BP p.l.c. (BP)":
        name = "BP"
    if name == "Exxon Mobil Corporation (XOM)":
        name = "Exxon Mobil"
    if name == "NVIDIA Corporation (NVDA)":
        name = "NVIDIA"
    if name == "QUALCOMM Incorporated (QCOM)":
        name = "QUALCOMM"
    if name == "Advanced Micro Devices, Inc. (AMD)":
        name = "AMD"
    if name == "Tesla, Inc. (TSLA)":
        name = "Tesla"
    if name == "Alphabet Inc. (GOOG)":
        name = "Google"
    if name == "Meta Platforms, Inc. (META)":
        name = "Meta Platforms"
    if name == "Amazon.com, Inc. (AMZN)":
        name = "Amazon"
    if name == "Apple Inc. (AAPL)":
        name = "Apple"
    if name == "Netflix, Inc. (NFLX)":
        name = "Netflix"
    return name


def get_normalized_name_rus(name):
    if name == "ПАО НК РОСНЕФТЬ":
        name = "РОСНЕФТЬ"
    if name == 'ПАО "НОВАТЭК" АО':
        name = "НОВАТЭК"
    if name == 'ГМК "НОР.НИКЕЛЬ" ПАО АО':
        name = "НОР.НИКЕЛЬ"
    if name == "ФОСАГРО ПАО АО":
        name = "ФОСАГРО"
    if name == 'ПАО "НЛМК" АО':
        name = "НЛМК"
    if name == "АКРОН ПАО АО":
        name = "АКРОН"
    if name == "United Company RUSAL PLC":
        name = "RUSAL"
    if name == "АЛРОСА ПАО АО":
        name = "АЛРОСА"
    if name == "ГРУППА ПОЗИТИВ АО":
        name = "ПОЗИТИВ"
    if name == "СЕГЕЖА АО":
        name = "СЕГЕЖА"
    if name == "ПАО ДЕТСКИЙ МИР":
        name = "ДЕТСКИЙ МИР"
    if name == "ПИК СЗ (ПАО) АО":
        name = "ПИК"
    else:
        name = name
    return name


def get_price_market_for_america(item):
    mytable = PrettyTable()
    mytable.field_names = ["компания ", "цена 💰", "📈 $", "📉 %"]
    ses = requests.Session()
    try:
        for i in item:
            url = f"https://finance.yahoo.com/quote/{i}"

            respons = ses.get(url, headers=headers)
            soup = BeautifulSoup(respons.text, "html.parser")

            name = soup.find("h1", class_="D(ib) Fz(18px)").text
            name = get_normalized_name(name)
            price = soup.find(
                "fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)"
            ).text
            changes = soup.find_all(
                "fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)"
            )
            lst_changes = [i.text for i in changes if i.find("span")]
            dollar_change = lst_changes[0]
            percent_change = lst_changes[1]
            lst = []
            lst.extend([name, price, dollar_change, percent_change])
            mytable.add_row(lst)

    except Exception:
        mytable.add_row(["Что-то", "пошло", "не так", "!"])
    return f"<pre>{datetime.now()}\n{mytable}</pre>"


def get_price_market_for_russia():
    """Получение списка российских акций"""
    mytable = PrettyTable()
    mytable.field_names = ["компания ", "цена 💰", "📈 rub", "📉 %"]
    try:
        ses = requests.Session()
        response = ses.get(
            f"https://ru.tradingview.com/markets/stocks-russia/market-movers-large-cap/",
            headers=headers,
        )
        soup = BeautifulSoup(response.text, "html.parser")

        # список данных для извлечении имен
        list_data_names = soup.find_all("tr", class_="row-EdyDtqqh listRow")
        # список имен
        list_names = [
            i.find("sup", class_="apply-common-tooltip tickerDescription-hMpTPJiS").text
            for i in list_data_names
        ]
        # список данных для извлечении данных
        list_data_price = soup.find_all("td", class_="cell-TKkxf89L right-TKkxf89L")
        # список данных
        list_data = [i.text for i in list_data_price]
        lst = []
        # разбивка данных на коллекции
        while len(list_data) > 0:
            item = list_data[:9]
            lst.append(item)
            list_data = list_data[9:]

        ready_data = zip(list_names, lst)
        # извлечение и добавлении данных в таблицу
        for i in [i for i in ready_data]:
            name = i[0]
            price = i[1][1][:-3]

            percent_change = i[1][2]

            rub_change = i[1][3][:-3]
            data_table = []
            if name in allow_name:
                data_table.extend(
                    [get_normalized_name_rus(name), price, rub_change, percent_change]
                )
                mytable.add_row(data_table)
    except Exception:
        mytable.add_row(["Что-то", "пошло", "не так", "!"])

    return f"<pre>{datetime.now()}\n{mytable}</pre>"
