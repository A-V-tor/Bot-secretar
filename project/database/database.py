from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///project/database/database.db')
db = Session(engine)
