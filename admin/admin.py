from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from finance.models import CurrentBalance
from bot.handlers import current_user
from bot import server, db


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        try:
            if current_user.psw:
                return True
        except:
            pass


admin = Admin(
    server,
    name="",
    template_mode="bootstrap3",
    index_view=MyAdminIndexView(
        name="Админка", menu_icon_type="glyph", menu_icon_value="glyphicon-send"
    ),
)


class CurrentBalanceView(ModelView):
    column_display_pk = True
    column_labels = dict(
        date='дата',
        transport='транспорт',
        food='еда',
        entertainment='развлечения',
        clothes='одежда',
        present='подарки',
        health='здоровье',
        hobby='хобби',
        other='прочее',
    )
    can_view_details = True
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        try:
            if current_user.psw:
                return True
        except:
            pass


admin.add_view(
    CurrentBalanceView(
        CurrentBalance,
        db.session,
        name="Расходы",
        menu_icon_type="glyph",
        menu_icon_value="glyphicon-shopping-cart",
    )
)