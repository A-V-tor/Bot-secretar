import requests



token = '***************'



def get_weather(a =** , b=**):
    
    params = {f'lat' : {a}, 'lon' : {b}, 'appid' : token, 'units' : 'metric', 'lang' : 'ru'}
    response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
    res = response.json()
    
    # вынимаю из словаря нужные данные
    locality = res['name'] 
    description = res['weather'][0]['description'] 
    temp = (res['main']['temp_min'] + res['main']['temp_min'])/2 
    humidity = res['main']['humidity'] 
    pressure = res['main']['pressure'] 
    speed_wind = res['wind']['speed'] 
    gust_wind = res['wind']['gust']
    
    if description == 'пасмурно':
        g = '\u2600'
    if description == 'небольшой дождь':
        g = '\u2602'
    else:
        g = '\u2601'

     # добавил эмодзи для лучшего восприятия   
    p = f'населеный пункт:        \U0001F3D9{locality}\n\
небо:                               {g}{description}\n\
средняя температура:\U0001F321{temp}\u2103\n\
влажность воздуха:    \U0001F30A{humidity}%\n\
давление:                      \U0001F388{pressure} мм.рт.ст\n\
скорость ветра:            \U0001F32C{speed_wind} м\с\n\
порывы:                         \u21A0{gust_wind} м\с'
    
    return p


if __name__ == '__main__':
    print('погода запрошена')
    get_weather()
    
