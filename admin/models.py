from bot import db
from flask_login import UserMixin


class AdminUser(db.Model, UserMixin):
    __tablename__ = "adminuser"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default="admin")
    psw = db.Column(db.String(50), default="admin")

    def __str__(self):
        return self.name


# admin = AdminUser()
# db.session.add(admin)
# db.session.commit()
db.create_all()
