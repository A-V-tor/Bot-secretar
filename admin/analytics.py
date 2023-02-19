import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from sqlalchemy import func, text
from bot.handlers import current_user
from bot import server, app, app2, app3, db


def get_data_spend(server):
    """График по тратам"""
    app.layout = html.Div(
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(id='my-header', className='text-center'),
                        ],
                    )
                ],
            ),
            html.A('Войти', id='login-link', href='/login'),
            html.Div(id='my-div', className='text-center'),
            html.Button(
                id='submit-button-state',
                n_clicks=1,
                children='Submit',
                style={'display': 'none'},
            ),
        ]
    )

    @app.callback(
        [
            Output(component_id='my-header', component_property='children'),
            Output(component_id='my-div', component_property='children'),
            Output(component_id='login-link', component_property='style'),
        ],
        [
            Input(
                component_id='submit-button-state',
                component_property='n_clicks',
            )
        ],
    )
    def get_user_name(n_clicks):
        check = hasattr(current_user, 'psw')
        if not check:
            welcome_msg = ''
            user_data = None
            link_style = {'display': '/login'}
            return welcome_msg, user_data, link_style
        if current_user.psw:
            welcome_msg = None
            user_data = get_analytics_data()
            link_style = {'display': 'none'}
            return welcome_msg, user_data, link_style
        return 'Your Princess is in another castle', ''

    def get_analytics_data():
        data_present = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),present FROM  current_balance GROUP BY date'
                )
            )
        ]
        data_food = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),food FROM  current_balance GROUP BY date'
                )
            )
        ]
        data_entertainment = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),entertainment FROM  current_balance GROUP BY date'
                )
            )
        ]
        data_transport = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),transport FROM current_balance GROUP BY date'
                )
            )
        ]
        data_clothes = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),clothes FROM  current_balance GROUP BY date'
                )
            )
        ]
        data_health = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),health FROM  current_balance GROUP BY date'
                )
            )
        ]
        data_hobby = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),hobby FROM  current_balance GROUP BY date'
                )
            )
        ]
        data_other = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),other FROM  current_balance GROUP BY date'
                )
            )
        ]

        # данные для семидневного отчета
        data_weekly_report = db.engine.execute(
            text(
                'SELECT SUM(food),SUM(entertainment),SUM(transport),SUM(clothes),SUM(present),SUM(health),SUM(hobby),SUM(other) FROM current_balance ORDER BY date DESC LIMIT 7'
            )
        )

        # статистика трат по последним семи дням ведения записей и самая затратная категория
        weekly_report = [*data_weekly_report]
        total_spend_week = sum(*weekly_report)
        max_status_index = max(*weekly_report)

        for index, _ in enumerate(weekly_report[0]):
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
            sl_present[i[0]] = i[1]

        for i in data_food:
            sl_food[i[0]] = i[1]

        for i in data_entertainment:
            sl_entertainment[i[0]] = i[1]

        for i in data_transport:
            sl_transport[i[0]] = i[1]

        for i in data_clothes:
            sl_clothes[i[0]] = i[1]

        for i in data_health:
            sl_health[i[0]] = i[1]

        for i in data_hobby:
            sl_hobby[i[0]] = i[1]

        for i in data_other:
            sl_other[i[0]] = i[1]
        return html.Div(
            [
                html.Div(id='body-div'),
                html.Div(
                    [html.H1('Динамика расходов')],
                    style={
                        'font-family': 'monospace',
                        'margin-left': '35%',
                    },
                ),
                html.A(
                    children='назад',
                    href='/admin/',
                    style={'fontSize': '20px'},
                ),
                dcc.Graph(
                    id='graph',
                    figure={
                        'data': [
                            {
                                'x': [*sl_present.keys()],
                                'y': [*sl_present.values()],
                                'type': 'line',
                                'name': 'Подарки',
                            },
                            {
                                'x': [*sl_food.keys()],
                                'y': [*sl_food.values()],
                                'type': 'line',
                                'name': 'Еда',
                            },
                            {
                                'x': [*sl_entertainment.keys()],
                                'y': [*sl_entertainment.values()],
                                'type': 'line',
                                'name': 'Развлечения',
                            },
                            {
                                'x': [*sl_transport.keys()],
                                'y': [*sl_transport.values()],
                                'type': 'line',
                                'name': 'Транспорт',
                            },
                            {
                                'x': [*sl_clothes.keys()],
                                'y': [*sl_clothes.values()],
                                'type': 'line',
                                'name': 'Одежда',
                            },
                            {
                                'x': [*sl_health.keys()],
                                'y': [*sl_health.values()],
                                'type': 'line',
                                'name': 'Здоровье',
                            },
                            {
                                'x': [*sl_hobby.keys()],
                                'y': [*sl_hobby.values()],
                                'type': 'line',
                                'name': 'Хобби',
                            },
                            {
                                'x': [*sl_other.keys()],
                                'y': [*sl_other.values()],
                                'type': 'line',
                                'name': 'Прочее ',
                            },
                        ],
                        'layout': {'title': 'категории трат'},
                    },
                ),
                dcc.Interval(
                    id='graph-update', interval=1 * 1000, n_intervals=0
                ),
                html.Div(
                    [
                        html.H4('Общий расход за 7 дней: '),
                        html.Code(
                            [
                                html.P(f'{total_spend_week} рублей'),
                                html.P(
                                    f'Самая затратная категория: {str_max_status}'
                                ),
                            ],
                            style={'color': 'blue'},
                        ),
                    ],
                    style={
                        'font-family': 'monospace',
                        'margin-left': '15%',
                        'font-size': '20px',
                    },
                ),
            ]
        )

    return app.server


