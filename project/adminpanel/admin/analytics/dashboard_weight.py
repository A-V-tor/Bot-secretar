from project.database.database import db
from project.database.models import MyWeight
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from flask import current_app as current_flask_app
from .utils import DashboardManager


def get_weight_analytics(server):
    """Страница дашборда по весу."""

    window_size = 3

    def get_dataframe():
        """Создание датафрейма данных."""
        datalist = db.query(MyWeight).filter_by().all()
        timestamps = [i.date for i in datalist]
        values_weight = [i.text_value for i in datalist]
        group = pd.DataFrame({'дата': timestamps, 'значение': values_weight})

        # Вычисление скользящей средней для второй линии
        group['среднее'] = group['значение'].rolling(window=window_size).mean()

        return group

    config_layout = {
        'title': 'Отображение замеров',
        'yaxis_title': 'Вес в кг',
        'xaxis_title': 'Дата',
        'paper_bgcolor': 'rgba(124,252,0,0)',
        'plot_bgcolor': 'rgba(241, 231, 254, 1)',
        'legend': {
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': 1.02,
            'xanchor': 'right',
            'x': 1,
        },
    }

    def get_content():
        """Получение и отрисовка данных."""
        group = get_dataframe()
        fig = go.Figure()

        # Добавление первой линии
        fig.add_trace(
            go.Scatter(
                x=group['дата'],
                y=group['значение'],
                mode='lines',
                name='Текущий вес',
            )
        )
        # Добавление второй линии (скользящая средняя)
        fig.add_trace(
            go.Scatter(
                x=group['дата'],
                y=group['среднее'],
                mode='lines',
                line=dict(dash='dash', color='lightblue'),
                name='Скользящая средняя',
            )
        )

        # Обновление макета графика
        fig.update_layout(**config_layout)

        content = html.Div(
            [
                html.H2(
                    [
                        html.A('НАЗАД', href='/admin'),
                    ]
                ),
                dcc.Markdown(
                    """
                ## График веса:
                """
                ),
                # Флекс-контейнер для размещения списков в одной строке
                html.Div(
                    [
                        # Добавление выпадающего списка для выбора интервала начальной даты
                        html.Label(
                            'Начало',
                            style={'margin-right': '10px', 'fontSize': '20px'},
                        ),
                        dcc.Dropdown(
                            id='start-date-dropdown',
                            options=[
                                {'label': str(date), 'value': date}
                                for date in group['дата']
                            ],
                            multi=False,
                            value=group['дата'].iloc[0],
                            style={'width': '50%'},  # уменьшаем ширину
                        ),
                        # Добавление выпадающего списка для выбора интервала конечной даты
                        html.Label(
                            'Конец',
                            style={'margin-right': '10px', 'fontSize': '20px'},
                        ),
                        dcc.Dropdown(
                            id='end-date-dropdown',
                            options=[
                                {'label': str(date), 'value': date}
                                for date in group['дата']
                            ],
                            multi=False,
                            value=group['дата'].iloc[-1],
                            style={'width': '50%'},  # уменьшаем ширину
                        ),
                    ],
                    style={
                        'display': 'flex',
                        'justify-content': 'space-between',
                    },
                ),  # стили для флекс-контейнера
                # Добавление графика
                dcc.Graph(id='weight-graph', figure=fig),
            ]
        )

        return content

    app = DashboardManager(
        __name__, server, server.config['DASHBOARD_WEIGHT'], get_content
    ).app

    @app.callback(
        Output('weight-graph', 'figure'),
        [
            Input('start-date-dropdown', 'value'),
            Input('end-date-dropdown', 'value'),
        ],
    )
    def update_graph(start_date, end_date):
        """Обработка выставленных границ-значений."""
        group = get_dataframe()

        # Фильтрация данных по выбранному интервалу дат
        filtered_data = group[
            (group['дата'] >= start_date) & (group['дата'] <= end_date)
        ]

        # Обновление графика с новыми данными
        updated_fig = go.Figure()

        # Добавление первой линии
        updated_fig.add_trace(
            go.Scatter(
                x=filtered_data['дата'],
                y=filtered_data['значение'],
                mode='lines',
                name='Текущий вес',
            )
        )

        # Вычисление скользящей средней для второй линии
        updated_fig.add_trace(
            go.Scatter(
                x=filtered_data['дата'],
                y=filtered_data['значение'].rolling(window=window_size).mean(),
                mode='lines',
                line=dict(dash='dash', color='lightblue'),
                name='Скользящая средняя',
            )
        )

        # Обновление макета графика
        updated_fig.update_layout(**config_layout)

        return updated_fig


get_weight_analytics(current_flask_app)
