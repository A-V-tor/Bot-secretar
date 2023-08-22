import logging
from datetime import datetime

from flask import (
    Flask,
    flash,
    request,
    render_template,
    redirect,
    url_for,
    session,
)
from flask_login import LoginManager, login_user, logout_user, current_user
from project.database.database import db
from werkzeug.security import check_password_hash
from project.database.models import MyWeight
from flask_babelex import Babel
from project.adminpanel.admin.models import AdminUser
from sqlalchemy import select


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.DevelopConfig')

    with app.app_context():
        from project.adminpanel.admin import admin

        return app


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
filehandler = logging.FileHandler('flask-logs.log')
logger.addHandler(filehandler)


login_manager = LoginManager()
babel = Babel()

app = create_app()

babel.init_app(app)
login_manager.init_app(app)


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'ru')


@login_manager.user_loader
def load_user(user_id):
    return db.query(AdminUser).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    date = datetime.now()
    logger.info(f'{date} Запрос с ip {request.access_route[0]}\n')
    logger.info(f'{request.user_agent}\n')
    logger.info(f'{request.cookies}\n\n')
    return 'Hi man'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        admin = (
            db.query(AdminUser).filter_by(name=request.form['name']).first()
        )
        check = check_password_hash(admin.psw, request.form['psw'])
        if check:
            login_user(admin)
            flash('Вы в системе!')
            next = request.args.get('next')
            return redirect(next or url_for('admin.index'))
        flash('Что-то не так')
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    else:
        flash('Введи пароль!')
    return render_template('login.html', title='Авторизация')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def pageNot(error):
    date = datetime.now()
    logger.error(
        f'{date} !!! Запрос с ip {request.access_route[0]} на несуществующий адрес {request.url}\n'
    )
    return 'Адрес не существует'


@app.errorhandler(403)
def notAllowed(error):
    date = datetime.now()
    logger.error(
        f'{date} !!! Запрос с ip {request.access_route[0]} на запрещеный адрес {request.url}\n'
    )
    return redirect('https://www.google.com/')


def web_run():
    app.run()


if __name__ == '__main__':
    app.run()
