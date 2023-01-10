from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from dash import Dash


server = Flask(__name__)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(
    __name__,
    server=server,
    url_base_pathname="/admin/analytics/",
    external_stylesheets=external_stylesheets,
)

app2 = Dash(
    __name__,
    server=server,
    url_base_pathname="/admin/analytics/weight/",
    external_stylesheets=external_stylesheets,
)

server.config.from_object("config.TestConfig")
db = SQLAlchemy(server)
babel = Babel(server)

from . import handlers
from admin.admin import *
from admin.analytics import *

db.create_all()
