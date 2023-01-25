from wtforms import TextAreaField
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from finance.models import CurrentBalance
from bot.models import MyWeight, MyNotes, MyWorkouts
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
        date="дата",
        transport="транспорт",
        food="еда",
        entertainment="развлечения",
        clothes="одежда",
        present="подарки",
        health="здоровье",
        hobby="хобби",
        other="прочее",
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


class MyWeightView(ModelView):
    column_display_pk = True
    column_labels = dict(date="дата", value="вес")
    column_filters = ["date"]


class MyNotesView(ModelView):
    column_display_pk = True
    column_labels = dict(date="дата", note="запись")
    column_editable_list = ["note"]
    form_widget_args = {
        "note": {
            "rows": 10,
            "style": "font-family: monospace;",
        }
    }
    form_overrides = dict(note=TextAreaField)
    can_view_details = True


class MyWorkoutView(ModelView):
    column_display_pk = True
    column_labels = dict(date="дата", entries="тренировка")
    column_editable_list = ["entries"]
    form_widget_args = {
        "entries": {
            "rows": 10,
            "style": "font-family: monospace;",
        }
    }
    form_overrides = dict(entries=TextAreaField)


admin.add_view(
    CurrentBalanceView(
        CurrentBalance,
        db.session,
        name="Расходы",
        menu_icon_type="glyph",
        menu_icon_value="glyphicon-shopping-cart",
    )
)

admin.add_view(
    MyWeightView(
        MyWeight,
        db.session,
        name="Вес",
        menu_icon_type="glyph",
        menu_icon_value="glyphicon-hand-down",
    )
)

admin.add_view(
    MyNotesView(
        MyNotes,
        db.session,
        name="Заметки",
        menu_icon_type="glyph",
        menu_icon_value="glyphicon-pencil",
    )
)

admin.add_view(
    MyWorkoutView(
        MyWorkouts,
        db.session,
        name="Тренировки",
        menu_icon_type="glyph",
        menu_icon_value="glyphicon-heart-empty",
    )
)
