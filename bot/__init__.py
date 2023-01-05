from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("config.TestConfig")
db = SQLAlchemy(app)

from . import handlers

db.create_all()
