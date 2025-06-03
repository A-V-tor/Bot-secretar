from dotenv import find_dotenv, load_dotenv
from flask import (
    current_app as app,
    request,
)
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_ckeditor import CKEditorField
from flask_login import current_user

from config import settings
from src.database.base import session_factory
from src.database.models.expenses import Expenses
from src.database.models.users import User
from src.database.models.weight import Weight
from src.database.models.workouts import Workout
from src.utils.tools import TypeExpenses, UserPermissions

load_dotenv(find_dotenv())


class CustomModelView(ModelView):
    def is_accessible(self):
        """
        Определение доступа к администрированию моделей бд.
        """

        def is_accessible(self):
            if current_user.is_authenticated and current_user.permission.value in ['Админ', 'Владелец']:
                return True

            return False


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def default_view(self):
        expense_url = settings.DASHBOARD_EXPENSE
        weight_url = settings.DASHBOARD_WEIGHT
        if 'check_mobile=True' in request.query_string.decode('utf-8'):
            return self.render('admin/index.html', expense_url=expense_url, weight_url=weight_url, check_mobile=True)
        else:
            return self.render('admin/index.html', expense_url=expense_url, weight_url=weight_url, check_mobile=False)

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


class UserView(CustomModelView):
    can_view_details = True
    # form_choices = {'permission': [
    #     (i.split(".")[-1], i.value) for i in UserPermissions
    # ]}
    column_choices = {'permission': [(i.split('.')[-1], i.value) for i in UserPermissions]}
    column_filters = ('username', 'telegram_id', 'is_active', 'permission')
    column_default_sort = [
        ('username', True),
        ('telegram_id', True),
        ('is_active', True),
        ('permission', True),
    ]
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
        workouts='заметка по тренировке',
    )
    create_modal = True
    edit_modal = True


class WeightView(CustomModelView):
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


class ExpensesView(CustomModelView):
    can_view_details = True
    form_columns = ['type_expenses', 'value', 'user', 'created_at']
    column_exclude_list = ('id',)
    column_default_sort = [('updated_at', True), ('created_at', True)]
    column_choices = {'type_expenses': [(i.split('.')[-1], i.value) for i in TypeExpenses]}
    column_labels = dict(
        type_expenses='Трата',
        value='Значение',
        user='Пользователь',
        created_at='Дата создания',
        updated_at='Дата обновления',
    )

    create_modal = True
    edit_modal = True

    def on_model_change(self, form, model, is_created):
        if is_created:
            # TODO: Логика при создании новой записи
            print('Новая запись создана', model)
            print(dir(form))
        return super().on_model_change(form, model, is_created)


class WorkoutView(CustomModelView):
    can_view_details = True
    column_default_sort = [('updated_at', True), ('created_at', True)]
    form_columns = ['text_value', 'user', 'is_active']
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


admin.add_view(UserView(User, session_factory(), name='Пользователи'))
admin.add_view(WeightView(Weight, session_factory(), name='Журнал веса', category='Журналы'))
admin.add_view(ExpensesView(Expenses, session_factory(), name='Журнал трат', category='Журналы'))
admin.add_view(
    WorkoutView(
        Workout,
        session_factory(),
        name='Журнал тренировок',
        category='Журналы',
    )
)
