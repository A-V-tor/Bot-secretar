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
        self.app = Dash(name, server=server_name, url_base_pathname=url)

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
