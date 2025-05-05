import datetime
from unittest.mock import AsyncMock

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from src.database import Expenses
from src.services.expenses import ExpensesTelegramService
from src.telegram.handlers.expenses import root_expenses_menu, save_expenses, show_expanses_for_day
from src.telegram.keyboards.base_kb import start_kb
from src.telegram.keyboards.expenses_kb import expanses_journal_kb, root_menu_expanses_kb


class TestExpenses:
    """
    Тестирования хендлеров бота по ведению расходов.
    `src.telegram.handlers.base`
    """

    @pytest.mark.asyncio
    async def test_callback_handler_root_expenses_menu(self, callback_query, user):
        """
        Проверка ответа от нажатия на кнопку "Журнал расходов".
        """
        callback_query.message.answer = AsyncMock()
        callback_query.message.delete = AsyncMock()

        state = FSMContext(MemoryStorage(), user['chat.id'])
        await root_expenses_menu(callback_query, state)

        callback_query.message.delete.assert_called()
        callback_query.message.answer.assert_called_with(
            'Журнал ведения расходов', reply_markup=await root_menu_expanses_kb()
        )

    @pytest.mark.asyncio
    async def test_callback_handler_show_expanses_for_day(self, callback_query, user):
        callback_query.message.answer = AsyncMock()
        callback_query.message.delete = AsyncMock()

        expenses_service = ExpensesTelegramService(callback_query)
        my_table, flag_last_note = await expenses_service.get_expenses_for_day()
        await show_expanses_for_day(callback_query)

        callback_query.message.delete.assert_called_once()
        callback_query.message.answer.assert_called_once_with(
            f'<pre>{my_table}</pre>', reply_markup=await expanses_journal_kb(False), parse_mode='HTML'
        )

    @pytest.mark.asyncio
    async def test_callback_handler_save_expenses(self, callback_query, user):
        callback_query.message.answer = AsyncMock()
        callback_query.message.delete = AsyncMock()

        state = FSMContext(MemoryStorage(), user['chat.id'])
        data = {'category': 'транспорт', 'money': 1000}
        await state.set_data(data)

        await save_expenses(callback_query, state)

        callback_query.message.delete.assert_called_once()
        msg = 'Запись сохранена'
        callback_query.message.answer.assert_called_once_with(msg, reply_markup=await start_kb())

        today = datetime.date.today()
        year, month, day = today.year, today.month, today.day
        check_note = Expenses.get_last_note_for_current_day(user['chat.id'], year, month, day)

        assert check_note is not None