def get_data_weight(server):
    """График по весу"""
    app2.layout = html.Div(
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(id='my-header', className='text-center'),
                        ],
                    )
                ],
            ),
            html.A('Войти', id='login-link', href='/login'),
            html.Div(id='my-div', className='text-center'),
            html.Button(
                id='submit-button-state',
                n_clicks=1,
                children='Submit',
                style={'display': 'none'},
            ),
        ]
    )

    @app2.callback(
        [
            Output(component_id='my-header', component_property='children'),
            Output(component_id='my-div', component_property='children'),
            Output(component_id='login-link', component_property='style'),
        ],
        [
            Input(
                component_id='submit-button-state',
                component_property='n_clicks',
            )
        ],
    )
    def get_user_name(n_clicks):
        check = hasattr(current_user, 'psw')
        if not check:
            welcome_msg = ''
            user_data = None
            link_style = {'display': '/login'}
            return welcome_msg, user_data, link_style
        if current_user.psw:
            welcome_msg = None
            user_data = get_analytics_data()
            link_style = {'display': 'none'}
            return welcome_msg, user_data, link_style
        return 'Your Princess is in another castle', ''

    def get_analytics_data():
        data_weight = [
            i
            for i in db.engine.execute(
                text('SELECT date,value FROM  myweight GROUP BY date')
            )
        ]
        sl = {}

        for i in data_weight:
            sl[i[0]] = i[1]

        return html.Div(
            [
                html.Div(id='body-div'),
                html.Div(
                    [html.H1('Динамика массы тела')],
                    style={
                        'font-family': 'monospace',
                        'margin-left': '35%',
                    },
                ),
                html.A(
                    children='назад',
                    href='/admin/',
                    style={'fontSize': '20px'},
                ),
                dcc.Graph(
                    id='graph',
                    figure={
                        'data': [
                            {
                                'x': [*sl.keys()],
                                'y': [*sl.values()],
                                'type': 'line',
                                'name': 'Подарки',
                            },
                        ],
                    },
                ),
                dcc.Interval(
                    id='graph-update', interval=1 * 1000, n_intervals=0
                ),
            ]
        )

    return app2.server


def get_data_nutrition(server):
    """График по учету бжу"""
    app3.layout = html.Div(
        children=[
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(id='my-header', className='text-center'),
                        ],
                    )
                ],
            ),
            html.A('Войти', id='login-link', href='/login'),
            html.Div(id='my-div', className='text-center'),
            html.Button(
                id='submit-button-state',
                n_clicks=1,
                children='Submit',
                style={'display': 'none'},
            ),
        ]
    )

    @app3.callback(
        [
            Output(component_id='my-header', component_property='children'),
            Output(component_id='my-div', component_property='children'),
            Output(component_id='login-link', component_property='style'),
        ],
        [
            Input(
                component_id='submit-button-state',
                component_property='n_clicks',
            )
        ],
    )
    def get_user_name(n_clicks):
        check = hasattr(current_user, 'psw')
        if not check:
            welcome_msg = ''
            user_data = None
            link_style = {'display': '/login'}
            return welcome_msg, user_data, link_style
        if current_user.psw:
            welcome_msg = None
            user_data = get_analytics_data()
            link_style = {'display': 'none'}
            return welcome_msg, user_data, link_style
        return 'Your Princess is in another castle', ''

    def get_analytics_data():
        data_proteins = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),SUM(proteins) FROM  nutrition GROUP BY strftime("%Y-%m-%d",date)'
                )
            )
        ]
        data_fats = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),SUM(fats) FROM  nutrition GROUP BY strftime("%Y-%m-%d",date)'
                )
            )
        ]
        data_carbohydrates = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),SUM(carbohydrates) FROM  nutrition GROUP BY strftime("%Y-%m-%d",date)'
                )
            )
        ]
        data_energy = [
            i
            for i in db.engine.execute(
                text(
                    'SELECT strftime("%Y-%m-%d",date),SUM(energy) FROM  nutrition GROUP BY strftime("%Y-%m-%d",date)'
                )
            )
        ]

        sl_proteins = {}
        sl_fats = {}
        sl_carbohydrates = {}
        sl_energy = {}

        for i in data_proteins:
            sl_proteins[i[0]] = i[1]

        for i in data_fats:
            sl_fats[i[0]] = i[1]

        for i in data_carbohydrates:
            sl_carbohydrates[i[0]] = i[1]

        for i in data_energy:
            sl_energy[i[0]] = i[1]

        return html.Div(
            [
                html.Div(id='body-div'),
                html.Div(
                    [html.H1('Учет БЖУ')],
                    style={
                        'font-family': 'monospace',
                        'margin-left': '35%',
                    },
                ),
                html.A(
                    children='назад',
                    href='/admin/',
                    style={'fontSize': '20px'},
                ),
                dcc.Graph(
                    id='graph',
                    figure={
                        'data': [
                            {
                                'x': [*sl_proteins.keys()],
                                'y': [*sl_proteins.values()],
                                'type': 'line',
                                'name': 'Белки',
                            },
                            {
                                'x': [*sl_fats.keys()],
                                'y': [*sl_fats.values()],
                                'type': 'line',
                                'name': 'Жиры',
                            },
                            {
                                'x': [*sl_carbohydrates.keys()],
                                'y': [*sl_carbohydrates.values()],
                                'type': 'line',
                                'name': 'Углеводы',
                            },
                            {
                                'x': [*sl_energy.keys()],
                                'y': [*sl_energy.values()],
                                'type': 'line',
                                'name': 'Калории',
                            },
                        ],
                    },
                ),
                dcc.Interval(
                    id='graph-update', interval=1 * 1000, n_intervals=0
                ),
            ]
        )

    return app3.server


get_data_spend(server)
get_data_weight(server)
get_data_nutrition(server)
