from aiogram.filters.callback_data import CallbackData


class AllGoods(CallbackData, prefix="all_goods"):
    user_id: str


class OneGood(CallbackData, prefix="one_good"):
    user_id: str


class AddOne(CallbackData, prefix="add_good"):
    user_id: str


class DeleteGood(CallbackData, prefix="delete_good"):
    user_id: str


class AddAdmin(CallbackData, prefix="add_admin"):
    user_id: str


class Sizes(CallbackData, prefix="sizes"):
    size: str
