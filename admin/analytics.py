import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from sqlalchemy import func, text
from bot.handlers import current_user
from bot import server, app, db


#data = pd.read_sql_table('current_balance', 'sqlite:///database.db')

# data = text('SELECT strftime("%Y-%m-%d",date),transport,food,entertainment,clothes,present,health,hobby,other FROM  current_balance GROUP BY date')

# выборка данных по категориям трат
data_present = [i for i in db.engine.execute(text('SELECT strftime("%Y-%m-%d",date),present FROM  current_balance GROUP BY date'))]
data_food = [i for i in db.engine.execute(text('SELECT strftime("%Y-%m-%d",date),food FROM  current_balance GROUP BY date'))]
data_entertainment = [i for i in db.engine.execute(text('SELECT strftime("%Y-%m-%d",date),entertainment FROM  current_balance GROUP BY date'))]
data_transport = [i for i in db.engine.execute(text('SELECT strftime("%Y-%m-%d",date),transport FROM current_balance GROUP BY date'))]
data_clothes = [i for i in db.engine.execute(text('SELECT strftime("%Y-%m-%d",date),clothes FROM  current_balance GROUP BY date'))]
data_health = [i for i in db.engine.execute(text('SELECT strftime("%Y-%m-%d",date),health FROM  current_balance GROUP BY date'))]
data_hobby = [i for i in db.engine.execute(text('SELECT strftime("%Y-%m-%d",date),hobby FROM  current_balance GROUP BY date'))]
data_other = [i for i in db.engine.execute(text('SELECT strftime("%Y-%m-%d",date),other FROM  current_balance GROUP BY date'))]

# данные для семидневного отчета
data_weekly_report = db.engine.execute(text('SELECT SUM(food),SUM(entertainment),SUM(transport),SUM(clothes),SUM(present),SUM(health),SUM(hobby),SUM(other) FROM current_balance ORDER BY date DESC LIMIT 7'))

weekly_report = [*data_weekly_report]
total_spend_week = sum(*weekly_report)
max_status_index =max(*weekly_report)

for index,_ in enumerate(weekly_report[0]):
    if _ == max_status_index:
        max_status = index

if max_status == 0:
    str_max_status = 'транспорт'
if max_status == 1:
    str_max_status = 'еда'
if max_status == 2:
    str_max_status = 'развлечения'
if max_status == 3:
    str_max_status = 'одежда'
if max_status == 4:
    str_max_status = 'подарки'
if max_status == 5:
    str_max_status = 'здоровье'
if max_status == 6:
    str_max_status = 'хобби'
if max_status == 7:
    str_max_status = 'прочее'


sl_present = {}
sl_food = {}
sl_entertainment = {}
sl_transport = {}
sl_clothes = {}
sl_health = {}
sl_hobby = {}
sl_other = {}

# формирование словарей с данными для отображения
for i in data_present:
    sl_present[i[0]]=i[1]

for i in data_food:
    sl_food[i[0]]=i[1]

for i in data_entertainment:
    sl_entertainment[i[0]]=i[1]

for i in data_transport:
    sl_transport[i[0]]=i[1]

for i in data_clothes:
    sl_clothes[i[0]]=i[1]

for i in data_health:
    sl_health[i[0]]=i[1]

for i in data_hobby:
    sl_hobby[i[0]]=i[1]

for i in data_other:
    sl_other[i[0]]=i[1]


app.layout = html.Div([
    html.Div([
        html.Div(
            [
                html.H1(id="my-header", className="text-center"),
            ],
            className="col-md-12",
        )
    ],
    className="row",
    ),
    html.A("Войти", id="login-link", href="/login"),
            html.Div(id="my-div", className="text-center"),
            html.Button(
                id="submit-button-state",
                n_clicks=1,
                children="Submit",
                style={"display": "none"},
            ),
    html.Div([
        html.H1('Динамика расходов')
    ], style={
        'font-family': 'monospace',
        'margin-left': '35%',
    }),

    dcc.Graph(
        id='graph',
        figure={
            'data': [
                {
                    'x': [*sl_present.keys()],
                    'y': [*sl_present.values()],
                    'type': 'line',
                    'name': 'Подарки'
                },
                {
                    'x': [*sl_food.keys()],
                    'y': [*sl_food.values()],
                    'type': 'line',
                    'name': 'Еда'
                },
                {
                    'x': [*sl_entertainment.keys()],
                    'y': [*sl_entertainment.values()],
                    'type': 'line',
                    'name': 'Развлечения'
                },
                {
                    'x': [*sl_transport.keys()],
                    'y': [*sl_transport.values()],
                    'type': 'line',
                    'name': 'Транспорт'
                },
                {
                    'x': [*sl_clothes.keys()],
                    'y': [*sl_clothes.values()],
                    'type': 'line',
                    'name': 'Одежда'
                },
                {
                    'x': [*sl_health.keys()],
                    'y': [*sl_health.values()],
                    'type': 'line',
                    'name': 'Здоровье'
                },
                {
                    'x': [*sl_hobby.keys()],
                    'y': [*sl_hobby.values()],
                    'type': 'line',
                    'name': 'Хобби'
                },
                {
                    'x': [*sl_other.keys()],
                    'y': [*sl_other.values()],
                    'type': 'line',
                    'name': 'Прочее '
                },
            ],
            "layout": {"title": "категории трат"},
        }
    ),

    html.Div([
        html.H4('Общий расход за 7 дней: '),
        html.Code([
            html.P(f"{total_spend_week} рублей"),
            html.P(f"Самая затратная категория: {str_max_status}")
        ], style={
            'color': 'blue'
        })
    ], style={
        'font-family': 'monospace',
        'margin-left': '15%',
        'font-size': '20px'
    }),

])

