import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import re
import psycopg2
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, InputFile
from aiogram.utils import executor
from openpyxl import Workbook

# logs level
logging.basicConfig(level=logging.INFO)
DB_URI = 'postgres://afzlxrjvaklsms:2acd0197ef23a3692c85d7fca7922eeed81046ca1597d9f' \
         '31cb559b243b9f2e8@ec2-79-125-26-60.eu-west-1.compute.amazonaws.com:5432/ddnqvvcb17288e'

# initialization bot
# TOKEN = your API token
bot = Bot(token='5295251052:AAG0BkwstG0vN59muiaOIpsUIFHpv-2jIBo')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# DB config
db_connection = psycopg2.connect(DB_URI, sslmode='require')
db_object = db_connection.cursor()

# EXCEL config
wb = Workbook()
# grab the active worksheet
ws = wb.active

# Button config
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
but1 = types.KeyboardButton(text='Зарегистрироваться')
but2 = types.KeyboardButton(text='1234')
keyboard.add(but1)


# Form registration start place
class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    phone_number = State()  # Will be represented in storage as 'Form:age'


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    username = message.from_user.username
    # db_object.execute(f'SELECT id FROM users WHERE id = {id1}')
    # result = db_object.fetchone()
    #
    # if not result:
    #     db_object.execute('INSERT INTO users(id, username, name, phone_number) VALUES (%s, %s, %s)',
    #                       (id1, username, 0, 0))
    #     db_connection.commit()

    await message.reply(f"Привет! {username}", reply_markup=keyboard)


# @dp.message_handler(commands=['referal'])
# async def referal_start(message: types.Message):
#     my_channel_id = -1001478296614
#     user_channel_status = await bot.get_chat_member(chat_id=my_channel_id, user_id=message.chat.id)
#     user_channel_status = re.findall(r"\w*", str(user_channel_status))
#     try:
#         if user_channel_status[70] != 'left':
#             with open('1.png', mode='rb') as f:
#                 await bot.send_photo(message.from_user.id, f)
#             await bot.send_message(message.from_user.id, 'ок')
#
#         else:
#             with open('2.png', mode='rb') as f:
#                 await bot.send_photo(message.from_user.id, f)
#             await bot.send_message(message.chat.id, 'ne ok')
#             # Условие для тех, кто не подписан
#     except:
#         if user_channel_status[60] != 'left':
#             with open('1.png', mode='rb') as f:
#                 await bot.send_photo(message.from_user.id, f)
#             await bot.send_message(message.from_user.id, 'ok1')
#             # Условие для "подписанных"
#         else:
#             with open('2.png', mode='rb') as f:
#                 await bot.send_photo(message.from_user.id, f)
#             await bot.send_message(message.from_user.id, 'ne ok1')
#             # Условие для тех, кто не подписан
#
#
# @dp.message_handler(Text(equals='Задать вопрос'))
# async def one_use_answer(message: types.Message):
#     await message.answer('@siberian_vapor_102')
#
#
# @dp.message_handler(Text(equals='ОДНОРАЗКИ'))
# async def one_use_answer(message: types.Message):
#     with open('one_use.txt', 'r', encoding='utf-8') as f:
#         texts = f.read()
#         await message.answer(texts)


@dp.message_handler(Text(equals='Зарегистрироваться'))
async def process_start_command2(message: types.Message):
    # Test user for registration yet

    db_object.execute(f'SELECT telegram_id FROM users WHERE telegram_id = {message.from_user.id}')
    result = db_object.fetchone()

    db_object.execute(f'SELECT id FROM users WHERE telegram_id = {message.from_user.id}')
    result1 = str(db_object.fetchone()).replace(',)', '').replace('(', '')
    # db_object.execute(f"SELECT CURRVAL(pg_get_serial_sequence('users','id')) AS last_insert_id;")
    # rez = db_object.fetchone()
    # print(rez)
    if result:
        await message.answer(f'Вы уже зарегистрированы ваш код для входа {result1}')
    else:
        with open('text.txt', 'r', encoding='utf-8') as f:
            texts = f.read()
        await bot.send_photo(message.chat.id, photo=InputFile('1.jpg'), caption=texts, reply_markup=keyboard)
        await Form.name.set()
        markup = types.ReplyKeyboardRemove()
        return await message.answer('Введите ваше имя и фамилию', reply_markup=markup)


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.reply("Отлично! теперь ваш номер телефона?")


@dp.message_handler(state=Form.phone_number)
async def process_number(message: types.Message, state: FSMContext):
    # a = input()
    #
    # d = '1234567890-()+'
    #
    # for i in a:
    #     if i not in d:
    #         await state.reset_state(True)

    async with state.proxy() as data:
        data['phone_number'] = message.text
        phone = data['phone_number']
        name = data['name']

    id1 = message.from_user.id
    username = message.from_user.username
    db_object.execute(f'SELECT telegram_id FROM users WHERE telegram_id = {id1}')
    result = db_object.fetchone()

    if not result:
        db_object.execute('INSERT INTO users(telegram_id, username, name, phone_number) VALUES (%s, %s, %s, %s)',
                          (id1, username, name, phone))
        print(id1, username, data['name'], data['phone_number'])
        db_connection.commit()

    db_object.execute(f'SELECT id FROM users WHERE telegram_id = {id1}')
    result1 = str(db_object.fetchone()).replace(',)', '').replace('(', '')
    markup = types.KeyboardButton(text='/start')
    keyboard.add(markup)
    await message.reply(f'Отлично, твой номер: {result1}\n '
                        f'Кстати, не забудь подписаться на наши телеграмм аккаунты, '
                        f'там будет вся информация о наших тусовках: \n'
                        f'https://t.me/+RgkE9Witvo5kMTc6\n '
                        f'https://t.me/taste_party\n '
                        f'Увидимся уже в эту пятницу!\n '
                        f'Со стилем, KAZANTIP X TASTE🤍\n', reply_markup=keyboard)
    await state.finish()


@dp.message_handler(commands=['chilldabrek'])
async def process_start_command1(message: types.Message):
    await message.reply("Да да он\ntelegram:\n@chilldabrek\n\nhttps://github.com/childabrek")


@dp.message_handler(Text(equals='excel'))
async def excel(message: types.Message):
    db_object.execute(f'SELECT * FROM users')
    for i in db_object.fetchall():
        ws.append(i)
    # Save the file
    wb.save("sample.xlsx")

    await message.answer_document(open("sample.xlsx", 'rb'))


# запускаем лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
