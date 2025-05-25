from aiogram.fsm.state import StatesGroup, State

class OrderStates(StatesGroup):
    first_name = State()
    second_name = State()
    email = State()
    number = State()
    address = State()
