from aiogram.fsm.state import State, StatesGroup


class GetArticle(StatesGroup):
    article: State = State()

class AddGood(StatesGroup):
    article: State = State()
    size: State = State()
    amount: State = State()
