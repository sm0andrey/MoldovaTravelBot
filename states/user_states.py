from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    Starting_state = State()
    City_state = State()
    Option_state = State()
    Request1_state = State()
    Request2_state = State()
