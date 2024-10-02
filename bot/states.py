from aiogram.fsm.state import State, StatesGroup


class GetArticle(StatesGroup):
    article: State = State()


class AddGood(StatesGroup):
    article: State = State()
    size: State = State()
    amount: State = State()
    address: State = State()


class Admin(StatesGroup):
    admin: State = State()


class DeleteArticle(StatesGroup):
    article: State = State()


class DeleteOneState(StatesGroup):
    article: State = State()
    size: State = State()
    amount: State = State()


class EditAddressState(StatesGroup):
    article: State = State()
    address: State = State()
