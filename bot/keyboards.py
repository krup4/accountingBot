from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from filters import *


def default_markup(user_id):
    markup = InlineKeyboardBuilder()

    markup.row(InlineKeyboardButton(
        text='Посмотреть все товары', callback_data=AllGoods(user_id=user_id).pack()))
    markup.row(InlineKeyboardButton(
        text='Посмотреть конкретный товар', callback_data=OneGood(user_id=user_id).pack()))

    return markup.as_markup()


def admin_markup(user_id):
    markup = InlineKeyboardBuilder()

    markup.row(InlineKeyboardButton(
        text='Посмотреть все товары', callback_data=AllGoods(user_id=user_id).pack()))
    markup.row(InlineKeyboardButton(
        text='Посмотреть конкретный товар', callback_data=OneGood(user_id=user_id).pack()))
    markup.row(InlineKeyboardButton(
        text='Добавить товар', callback_data=AddGood(user_id=user_id).pack()))
    markup.row(InlineKeyboardButton(text='Удалить товар',
               callback_data=DeleteGood(user_id=user_id).pack()))

    return markup.as_markup()


def developer_markup(user_id):
    markup = InlineKeyboardBuilder()

    markup.row(InlineKeyboardButton(
        text='Посмотреть все товары', callback_data=AllGoods(user_id=user_id).pack()))
    markup.row(InlineKeyboardButton(
        text='Посмотреть конкретный товар', callback_data=OneGood(user_id=user_id).pack()))
    markup.row(InlineKeyboardButton(
        text='Добавить товар', callback_data=AddGood(user_id=user_id).pack()))
    markup.row(InlineKeyboardButton(text='Удалить товар',
               callback_data=DeleteGood(user_id=user_id).pack()))
    markup.row(InlineKeyboardButton(text='Добавить админа',
               callback_data=AddAdmin(user_id=user_id).pack()))

    return markup.as_markup()
