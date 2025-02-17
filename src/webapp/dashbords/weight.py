from flask import session, current_app as current_flask_app
from dash import dcc, html
from datetime import datetime
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from src.webapp.dashbords.base import DashboardManager, StyleDash
from flask_login import current_user
from src.services.weight import WeightDashbordService
from config import settings


def get_weight_analytics(current_flask_app):
    def show_content():
        """Получение и отрисовка данных."""
        weight_manager = WeightDashbordService(current_user.telegram_id)

        data_weight = weight_manager.get_all_weight_by_telegram_id()
        list_timestamp = sorted(set([i[1] for i in data_weight]))

        try:
            # хранение отрезка, в случае удаления в web точки отрезка
            session['start_date'] = list_timestamp[0].strftime('%Y-%m-%d')
            session['end_date'] = list_timestamp[-1].strftime('%Y-%m-%d')
        except IndexError:
            # TODO: залогировать
            print('Нет записи')
            session['start_date'] = datetime.now().date()
            session['end_date'] = datetime.now().date()

        fig = go.Figure()
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(255, 255, 255, 1)',
            font=dict(color='black'),
        )

        fig.add_trace(
            go.Scatter(
                x=list_timestamp,
                y=[i[0] for i in data_weight],
                mode='lines',
                name='ВЕС',
            )
        )
        last_measurement = data_weight[-1][0] if data_weight else '-'
        content = html.Div(
            [
                html.H2(
                    [
                        html.A(
                            'НАЗАД',
                            href='/admin',
                            style=StyleDash.back_button_style,
                        ),
                    ],
                ),
                html.H2(f'Последнее измерение: {last_measurement}'),
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
                dcc.Graph(
                    id='weight-graph', figure=fig, style={'height': '600px'}
                ),
            ]
        )

        return content

    app = DashboardManager(
        __name__, current_flask_app, settings.DASHBOARD_WEIGHT, show_content
    ).app

    @app.callback(
        [
            Output('weight-graph', 'figure', allow_duplicate=True),
        ],
        [
            Input('start-date-dropdown', 'value'),
            Input('end-date-dropdown', 'value'),
        ],
        prevent_initial_call=True,
    )
    def update_graph(start_date, end_date):
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

        weight_manager = WeightDashbordService(current_user.telegram_id)
        data_weight = weight_manager.get_all_weight_by_telegram_id()

        fig = go.Figure()

        date_time = []
        values_expanses = []

        for v in data_weight:
            target_date = v[1]
            expense_item = v[0]
            if start_date <= target_date <= end_date:
                date_time.append(target_date)
                values_expanses.append(expense_item)

        fig.add_trace(
            go.Scatter(
                x=sorted(date_time),
                y=values_expanses,
                mode='lines',
                name='ВЕС',
            )
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            legend=dict(
                orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1
            ),
        )

        return [fig]


get_weight_analytics(current_flask_app)
