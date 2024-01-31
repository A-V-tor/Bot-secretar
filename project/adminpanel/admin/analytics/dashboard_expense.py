from project.database.database import db
from project.database.models import DayReport, MyWeight
from dash import dcc, html
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
from flask import current_app as current_flask_app
from .utils import DashboardManager


def get_expense_analytics(server):
    """Страница дашборда по расходам."""

    def get_sample_results() -> dict:
        """Получение словаря с выборками."""
        datalist = db.query(DayReport).filter_by().all()
        timestamps = [i.date for i in datalist]

        # данные для линейного график отражающего все значения
        health = [i.health for i in datalist]
        transport = [i.transport for i in datalist]
        food = [i.food for i in datalist]
        entertainment = [i.entertainment for i in datalist]
        purchases = [i.purchases for i in datalist]
        present = [i.present for i in datalist]
        other = [i.other for i in datalist]

        res = {
            'timestamps': timestamps,
            'health': health,
            'transport': transport,
            'food': food,
            'entertainment': entertainment,
            'purchases': purchases,
            'present': present,
            'other': other,
        }

        return res

    def get_dataframe(datadict):
        """Создание датафрейма данных."""
        df = pd.DataFrame(
            {
                'дата': datadict['timestamps'],
                'здоровье': datadict['health'],
                'транспорт': datadict['transport'],
                'еда': datadict['food'],
                'развлечения': datadict['entertainment'],
                'покупки': datadict['purchases'],
                'подарки': datadict['present'],
                'прочее': datadict['other'],
            }
        )

        return df

    def get_not_null_values(map_data: dict, category: str) -> list:
        """Оставить только не нулевые значения."""
        res = [i for i in map_data[category] if i != 0]
        return res

    def get_content():
        """Получение и отрисовка данных."""
        sample_data = get_sample_results()
        group = get_dataframe(sample_data)

        # выборка с исключением нулевых значений
        health_true = get_not_null_values(sample_data, 'health')
        transport_true = get_not_null_values(sample_data, 'transport')
        food_true = get_not_null_values(sample_data, 'food')
        entertainment_true = get_not_null_values(sample_data, 'entertainment')
        purchases_true = get_not_null_values(sample_data, 'purchases')
        present_true = get_not_null_values(sample_data, 'present')
        other_true = get_not_null_values(sample_data, 'other')

        # суммирование значение по категориям
        total_health = sum(health_true)
        total_transport = sum(transport_true)
        total_food = sum(food_true)
        total_entertainment = sum(entertainment_true)
        total_purchases = sum(purchases_true)
        total_present = sum(present_true)
        total_other = sum(other_true)

        # данные показывающие средние траты по категориям
        avg_health = (
            sum(health_true) / len(health_true) if len(health_true) > 0 else 0
        )
        avg_transport = (
            sum(transport_true) / len(transport_true)
            if len(transport_true) > 0
            else 0
        )
        avg_food = sum(food_true) / len(food_true) if len(food_true) > 0 else 0
        avg_entertainment = (
            sum(entertainment_true) / len(entertainment_true)
            if len(entertainment_true) > 0
            else 0
        )
        avg_purchases = (
            sum(purchases_true) / len(purchases_true)
            if len(purchases_true) > 0
            else 0
        )
        avg_present = (
            sum(present_true) / len(present_true)
            if len(present_true) > 0
            else 0
        )
        avg_other = (
            sum(other_true) / len(other_true) if len(other_true) > 0 else 0
        )

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=group['дата'],
                y=group['здоровье'],
                mode='lines',
                name='здоровье',
            )
        )
        fig.add_trace(
            go.Scatter(
                x=group['дата'],
                y=group['транспорт'],
                mode='lines',
                name='транспорт',
            )
        )
        fig.add_trace(
            go.Scatter(
                x=group['дата'], y=group['еда'], mode='lines', name='еда'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=group['дата'],
                y=group['развлечения'],
                mode='lines',
                name='развлечения',
            )
        )
        fig.add_trace(
            go.Scatter(
                x=group['дата'],
                y=group['покупки'],
                mode='lines',
                name='покупки',
            )
        )
        fig.add_trace(
            go.Scatter(
                x=group['дата'],
                y=group['подарки'],
                mode='lines',
                name='подарки',
            )
        )
        fig.add_trace(
            go.Scatter(
                x=group['дата'], y=group['прочее'], mode='lines', name='прочее'
            )
        )

        list_sum_values = [
            total_health,
            total_transport,
            total_food,
            total_entertainment,
            total_purchases,
            total_present,
            total_other,
        ]
        list_avg_values = [
            avg_health,
            avg_transport,
            avg_food,
            avg_entertainment,
            avg_purchases,
            avg_present,
            avg_other,
        ]
        total = sum(list_sum_values)

        pie_fig = px.pie(
            values=list_sum_values, names=list(group.keys())[1:], hole=0.3
        )
        avg_fig = px.bar(x=list(group.keys())[1:], y=list_avg_values)

        content = html.Div(
            [
                html.H2(
                    [
                        html.A('НАЗАД', href='/admin'),
                    ]
                ),
                html.H1(f'Аналитика по тратам', style={'textAlign': 'center'}),
                html.Br(),
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
                html.Hr(),
                # Добавление графика
                dcc.Graph(id='expenses-graph', figure=fig),
                html.H3(
                    f'Всего потрачено {total} ₽',
                    style={'textAlign': 'center'},
                    id='total',
                ),
                dcc.Graph(id='expenses-pie', figure=pie_fig),
                html.H2(
                    f'Средний чек по категории', style={'textAlign': 'center'}
                ),
                dcc.Graph(id='expenses-avg', figure=avg_fig),
            ]
        )

        return content

    app = DashboardManager(
        __name__, server, server.config['DASHBOARD_EXPENSE'], get_content
    ).app

    @app.callback(
        [
            Output('expenses-graph', 'figure'),
            Output('expenses-pie', 'figure'),
            Output('expenses-avg', 'figure'),
            Output('total', 'children'),
        ],
        [
            Input('start-date-dropdown', 'value'),
            Input('end-date-dropdown', 'value'),
        ],
    )
    def update_graph(start_date, end_date):
        sample_data = get_sample_results()
        group = get_dataframe(sample_data)

        # Преобразование строковых дат в объекты datetime.date
        start_date = (
            datetime.strptime(start_date, '%Y-%m-%d').date()
            if start_date
            else None
        )
        end_date = (
            datetime.strptime(end_date, '%Y-%m-%d').date()
            if end_date
            else None
        )

        # Фильтрация данных по выбранному интервалу дат
        filtered_data = group[
            (group['дата'] >= start_date) & (group['дата'] <= end_date)
        ]

        # Обновление графика с новыми filtered_data
        updated_fig = go.Figure()

        updated_fig.add_trace(
            go.Scatter(
                x=filtered_data['дата'],
                y=filtered_data['здоровье'],
                mode='lines',
                name='здоровье',
            )
        )
        updated_fig.add_trace(
            go.Scatter(
                x=filtered_data['дата'],
                y=filtered_data['транспорт'],
                mode='lines',
                name='транспорт',
            )
        )
        updated_fig.add_trace(
            go.Scatter(
                x=filtered_data['дата'],
                y=filtered_data['еда'],
                mode='lines',
                name='еда',
            )
        )
        updated_fig.add_trace(
            go.Scatter(
                x=filtered_data['дата'],
                y=filtered_data['развлечения'],
                mode='lines',
                name='развлечения',
            )
        )
        updated_fig.add_trace(
            go.Scatter(
                x=filtered_data['дата'],
                y=filtered_data['покупки'],
                mode='lines',
                name='покупки',
            )
        )
        updated_fig.add_trace(
            go.Scatter(
                x=filtered_data['дата'],
                y=filtered_data['подарки'],
                mode='lines',
                name='подарки',
            )
        )
        updated_fig.add_trace(
            go.Scatter(
                x=filtered_data['дата'],
                y=filtered_data['прочее'],
                mode='lines',
                name='прочее',
            )
        )

        # выборка с исключением нулевых значений
        health_true = get_not_null_values(filtered_data, 'здоровье')
        transport_true = get_not_null_values(filtered_data, 'транспорт')
        food_true = get_not_null_values(filtered_data, 'еда')
        entertainment_true = get_not_null_values(filtered_data, 'развлечения')
        purchases_true = get_not_null_values(filtered_data, 'покупки')
        present_true = get_not_null_values(filtered_data, 'подарки')
        other_true = get_not_null_values(filtered_data, 'прочее')

        # данные для круговой диаграммы суммирующей траты
        total_health = sum(health_true)
        total_transport = sum(transport_true)
        total_food = sum(food_true)
        total_entertainment = sum(entertainment_true)
        total_purchases = sum(purchases_true)
        total_present = sum(present_true)
        total_other = sum(other_true)

        # данные показывающие средние траты по категориям
        avg_health = (
            sum(health_true) / len(health_true) if len(health_true) > 0 else 0
        )
        avg_transport = (
            sum(transport_true) / len(transport_true)
            if len(transport_true) > 0
            else 0
        )
        avg_food = sum(food_true) / len(food_true) if len(food_true) > 0 else 0
        avg_entertainment = (
            sum(entertainment_true) / len(entertainment_true)
            if len(entertainment_true) > 0
            else 0
        )
        avg_purchases = (
            sum(purchases_true) / len(purchases_true)
            if len(purchases_true) > 0
            else 0
        )
        avg_present = (
            sum(present_true) / len(present_true)
            if len(present_true) > 0
            else 0
        )
        avg_other = (
            sum(other_true) / len(other_true) if len(other_true) > 0 else 0
        )

        list_sum_values = [
            total_health,
            total_transport,
            total_food,
            total_entertainment,
            total_purchases,
            total_present,
            total_other,
        ]
        list_avg_values = [
            avg_health,
            avg_transport,
            avg_food,
            avg_entertainment,
            avg_purchases,
            avg_present,
            avg_other,
        ]
        total = sum(list_sum_values)

        pie_fig = px.pie(
            values=list_sum_values,
            names=list(filtered_data.keys())[1:],
            hole=0.3,
        )

        avg_fig = px.bar(x=list(filtered_data.keys())[1:], y=list_avg_values)
        avg_fig.update_layout(
            yaxis_title='Значение в ₽',
            xaxis_title='Категории',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            legend=dict(
                orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1
            ),
        )

        # Обновление макета графика
        updated_fig.update_layout(
            title='Отображение замеров',
            yaxis_title='Значение в ₽',
            xaxis_title='Дата',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            legend=dict(
                orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1
            ),
        )

        return (
            updated_fig,
            pie_fig,
            avg_fig,
            html.H4(f'Всего потрачено {total} ₽', id='total'),
        )


get_expense_analytics(current_flask_app)
