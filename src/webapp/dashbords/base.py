from dash import Dash, html
from dash.dependencies import Input, Output
from flask_login import current_user
from dotenv import load_dotenv
import os

load_dotenv()


class DashboardManager:
    """Логика для создания приложений дашбордов."""

    login_url = os.getenv('URL_ADMIN')

    def __init__(self, name, server_name, url, func):
        self.func = func
        self.app = Dash(
            name,
            server=server_name,
            url_base_pathname=url,
        )

        self.app.layout = html.Div(
            children=[
                html.A('Войти', id='login-link', href=self.login_url),
                html.Div(id='my-div', className='text-center'),
                html.Button(
                    id='submit-button-state',
                    n_clicks=1,
                    children='Submit',
                    style={'display': 'none'},
                ),
            ]
        )

        self.app.callback(
            [
                Output('my-div', 'children'),
                Output('login-link', 'style'),
            ],
            [Input('submit-button-state', 'n_clicks')],
        )(self.authentication_check)

    def authentication_check(self, n_clicks):
        """Проверка аутенофикации юзера и получение данных"""
        if not hasattr(current_user, 'psw'):
            user_data = None
            link_style = {
                'display': 'inline-block',
                'border': '2px solid #4CAF50',
                'padding': '10px',
                'text-align': 'center',
                'box-shadow': '2px 2px 5px #888888',
                'color': '#4CAF50',
                'font-size': '16px',
                'font-weight': 'bold',
            }
        else:
            link_style = {'display': 'none'}
            user_data = self.func()
        return user_data, link_style


class StyleDash:
    """Общие стили для дашбордов."""

    dropdown_style = {
        'width': '50%',
        'background-color': 'white',
        'border': '1px solid #ccc',
        'border-radius': '4px',
        'padding': '8px 12px',
        'cursor': 'pointer',
        'font-size': '16px',
        'font-family': 'Arial, sans-serif',
        'background': 'linear-gradient(45deg, #f0f0f0 25%, #ffffff 25%, #ffffff 50%, #f0f0f0 50%, #f0f0f0 75%, #ffffff 75%, #ffffff)',
    }
    back_button_style = {
        'display': 'inline-block',
        'padding': '12px 30px',
        'background-color': 'transparent',
        'color': '#333',
        'text-decoration': 'none',
        'border': '2px solid #333',
        'border-radius': '25px',
        'font-size': '16px',
        'font-weight': '500',
        'text-transform': 'uppercase',
        'box-shadow': '0 2px 6px rgba(0, 0, 0, 0.1)',
        'transition': 'all 0.3s ease',
        'cursor': 'pointer',
    }
