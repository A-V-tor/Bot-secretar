from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel


app = Flask(__name__)
app.config.from_object("config.TestConfig")
db = SQLAlchemy(app)
babel = Babel(app)

from . import handlers
from admin.admin import *

db.create_all()
