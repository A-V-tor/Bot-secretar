import os
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask import current_app as app
from flask_ckeditor import CKEditorField
from src.database.base import session_factory, get_session
from dotenv import load_dotenv, find_dotenv
from src.database.models.users import User
from src.database.models.weight import Weight
from flask_admin.contrib.sqla import ModelView
from src.database.models.expenses import Expenses
from src.database.models.workouts import Workout
from flask_login import current_user
from flask_admin.theme import Bootstrap4Theme

from flask_admin.menu import MenuLink
load_dotenv(find_dotenv())
from src.utils.tools import UserPermissions, TypeExpenses

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def default_view(self):
        expense_url = os.getenv('DASHBOARD_EXPENSE')
        weight_url = os.getenv('DASHBOARD_WEIGHT')
        return self.render('admin/index.html', expense_url=expense_url, weight_url=weight_url)

    def is_accessible(self):

        if current_user.is_authenticated:
            return True

        return False


admin = Admin(
    app,
    name='',
    static_url_path='admin/static/',
    theme=Bootstrap4Theme(swatch='lumen', fluid=True),
    index_view=MyAdminIndexView(
        name='Bot panel',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-send',
    ),
)


class UserView(ModelView):
    can_view_details = True
    # form_choices = {'permission': [
    #     (i.split(".")[-1], i.value) for i in UserPermissions
    # ]}
    column_choices = {'permission': [
        (i.split(".")[-1], i.value) for i in UserPermissions
    ]}
    column_filters = ('username', 'telegram_id', 'is_active', 'permission')
    column_default_sort = [('username', True), ('telegram_id', True), ('is_active', True), ('permission', True)]
    column_labels = dict(
        username='Юзернейм',
        psw='Пароль',
        permission='Права',
        first_surname='Фамилия',
        last_surname='Отчество',
        description='Описание',
        telegram_id='Телеграм id',
        is_active='Активно?',
        created_at='Дата создания',
        updated_at='Дата обновления',
        weight='заметка по весу',
        expenses='заметка по тратам',
        workouts='заметка по тренировке'
    )
    create_modal = True
    edit_modal = True


    def is_accessible(self):
        if current_user.is_authenticated:
            return True

        return False


class WeightView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_exclude_list = ('id',)
    column_default_sort = [('updated_at', True), ('created_at', True)]
    column_labels = dict(
        value='Вес',
        user='Пользователь',
        created_at='Дата создания',
        updated_at='Дата обновления',
    )

    create_modal = True
    edit_modal = True

    def is_accessible(self):
        if current_user.is_authenticated and current_user.permission.value in ['Админ', 'Владелец']:
            return True

        return False


class ExpensesView(ModelView):
    can_view_details = True
    form_columns = ["type_expenses", "value", "user", "created_at"]
    column_exclude_list = ('id',)
    column_default_sort = [('updated_at', True), ('created_at', True)]
    column_choices = {'type_expenses': [
        (i.split(".")[-1], i.value) for i in TypeExpenses
    ]}
    column_labels = dict(
        type_expenses='Трата',
        value='Значение',
        user='Пользователь',
        created_at='Дата создания',
        updated_at='Дата обновления',
    )

    create_modal = True
    edit_modal = True

    def is_accessible(self):
        if current_user.is_authenticated and current_user.permission.value in ['Админ', 'Владелец']:
            return True

        return False

    def on_model_change(self, form, model, is_created):
        if is_created:
            # Логика при создании новой записи
            print("Новая запись создана", model)
            print(dir(form))
        return super().on_model_change(form, model, is_created)


class WorkoutView(ModelView):
    can_view_details = True
    column_default_sort = [('updated_at', True), ('created_at', True)]
    form_columns = ["text_value", "user", "is_active"]
    column_labels = dict(
        text_value='Значение',
        user='Пользователь',
        is_active='Активно?',
        created_at='Дата создания',
        updated_at='Дата обновления',
    )
    column_list = ['text_value', 'is_active', 'created_at', 'updated_at']
    create_template = 'admin/edit.html'
    edit_template = 'admin/edit.html'
    form_overrides = {'text_value': CKEditorField}

    def is_accessible(self):
        if current_user.is_authenticated and current_user.permission.value in ['Админ', 'Владелец']:
            return True

        return False


admin.add_view(UserView(User, session_factory(), name='Пользователи'))

admin.add_view(WeightView(Weight, session_factory(), name='Журнал веса', category="Журналы"))
admin.add_view(ExpensesView(Expenses, session_factory(), name='Журнал трат', category="Журналы"))
admin.add_view(WorkoutView(Workout, session_factory(), name='Журнал тренировок', category="Журналы"))

# admin.add_link(MenuLink(name='Home Page', url='/', category='Links'))
