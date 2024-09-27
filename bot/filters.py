from aiogram.filters.callback_data import CallbackData


class EnterKey(CallbackData, prefix="enter_key"):
    user_id : str


class NoKey(CallbackData, prefix="no_key"):
    user_id : str


class AllGoods(CallbackData, prefix="all_goods"):
    user_id : str


class OneGood(CallbackData, prefix="one_good"):
    user_id : str


class AddGood(CallbackData, prefix="add_good"):
    user_id : str


class DeleteGood(CallbackData, prefix="delete_good"):
    user_id : str


class AddAdmin(CallbackData, prefix="add_admin"):
    user_id : str
