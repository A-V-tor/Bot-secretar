from flask_admin import Admin, AdminIndexView, expose
from flask import current_app as app
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from project.database.database import db
from project.database.models import (
    MyWeight,
    MyWorkout,
    MyExpenses,
    DayReport,
    MyNotes,
)
from project.adminpanel.admin.models import AdminUser


class MyAdminIndexView(AdminIndexView):
    @expose('/admin')
    def default_view(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        try:
            if current_user.is_authenticated:
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

    def is_accessible(self):
        try:
            if current_user.is_authenticated:
                return True
        except Exception as e:
            pass


class MyWorkoutView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_labels = dict(
        date='Дата',
        value='Значение',
    )
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        try:
            if current_user.is_authenticated:
                return True
        except Exception as e:
            pass


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

    def is_accessible(self):
        try:
            if current_user.is_authenticated:
                return True
        except Exception as e:
            pass


class AdminUserView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_labels = dict(
        name='Логин',
        psw='Пароль',
    )

    def is_accessible(self):
        try:
            if current_user.is_authenticated:
                return True
        except Exception as e:
            pass


class MyNotesView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_labels = dict(
        date='ДАТА',
        note='Заметка',
    )

    def is_accessible(self):
        try:
            if current_user.is_authenticated:
                return True
        except Exception as e:
            pass


admin.add_view(MyWeightView(MyWeight, db, name='Вес'))
admin.add_view(MyWorkoutView(MyWorkout, db, name='Тренировки'))
admin.add_view(MyExpensesView(MyExpenses, db, name='Расходы'))
admin.add_view(AdminUserView(AdminUser, db, name='Администраторы'))
admin.add_view(MyNotesView(MyNotes, db, name='Заметки'))
