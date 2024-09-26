from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.client.session.base import BaseSession

import pygsheets

import json


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

    async def start(self, message: types.Message):
        await self.set_my_commands(self.default_commands)
        await message.answer(text=f"Привет, <b>{message.from_user.first_name}</b>!", parse_mode='html')

        self.worksht.update_value('A13', 'test')
        data = self.worksht.get_all_records()
        target_value = '#qu'
        for idx, row in enumerate(data, 2):
            # print(row)
            if row['Арктикул'] == target_value:
                await message.answer(text=f"Строка найдена: {idx} : {row}")
                break
        else:
            await message.answer(text="Строка с заданным значением не найдена")


if __name__ == '__main__':
    with open('info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        bot = AccauntingBot(token=data.get('token'))
        bot.dispatcher.run_polling(bot)
