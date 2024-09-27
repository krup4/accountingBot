from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.client.session.base import BaseSession
from aiogram.utils.keyboard import InlineKeyboardBuilder

import pygsheets

import json

from keyboards import *
from filters import *


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

        self.router.callback_query.register(self.show_all, AllGoods.filter())

    async def start(self, message: types.Message):
        await self.set_my_commands(self.default_commands)
        with open('info.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            markup = default_markup(str(message.from_user.id))
            if str(message.from_user.id) in data.get('developer'):
                markup = developer_markup(str(message.from_user.id))
            elif str(message.from_user.id) in data.get('admins'):
                markup = admin_markup(str(message.from_user.id))
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

        with open('info.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            markup = default_markup(callback_data.user_id)
            if callback_data.user_id in data.get('developer'):
                markup = developer_markup(callback_data.user_id)
            elif callback_data.user_id in data.get('admins'):
                markup = admin_markup(callback_data.user_id)
            await query.message.answer(
                text="Выберите действие:", reply_markup=markup)
        await query.message.delete()


if __name__ == '__main__':
    with open('info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        bot = AccauntingBot(token=data.get('token'))
        bot.dispatcher.run_polling(bot)
