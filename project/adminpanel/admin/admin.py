from flask_admin import Admin, AdminIndexView, expose
from flask import current_app as app
from flask_admin.contrib.sqla import ModelView
from project.database.database import db
from project.database.models import MyWeight, MyWorkout, MyExpenses, DayReport


class MyAdminIndexView(AdminIndexView):
    @expose('/admin')
    def default_view(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        try:
            return True
        except Exception as e:
            pass


admin = Admin(
    app,
    name='',
    static_url_path='admin/static/',
    template_mode='bootstrap3',
    index_view=MyAdminIndexView(
        name='Bot panel',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-send',
    ),
)


class MyWeightView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_labels = dict(
        date='Дата',
        value='Значение',
    )
    create_modal = True
    edit_modal = True


class MyWorkoutView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_labels = dict(
        date='Дата',
        value='Значение',
    )
    create_modal = True
    edit_modal = True


class MyExpensesView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_labels = dict(
        date='Дата',
        value='Значение',
        health='Здоровье',
        transport='Транспорт',
        food='Еда',
        entertainment='Развлечения',
        purchases='Покупки',
        present='Подарки',
        other='Прочее',
    )
    create_modal = True
    edit_modal = True


admin.add_view(MyWeightView(MyWeight, db, name='Вес'))
admin.add_view(MyWorkoutView(MyWorkout, db, name='Тренировки'))
admin.add_view(MyExpensesView(MyExpenses, db, name='Расходы'))
