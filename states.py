from aiogram.fsm.state import StatesGroup, State

class ModelStatesGroup(StatesGroup):
    user_name = State()
    queue_name = State()
    queue_id = State()
    users_entered = State()


class OtherStatesGroup(StatesGroup):
    user_name = State()
    queue_id = State()


class MainStatesGroup(StatesGroup):
    user_name = State()
    is_moder = State()
    queue_name_M = State()
    queue_id_O = State()
    queue_id = State()
    users_entered_M = State()
    is_waiting = State()
    is_requare_param = State()


