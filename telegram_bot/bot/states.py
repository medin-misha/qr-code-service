from aiogram.fsm.state import State, StatesGroup


class MakeBasicQRCode(StatesGroup):
    get_data = State()


class BuyQrs(StatesGroup):
    get_count = State()
