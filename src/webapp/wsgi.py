import os

from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_babel import Babel
from flask_ckeditor import CKEditor
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from config import get_config
from src.database.models.users import User


def create_app():
    app = Flask(__name__)
    ckeditor = CKEditor()

    config = get_config()
    app.config.from_object(config)
    ckeditor.init_app(app)

    with app.app_context():
        from src.webapp.admin import admin
        from src.webapp.dashbords import expenses, weight

        return app


login_manager = LoginManager()


def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(['de', 'fr', 'en'])


def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


babel = Babel(locale_selector=get_locale, timezone_selector=get_timezone)

app = create_app()

babel.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon',
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hi man'


@app.route('/login', methods=['GET', 'POST'])
def login():
    check_mobile = 'mobile' in request.query_string.decode('utf-8')
    if request.method == 'POST':
        user = User.get_user_by_username(request.form['name'])
        if user:
            check = check_password_hash(user.psw, request.form['psw'])
            if check:
                login_user(user)
                flash('Добро пожаловать!')
                next_link = request.args.get('next')
                return redirect(next_link or url_for('admin.index', check_mobile=check_mobile))

        flash('Пароль не верен!')
    if current_user.is_authenticated:
        return redirect(url_for('admin.index', check_mobile=check_mobile))
    else:
        flash('Введи пароль!')
    return render_template('login.html', title='Авторизация')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return 'Адрес не существует'


@app.errorhandler(403)
def not_allowed(error):
    return redirect('https://www.google.com/')
