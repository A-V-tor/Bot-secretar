from flask import session, current_app as current_flask_app
from dash import dcc, html, callback, set_props
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.io import to_image, write_image
import plotly.express as px
from dash.dependencies import Input, Output
from src.webapp.dashbords.base import DashboardManager
from flask_login import current_user
from src.service.expenses import ExpensesDashbordService


class DashbordExpenses:
    dropdown_style = {
        "width": "50%",
        "background-color": "white",
        "border": "1px solid #ccc",
        "border-radius": "4px",
        "padding": "8px 12px",
        "cursor": "pointer",
        "font-size": "16px",
        "font-family": "Arial, sans-serif",
        "background": "linear-gradient(45deg, #f0f0f0 25%, #ffffff 25%, #ffffff 50%, #f0f0f0 50%, #f0f0f0 75%, #ffffff 75%, #ffffff)",
    }
    back_button_style = {
        "display": "inline-block",
        "padding": "12px 30px",
        "background-color": "transparent",
        "color": "#333",
        "text-decoration": "none",
        "border": "2px solid #333",
        "border-radius": "25px",
        "font-size": "16px",
        "font-weight": "500",
        "text-transform": "uppercase",
        "box-shadow": "0 2px 6px rgba(0, 0, 0, 0.1)",
        "transition": "all 0.3s ease",
        "cursor": "pointer",
    }

    def __init__(self, server) -> None:
        self.app = DashboardManager(
            __name__, server, "/admin/analytics/expense/", self.show_content
        ).app

    def show_content(self):
        """Получение и отрисовка данных."""

        expanses_manager = ExpensesDashbordService(current_user.telegram_id)
        mapa_expanses = {}
        total_money = []

        data_expanses = expanses_manager.get_all_expenses_by_telegram_id()
        list_timestamp = sorted(set([i[1] for i in data_expanses]))

        # хранение отрезка, в случае удаления в web точки отрезка
        session["start_date"] = list_timestamp[0].strftime("%Y-%m-%d")
        session["end_date"] = list_timestamp[-1].strftime("%Y-%m-%d")

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
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(255, 255, 255, 1)",
            font=dict(color="black"),
        )

        for expense_item, value_tuple in mapa_expanses.items():

            date_time = sorted([i[0] for i in value_tuple])
            date_time = [i.strftime("%m/%d/%Y") for i in date_time]

            values = [i[1] for i in value_tuple]
            total_money.append(sum(values))

            fig.add_trace(
                go.Scatter(
                    x=date_time,
                    y=values,
                    mode="lines",
                    name=expense_item,
                )
            )
        # save_graph_as_image(fig)
        content = html.Div(
            [
                html.H2(
                    [
                        html.A(
                            "НАЗАД",
                            href="/admin",
                            style=self.back_button_style,
                        ),
                    ],
                ),
                html.H2(f"Ваши траты: {current_user.username}"),
                html.Div(
                    [
                        # Добавление выпадающего списка для выбора интервала начальной даты
                        html.Label(
                            # "Начало",
                            style={"margin-right": "10px", "fontSize": "20px"},
                        ),
                        dcc.Dropdown(
                            id="start-date-dropdown",
                            options=[
                                {"label": f"С {date}", "value": date}
                                for date in list_timestamp
                            ],
                            multi=False,
                            value=list_timestamp[0],
                            style=self.dropdown_style,
                        ),
                        # Добавление выпадающего списка для выбора интервала конечной даты
                        html.Label(
                            # "Конец",
                            style={"margin-right": "10px", "fontSize": "20px"},
                        ),
                        dcc.Dropdown(
                            id="end-date-dropdown",
                            options=[
                                {"label": f"ДО {date}", "value": date}
                                for date in list_timestamp
                            ],
                            multi=False,
                            value=list_timestamp[-1],
                            style=self.dropdown_style,
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justify-content": "space-between",
                        "padding": "2px 6px",
                    },
                ),
                html.Hr(),
                html.H1(
                    f"Потрачено за период: {sum(total_money)}",
                    style={"textAlign": "center"},
                    id="total",
                ),
                dcc.Graph(id="expenses-graph", figure=fig, style={"height": "600px"}),
                html.Br(),
            ]
        )

        return content

    @callback(
        [
            Output("expenses-graph", "figure"),
            Output("total", "children"),
        ],
        [
            Input("start-date-dropdown", "value"),
            Input("end-date-dropdown", "value"),
        ],
    )
    @staticmethod
    def update_graph(start_date, end_date):
        """Обновление дашборда."""

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except TypeError:
            start_date = datetime.strptime(session.get("start_date"), "%Y-%m-%d").date()
            end_date = datetime.strptime(session.get("end_date"), "%Y-%m-%d").date()

        expanses_manager = ExpensesDashbordService(current_user.telegram_id)
        total_money = []
        mapa_expanses = {}
        data_expanses = expanses_manager.get_all_expenses_by_telegram_id()

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
        date_time = []

        for name_line, value_tuple in mapa_expanses.items():
            values_expanses = []

            for v in value_tuple:
                if start_date <= v[0] <= end_date:
                    date_time.append(v[0])
                    values_expanses.append(v[1])
            total_money.append(sum(values_expanses))

            fig.add_trace(
                go.Scatter(
                    x=sorted(date_time),
                    y=values_expanses,
                    mode="lines",
                    name=name_line,
                )
            )
            # не правильно отрабатвает проерить всю логику

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )

        return [fig, html.H4(f"Всего потрачено {sum(total_money)} ₽", id="total")]


def save_graph_as_image(fig):
    """Сохраняет график в виде изображения."""
    # Настройка пути и формата файла
    file_path = "plotly_graph.png"
    write_image(fig, file_path)

    print(f"Graph saved as {file_path}")


DashbordExpenses(current_flask_app)


"""
import os
import plotly.graph_objects as go
from plotly.io import write_image


# Создадим функцию для генерации графика и сохранения его как изображение
def save_graph_as_image(fig, file_path="plotly_graph.png"):
    write_image(fig, file_path)
    print(f"Graph saved as {file_path}")


# Генерация графика (пример)
def generate_expense_graph():
    sample_data = [1, 2, 3, 4, 5, 6, 1, 2, 3]
    sample_data1 = [12, 13, 12, 11, 13, 12, 14, 15, 18]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sample_data, y=sample_data1, mode='lines', name='здоровье'))

    # Сохраняем график как изображение
    file_path = "plotly_graph.png"
    save_graph_as_image(fig, file_path)
    return file_path


# Функция для обработки команды в боте
def send_graph(update, context):
    chat_id = update.message.chat_id
    file_path = generate_expense_graph()

    # Отправляем изображение в чат
    with open(file_path, 'rb') as f:
        context.bot.send_photo(chat_id=chat_id, photo=f)

    # Удаляем изображение после отправки
    os.remove(file_path)

"""
