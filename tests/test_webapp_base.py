import os

from dotenv import load_dotenv

from src.database import User

load_dotenv()


class TestWebAppBase:
    def test_login(self, client):
        generate_psw = User.create_user(username='User', telegram_id=111111111)
        response = client.post('/login', data={'name': 'User', 'psw': generate_psw}, follow_redirects=True)
        assert 'Добро пожаловать!' in response.data.decode('utf-8')

    def test_logout(self, client):
        response = client.get('/logout', follow_redirects=True)
        assert 'Введи пароль!' in response.data.decode('utf-8')

    def test_dashboards(self, client):
        url = os.getenv('DASHBOARD_EXPENSE')
        response = client.get(url)
        assert 'Dash' in response.data.decode('utf-8')

        url = os.getenv('DASHBOARD_WEIGHT')
        response = client.get(url)
        assert 'Dash' in response.data.decode('utf-8')

    def test_admin_url(self, client):
        response = client.get('/admin')
        assert response.status_code == 308
