from unittest.mock import create_autospec

import pytest
from aiogram import types
from sqlalchemy.orm import sessionmaker

from config import DevelopConfig, settings
from src.database.base import Base, engine
from src.webapp.wsgi import app


@pytest.fixture(
    name='get_db',
    scope='session',
)
def get_test_db():
    assert isinstance(settings, DevelopConfig)

    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        engine,
        expire_on_commit=False,
    )

    yield session_factory

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope='session')
def user():
    user = {
        'chat.id': 123456789,
        'chat.username': 'test_username',
        'chat.first_name': 'first_name',
        'chat.last_name': 'last_name',
    }

    return user


@pytest.fixture
def message(user):
    message_mock = create_autospec(types.Message)
    message_mock.chat = create_autospec(types.Chat, instance=True)
    message_mock.chat.id = user['chat.id']
    message_mock.chat.username = user['chat.username']
    message_mock.chat.first_name = user['chat.first_name']
    message_mock.chat.last_name = user['chat.last_name']

    return message_mock


@pytest.fixture
def callback_query(user):
    callback_query = create_autospec(types.CallbackQuery, instance=True)
    callback_query.message = create_autospec(types.Message, instance=True)

    callback_query.message.chat = create_autospec(types.Chat, instance=True)
    callback_query.message.chat.id = user['chat.id']
    callback_query.message.chat.username = user['chat.username']
    callback_query.message.chat.first_name = user['chat.first_name']
    callback_query.message.chat.last_name = user['chat.last_name']
    return callback_query


@pytest.fixture()
def webapp():
    yield app


@pytest.fixture()
def client(webapp):
    return webapp.test_client()


@pytest.fixture()
def runner(webapp):
    return webapp.test_cli_runner()
