from flask import session, current_app as current_flask_app
from dash import dcc, html
import time
from datetime import datetime
import plotly.graph_objects as go
from plotly.io import write_image
import plotly.express as px
from dash.dependencies import Input, Output
from src.webapp.dashbords.base import DashboardManager, StyleDash
from flask_login import current_user
from src.services.expenses import ExpensesDashbordService
from config import settings


def get_expense_analytics(current_flask_app):
    def save_graph_as_image(fig, pie_fig, user_name='_Unknown_'):
        """Сохраняет график в виде изображения."""
        # Настройка пути и формата файла
        timestamp = int(time.time())
        fig_path = f'{timestamp}-{user_name}-fig.png'
        pie_fig_path = f'{timestamp}-{user_name}-pie_fig.png'

        write_image(fig, fig_path)
        write_image(pie_fig, pie_fig_path)
        # TODO: заменить на логи
        print(f'Graph saved as {fig_path}')
        print(f'Graph saved as {pie_fig_path}')

    def show_content():
        """Получение и отрисовка данных."""

        expanses_manager = ExpensesDashbordService(current_user.telegram_id)
        mapa_expanses = {}
        total_money = []
        pie_fig_names = []
        pie_fig_values = []

        data_expanses = expanses_manager.get_all_expenses_by_telegram_id()
        list_timestamp = sorted(set([i[1] for i in data_expanses]))

        try:
            # хранение отрезка, в случае удаления в web точки отрезка
            session['start_date'] = list_timestamp[0].strftime('%Y-%m-%d')
            session['end_date'] = list_timestamp[-1].strftime('%Y-%m-%d')
        except IndexError:
            # TODO: залогировать
            print('Нет записи')
            session['start_date'] = datetime.now().date()
            session['end_date'] = datetime.now().date()

        for row in data_expanses:
            # отсортировать данные по категориям
            date = row[1]
            value_expenses = row[2]
            expense_item = row[0].value

            if expense_item not in mapa_expanses:
                mapa_expanses[expense_item] = [(date, value_expenses)]
            else:
                mapa_expanses[expense_item].append((date, value_expenses))

        fig = go.Figure()
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(255, 255, 255, 1)',
            font=dict(color='black'),
        )

        for expense_item, value_tuple in mapa_expanses.items():

            date_time = sorted([i[0] for i in value_tuple])
            date_time = [i.strftime('%m/%d/%Y') for i in date_time]

            values = [i[1] for i in value_tuple]
            total_money.append(sum(values))

            fig.add_trace(
                go.Scatter(
                    x=date_time,
                    y=values,
                    mode='lines',
                    name=expense_item,
                )
            )
            pie_fig_values.append(sum(values))
            pie_fig_names.append(expense_item)

        pie_fig = px.pie(
            values=pie_fig_values,
            names=pie_fig_names,
            hole=0.3,
        )

        content = html.Div(
            [
                dcc.Location(id='url', refresh=False),
                html.H2(
                    [
                        html.A(
                            'НАЗАД',
                            href='/admin',
                            style=StyleDash.back_button_style,
                        ),
                    ],
                ),
                html.H2(f'Ваши траты: {current_user.username}'),
                html.Div(
                    [
                        # Добавление выпадающего списка для выбора интервала начальной даты
                        html.Label(
                            # "Начало",
                            style={'margin-right': '10px', 'fontSize': '20px'},
                        ),
                        dcc.Dropdown(
                            id='start-date-dropdown',
                            options=[
                                {'label': f'С {date}', 'value': date}
                                for date in list_timestamp
                            ],
                            multi=False,
                            value=list_timestamp[0],
                            style=StyleDash.dropdown_style,
                        ),
                        # Добавление выпадающего списка для выбора интервала конечной даты
                        html.Label(
                            # "Конец",
                            style={'margin-right': '10px', 'fontSize': '20px'},
                        ),
                        dcc.Dropdown(
                            id='end-date-dropdown',
                            options=[
                                {'label': f'ДО {date}', 'value': date}
                                for date in list_timestamp
                            ],
                            multi=False,
                            value=list_timestamp[-1],
                            style=StyleDash.dropdown_style,
                        ),
                    ],
                    style={
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'padding': '2px 6px',
                    },
                ),
                html.Hr(),
                html.H1(
                    f'Потрачено за период: {sum(total_money)} 💰',
                    style={'textAlign': 'center'},
                    id='total',
                ),
                dcc.Graph(
                    id='expenses-graph', figure=fig, style={'height': '600px'}
                ),
                html.Br(),
                dcc.Graph(
                    id='expenses-pie',
                    figure=pie_fig,
                    style={
                        'background': 'repeating-linear-gradient(45deg, #f0f0f0, #f0f0f0 10px, white 10px, white 20px)',
                        'padding': '20px',
                        'border-radius': '10px',
                    },
                ),
            ]
        )

        return content

    app = DashboardManager(
        __name__,
        current_flask_app,
        settings.DASHBOARD_EXPENSE,
        show_content,
    ).app

    @app.callback(
        [
            Output('expenses-graph', 'figure'),
            Output('expenses-pie', 'figure'),
            Output('total', 'children'),
        ],
        [
            Input('url', 'pathname'),
            Input('start-date-dropdown', 'value'),
            Input('end-date-dropdown', 'value'),
        ],
        prevent_initial_call=True,
    )
    def update_graph(pathname, start_date, end_date):
        """Обновление дашборда."""
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except TypeError:
            string_start_date = session.get('start_date')
            string_end_date = session.get('end_date')

            start_date = (
                datetime.strptime(string_start_date, '%Y-%m-%d').date()
                if string_start_date
                else datetime.now().date()
            )
            end_date = (
                datetime.strptime(string_end_date, '%Y-%m-%d').date()
                if string_end_date
                else datetime.now().date()
            )

        expanses_manager = ExpensesDashbordService(current_user.telegram_id)
        total_money = []
        mapa_expanses = {}
        data_expanses = expanses_manager.get_all_expenses_by_telegram_id()
        pie_fig_values = []
        pie_fig_names = []

        for row in data_expanses:
            # отсортировать данные по категориям
            date = row[1]
            value_expenses = row[2]
            expense_item = row[0].value

            if expense_item not in mapa_expanses:
                mapa_expanses[expense_item] = [(date, value_expenses)]
            else:
                mapa_expanses[expense_item].append((date, value_expenses))

        fig = go.Figure()

        for name_line, value_tuple in mapa_expanses.items():
            date_time = []
            values_expanses = []

            for v in value_tuple:
                target_date = v[0]
                expense_item = v[1]
                if start_date <= target_date <= end_date:
                    date_time.append(target_date)
                    values_expanses.append(expense_item)

            total_money.append(sum(values_expanses))

            fig.add_trace(
                go.Scatter(
                    x=sorted(date_time),
                    y=values_expanses,
                    mode='lines',
                    name=name_line,
                )
            )
            pie_fig_values.append(sum(values_expanses))
            pie_fig_names.append(name_line)

        pie_fig = px.pie(
            values=pie_fig_values,
            names=pie_fig_names,
            hole=0.3,
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            legend=dict(
                orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1
            ),
        )
        check_for_picture = pathname.split('/')[-1]
        if check_for_picture == 'picture':
            # запрос для получения пикчи
            save_graph_as_image(fig, pie_fig)

        return [
            fig,
            pie_fig,
            html.H4(f'Всего потрачено {sum(total_money)} 💰', id='total'),
        ]


get_expense_analytics(current_flask_app)
