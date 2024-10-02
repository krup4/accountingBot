from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.client.session.base import BaseSession
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove
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
        self.router.message.register(self.choose_size, AddGood.article)
        self.router.message.register(self.get_amount, AddGood.size)
        self.router.message.register(self.update_good, AddGood.amount)
        self.router.message.register(self.add_new, AddGood.address)
        self.router.message.register(self.add_admin, Admin.admin)
        self.router.message.register(self.delete_all, DeleteArticle.article)
        self.router.message.register(
            self.delete_choose_size, DeleteOneState.article)
        self.router.message.register(
            self.delete_get_amount, DeleteOneState.size)
        self.router.message.register(self.delete_one, DeleteOneState.amount)
        self.router.message.register(self.edit_new_address, EditAddressState.article)
        self.router.message.register(self.edit_address, EditAddressState.address)

        self.router.callback_query.register(self.show_all, AllGoods.filter())
        self.router.callback_query.register(
            self.get_article_one, OneGood.filter())
        self.router.callback_query.register(self.article_add, AddOne.filter())
        self.router.callback_query.register(self.get_admin, AddAdmin.filter())
        self.router.callback_query.register(
            self.delete_agree, DeleteGood.filter())
        self.router.callback_query.register(
            self.delete_all_article, DeleteAll.filter())
        self.router.callback_query.register(
            self.delete_one_article, DeleteOne.filter())
        self.router.callback_query.register(self.edit_address_article, EditAddress.filter())

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
                num = (15 - len(str(key))
                       ) if key == "Артикул" else (6 - len(str(key)))
                text += key + (" " * num)
                text += "┃ "

            text = text[:-3:] + "\n\n"

            for row in data:
                for key, value in row.items():
                    spaces = (
                        15 - len(str(value))) if key == "Артикул" else (6 - len(str(value)))
                    text += str(value) + (' ' * spaces) + "┃ "

                text = text[:-4:]
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
            text += "Данных в таблице нет."
        else:
            for key in data[0].keys():
                num = (15 - len(str(key))
                       ) if key == "Артикул" else (6 - len(str(key)))
                text += key + (" " * num)
                text += "┃ "

            text = text[:-3:] + "\n\n"

            for row in data:
                if row.get('Артикул') == message.text:
                    for key, value in row.items():
                        spaces = (
                            15 - len(str(value))) if key == "Артикул" else (6 - len(str(value)))
                        text += str(value) + (' ' * spaces) + "┃ "

                    text = text[:-4:]
                    text += "\n"

            text += "\n```"

        await message.answer(
            text=text, parse_mode="markdown", reply_markup=InlineKeyboardBuilder().as_markup())

        markup = get_keyboard(user_id)
        await message.answer(
            text="Выберите действие:", reply_markup=markup)

    async def article_add(self, query: types.callback_query.CallbackQuery, callback_data: AddOne, state: FSMContext):
        await query.message.edit_text(text="Введите артикул:", reply_markup=InlineKeyboardBuilder().as_markup())
        await state.set_state(AddGood.article)
        await state.set_data({"user_id": callback_data.user_id})

    async def choose_size(self, message: types.Message, state: FSMContext):
        good = await state.get_data()
        await state.clear()
        await state.set_state(AddGood.size)
        good["article"] = message.text
        await state.set_data(good)
        await message.answer(text="Выберите размер: ", reply_markup=sizes_markup())

    async def get_amount(self, message: types.Message, state: FSMContext):
        good = await state.get_data()
        await state.clear()
        await state.set_state(AddGood.amount)
        good['size'] = message.text
        await state.set_data(good)
        await message.answer(text="Введите количество: ", reply_markup=ReplyKeyboardRemove())

    async def update_good(self, message: types.Message, state: FSMContext):
        good = await state.get_data()
        await state.clear()
        good["amount"] = int(message.text)

        data = self.worksht.get_all_records()
        idx = 0
        last = 0
        num = 0
        for i, row in enumerate(data, 2):
            if row.get('Артикул') == good.get('article'):
                idx = i
                num = row.get(good.get('size'))
                break
            last = i

        if idx == 0:
            good['row'] = last
            await state.set_state(AddGood.address)
            await state.set_data(good)
            await message.answer(text="Походу, данного товара в таблице нет. Чтобы его добавить, введите адрес: ")
        else:
            sizes = {"S": "B", "M": 'C', "L": 'D', "XL": 'E', "XXL": 'F'}
            self.worksht.update_value(f"{sizes[good.get("size")]}{
                                      idx}", good.get("amount") + num)
            await message.answer(text="Товар успешно обновлен!")
            markup = get_keyboard(good.get("user_id"))
            await message.answer(text="Выберите действие: ", reply_markup=markup)

    async def add_new(self, message: types.Message, state: FSMContext):
        good = await state.get_data()
        await state.clear()
        good["address"] = message.text

        writing = [good.get('article')]
        sizes = {"S": 0, "M": 1, "L": 2, "XL": 3, "XXL": 4}
        for i in range(5):
            if i == sizes[good.get("size")]:
                writing.append(good.get("amount"))
            else:
                writing.append(0)
        writing.append(good.get("address"))

        self.worksht.insert_rows(row=good.get('row'), values=writing)

        await message.answer(text="Товар успешно добавлен!")
        markup = get_keyboard(good.get("user_id"))
        await message.answer(text="Выберите действие: ", reply_markup=markup)

    async def get_admin(self, query: types.callback_query.CallbackQuery, callback_data: AddAdmin, state: FSMContext):
        await state.set_state(Admin.admin)
        await state.set_data({"user_id": callback_data.user_id})
        await query.message.edit_text(text='Введите id пользователя: \n(Для этого нужно у бота @username_to_id_bot нажать кнопку "User" и выбрать пользователя, которого вы хотите добавить в администраторы. Затем надо скопировать этот id и прислать сюда) ', reply_markup=InlineKeyboardBuilder().as_markup())

    async def add_admin(self, message: types.Message, state: FSMContext):
        user = await state.get_data()
        await state.clear()
        with open('info.json', 'r') as f:
            data = json.load(f)

        data['admins'].append(message.text)

        with open('info.json', 'w') as f:
            json.dump(data, f, indent=4)

        await message.answer(text="Админ успешно добавлен!")
        markup = get_keyboard(user.get("user_id"))
        await message.answer(text="Выберите действие: ", reply_markup=markup)

    async def delete_agree(self, query: types.callback_query.CallbackQuery, callback_data: DeleteGood):
        await query.message.edit_text(text="Вы хотите удалить товар целиком или только несколько штук?", reply_markup=agree_markup(callback_data.user_id))

    async def delete_all_article(self, query: types.callback_query.CallbackQuery, callback_data: DeleteAll, state: FSMContext):
        await query.message.edit_text(text="Введите артикул:", reply_markup=InlineKeyboardBuilder().as_markup())
        await state.set_state(DeleteArticle.article)
        await state.set_data({"user_id": callback_data.user_id})

    async def delete_all(self, message: types.Message, state: FSMContext):
        user = await state.get_data()
        await state.clear()
        data = self.worksht.get_all_records()

        flag = False
        for i, row in enumerate(data, 2):
            if row.get("Артикул") == message.text:
                self.worksht.delete_rows(i)
                flag = True
                break

        if flag:
            await message.answer(text="Успешно удалено!")
        else:
            await message.answer(text="Данного артикула нет в таблице!")

        markup = get_keyboard(user.get("user_id"))
        await message.answer(text="Выберите действие: ", reply_markup=markup)

    async def delete_one_article(self, query: types.callback_query.CallbackQuery, callback_data: DeleteOne, state: FSMContext):
        await query.message.edit_text(text="Введите артикул:", reply_markup=InlineKeyboardBuilder().as_markup())
        await state.set_state(DeleteOneState.article)
        await state.set_data({"user_id": callback_data.user_id})

    async def delete_choose_size(self, message: types.Message, state: FSMContext):
        good = await state.get_data()
        await state.clear()
        await state.set_state(DeleteOneState.size)
        good["article"] = message.text
        await state.set_data(good)
        await message.answer(text="Выберите размер: ", reply_markup=sizes_markup())

    async def delete_get_amount(self, message: types.Message, state: FSMContext):
        good = await state.get_data()
        await state.clear()
        await state.set_state(DeleteOneState.amount)
        good['size'] = message.text
        await state.set_data(good)
        await message.answer(text="Введите количество: ", reply_markup=ReplyKeyboardRemove())

    async def delete_one(self, message: types.Message, state: FSMContext):
        good = await state.get_data()
        await state.clear()
        good['amount'] = int(message.text)
        
        data = self.worksht.get_all_records()
        idx = 0
        num = 0
        for i, row in enumerate(data, 2):
            if row.get('Артикул') == good.get('article'):
                idx = i
                num = row.get(good.get('size'))
                break

        if idx == 0:
            await message.answer(text="Данного артикула нет в таблице!")
        elif num - good.get("amount") < 0:
            await message.answer(text="Товар не может быть обновлен, так как в наличии товара меньше, чем указанное значение!")
        else:
            sizes = {"S": "B", "M": 'C', "L": 'D', "XL": 'E', "XXL": 'F'}
            self.worksht.update_value(f"{sizes[good.get("size")]}{idx}", num - good.get("amount"))
            await message.answer(text="Товар успешно обновлен!")
        
        markup = get_keyboard(good.get("user_id"))
        await message.answer(text="Выберите действие: ", reply_markup=markup)

    async def edit_address_article(self, query: types.callback_query.CallbackQuery, callback_data: EditAddress, state: FSMContext):
        await state.set_state(EditAddressState.article)
        await state.set_data({"user_id": callback_data.user_id})
        await query.message.edit_text(text="Введите артикул: ", reply_markup=InlineKeyboardBuilder().as_markup())

    async def edit_new_address(self, message: types.Message, state: FSMContext):
        good = await state.get_data()
        await state.clear()
        good["article"] = message.text

        data = self.worksht.get_all_records()
        idx = -1
        adress = ""
        for i, row in enumerate(data, 2):
            if row.get('Артикул') == good.get("article"):
                idx = i
                adress = row.get('Адрес')

        if idx == -1:
            await message.answer(text="Данного артикула нет в таблице!")
            markup = get_keyboard(good.get('user_id'))
            await message.answer(text="Выберите действие: ", reply_markup=markup)
        else:
            good['row'] = idx
            await state.set_state(EditAddressState.address)
            await state.set_data(good)
            await message.answer(text=f"Введите адрес: \n (Сейчас адрес такой: {adress})")

    async def edit_address(self, message: types.Message, state: FSMContext):
        good = await state.get_data()
        await state.clear()
        self.worksht.update_value(f"G{good.get('row')}", message.text)
        await message.answer(text="Адрес успешно обновлен!")
        markup = get_keyboard(good.get('user_id'))
        await message.answer(text="Выберите действие: ", reply_markup=markup)


if __name__ == '__main__':
    with open('info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        bot = AccauntingBot(token=data.get('token'))
        bot.dispatcher.run_polling(bot)
