import datetime

from prettytable import PrettyTable

from bot import db


class CurrentBalance(db.Model):
    """Текущий баланс"""

    __tablename__ = 'current_balance'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    transport = db.Column(db.Integer, default=0)
    food = db.Column(db.Integer, default=0)
    entertainment = db.Column(db.Integer, default=0)
    clothes = db.Column(db.Integer, default=0)
    present = db.Column(db.Integer, default=0)
    health = db.Column(db.Integer, default=0)
    hobby = db.Column(db.Integer, default=0)
    other = db.Column(db.Integer, default=0)

    def get_balance(self):
        mytable = PrettyTable()
        mytotaltable = PrettyTable()
        mytable.field_names = ['категория  ✇', 'расход 🏦']
        mytotaltable.field_names = ['ОБЩИЙ РАСХОД']

        mytable.add_row(['развлечения', str(self.entertainment)])
        mytable.add_row(['транспорт  ', str(self.transport)])
        mytable.add_row(['здоровье   ', str(self.health)])
        mytable.add_row(['подарки    ', str(self.present)])
        mytable.add_row(['одежда     ', str(self.clothes)])
        mytable.add_row(['прочее     ', str(self.other)])
        mytable.add_row(['хобби      ', str(self.hobby)])
        mytable.add_row(['еда        ', str(self.food)])

        total = (
            self.transport
            + self.food
            + self.entertainment
            + self.clothes
            + self.present
            + self.health
            + self.hobby
            + self.other
        )
        mytotaltable.add_row([str(total)])
        return (
            f'<pre>{datetime.datetime.now()}\n{mytable}\n{mytotaltable}</pre>'
        )


# db.create_all()
