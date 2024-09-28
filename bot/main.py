from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.client.session.base import BaseSession
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

import pygsheets

import json

from keyboards import *
from filters import *
from states import *


class AccauntingBot(Bot):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.dispatcher = Dispatcher()
        self.router = Router()
        self.dispatcher.include_router(self.router)

        self.client = pygsheets.authorize(
            service_account_file="clothesaccaunting-d71657ee2e61.json")
        self.spreadsht = self.client.open("clothes_accaunting")
        self.worksht = self.spreadsht.worksheet("title", "main")

        self.default_commands = [
            types.BotCommand(command='start', description='Запуск бота'),
        ]

        self.router.message.register(self.start, Command('start'))
        self.router.message.register(self.get_one, GetArticle.article)

        self.router.callback_query.register(self.show_all, AllGoods.filter())
        self.router.callback_query.register(
            self.get_article_one, OneGood.filter())

    async def start(self, message: types.Message):
        await self.set_my_commands(self.default_commands)
        markup = get_keyboard(str(message.from_user.id))
        await message.answer(text=f"Здравствуйте, <b>{message.from_user.first_name}</b>! Это бот, который помогает вести учет одежды. \nВыберите действие:", parse_mode='html', reply_markup=markup)

    async def show_all(self, query: types.callback_query.CallbackQuery, callback_data: AllGoods):
        data = self.worksht.get_all_records()
        text = "```\n"

        if (len(data) == 0):
            text = "Данных в таблице нет."
        else:
            for key in data[0].keys():
                text += key + " ┃ "
            text = text[:-3:] + "\n"
            for row in data:
                for key, value in row.items():
                    spaces = (10 - len(value)) if key == "Арктикул" else 1
                    text += str(value) + (' ' * spaces)
                text += "\n"
        text += "\n```"

        await query.message.answer(
            text=text, parse_mode="markdown", reply_markup=InlineKeyboardBuilder().as_markup())

        markup = get_keyboard(callback_data.user_id)
        await query.message.answer(
            text="Выберите действие:", reply_markup=markup)
        await query.message.delete()

    async def get_article_one(self, query: types.callback_query.CallbackQuery, callback_data: AllGoods, state: FSMContext):
        await state.set_state(GetArticle.article)
        await state.set_data({"user_id": callback_data.user_id})
        await query.message.edit_text(text="Введите артикул:", reply_markup=InlineKeyboardBuilder().as_markup())

    async def get_one(self, message: types.Message, state: FSMContext):
        state_data = await state.get_data()
        user_id = state_data.get('user_id')
        await state.clear()

        data = self.worksht.get_all_records()

        text = "```\n"

        if (len(data) == 0):
            text = "Данных в таблице нет."
        else:
            for key in data[0].keys():
                text += key + " ┃ "
            text = text[:-3:] + "\n"
            for row in data:
                if row.get('Артикул') == message.text:
                    for key, value in row.items():
                        spaces = (10 - len(value)) if key == "Арктикул" else 1
                        text += str(value) + (' ' * spaces)
        text += "\n```"

        await message.answer(
            text=text, parse_mode="markdown", reply_markup=InlineKeyboardBuilder().as_markup())

        markup = get_keyboard(user_id)
        await message.answer(
            text="Выберите действие:", reply_markup=markup)


if __name__ == '__main__':
    with open('info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        bot = AccauntingBot(token=data.get('token'))
        bot.dispatcher.run_polling(bot)
