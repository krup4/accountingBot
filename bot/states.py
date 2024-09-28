from aiogram.fsm.state import State, StatesGroup


class GetArticle(StatesGroup):
    article: State = State()