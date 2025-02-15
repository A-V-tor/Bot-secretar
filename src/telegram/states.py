from aiogram.fsm.state import State, StatesGroup


class DayWorkouts(StatesGroup):
    save_workout = State()


class AddExpenses(StatesGroup):
    start = State()
    end = State()


class EditLastNoteExpenses(StatesGroup):
    category = State()
    money = State()


class NewValueWeight(StatesGroup):
    start = State()


class ChangeValueWeight(StatesGroup):
    start = State()
