from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy import Integer, String, Column, event
from sqlalchemy.orm import DeclarativeBase


class BaseAdmin(DeclarativeBase):
    pass


class AdminUser(BaseAdmin, UserMixin):
    __tablename__ = 'adminuser'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), default='admin', unique=True)
    psw = Column(String(128), default='admin')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.psw = generate_password_hash(kwargs.get('psw'))

    def __str__(self):
        return self.name


# хеширование пароля в админке
@event.listens_for(AdminUser, 'before_insert')
def hash_password(mapper, connection, target):
    target.psw = generate_password_hash(target.psw)
