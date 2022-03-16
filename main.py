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
from aiogram.types import ParseMode
from aiogram.utils import executor

# задаем уровень логов
logging.basicConfig(level=logging.INFO)
DB_URI = 'postgres://ncwiwqltyogxme:db5c56c3e31c54d392efb6ae625f83700777' \
         'c736d5d653f1b61bd09cee685ce1@ec2-176-34-105-15.eu-west-1.compute.amazonaws.com:5432/d8bpubesc766fo'
# инициализируем бота
# TOKEN = your API token
bot = Bot(token='5295251052:AAG0BkwstG0vN59muiaOIpsUIFHpv-2jIBo')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db_connection = psycopg2.connect(DB_URI, sslmode='require')
db_object = db_connection.cursor()


class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    phone_number = State()  # Will be represented in storage as 'Form:age'


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but4 = types.KeyboardButton(text='Зарегистрироваться')
    keyboard.add(but4)
    # id1 = message.from_user.id
    # username = message.from_user.username
    # db_object.execute(f'SELECT id FROM users WHERE id = {id1}')
    # result = db_object.fetchone()
    #
    # if not result:
    #     db_object.execute('INSERT INTO users(id, username, name, phone_number) VALUES (%s, %s, %s)',
    #                       (id1, username, 0, 0))
    #     db_connection.commit()
    await message.reply("Привет!", reply_markup=keyboard)
    # with open('text.txt') as a:
    #     b = a.readlines()
    #     await message.answer(*b)
    await message.answer('Давно вы не ощущали этого семейного вайба. У НАС ДЛЯ ВАС ХОРОШИЕ НОВОСТИ!'
                         ' Самая семейная тусовка вернулась в строй💕 '
                         '@Андрей снова зарядит вас позитивом и энергией в конце недели, как в старые добрые😎'
                         'Ну и как же без подарочков? Мы подготовили для вас:'
                         '1. 5 ПРОХОДОК(помните, что это не просто проходка, к ней в подарок идёт'
                         ' самое крутое настроение и классно проведённое время)'
                         '2. 5 БУТЫЛОК 🍾'
                         '3. СТРИЖКА В @франк барбер'
                         'ОСТАЛЬНЫЕ ПОДАРОЧКИ БУДУТ РАСКРЫТЫ ЧУТОЧКУ ПОЗЖЕ '
                         'ОБЯЗАТЕЛЬНЫЕ УСЛОВИЯ:'
                         '1. Быть подписанным на наш телеграмм (ссылка в шапке профиля)'
                         '2. Отметить в комментариях РАЗНЫХ друзей (количество неограниченно)'
                         '3. Сделать репост афиши'
                         'Условия входа: '
                         '250₽ - с репостом ✅'
                         '300₽ - без ❌'
                         'ДАТА: 18 марта'
                         'ОТКРЫТИЕ: 19:00'
                         'ЗАВЕДЕНИЕ: LUNA BAR')


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
#
#
# @dp.message_handler(Text(equals='ЖЕЛЕЗО'))
# async def hardware_answer(message: types.Message):
#     with open('hardware.txt', 'r', encoding='utf-8') as f:
#         texts = f.read()
#         await message.answer(texts)
#
#
# @dp.message_handler(Text(equals='ЖИДКОСТИ'))
# async def liquids(message: types.Message):
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(types.InlineKeyboardButton(text="Щелочные", callback_data="liquids_standart"))
#     keyboard.add(types.InlineKeyboardButton(text="Солевые", callback_data="liquids_standart"))
#     await message.answer("Выберите какие жидкости вас интересуют", reply_markup=keyboard)
#
#
# @dp.callback_query_handler(text='liquids_standart')
# async def liq_answer(call: types.CallbackQuery):
#     with open('liquids_standart.txt', 'r', encoding='utf-8') as f:
#         texts = f.read()
#         await call.message.answer(texts)
#         await call.answer()


@dp.message_handler(Text(equals='Зарегистрироваться'))
async def process_start_command2(message: types.Message):
    await Form.name.set()
    await message.answer('Введите ваше имя')


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Отлично! теперь ваш номер телефона?")


@dp.message_handler(state=Form.phone_number)
async def process_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
        phone = data['phone_number']
        name = data['name']

    id1 = message.from_user.id
    username = message.from_user.username
    db_object.execute(f'SELECT id FROM users WHERE id = {id1}')
    result = db_object.fetchone()

    if not result:
        db_object.execute('INSERT INTO users(id, username, name, phone_number) VALUES (%s, %s, %s, %s)',
                          (id1, username, name, phone))
        print(id1, username, data['name'], data['phone_number'])
        db_connection.commit()
    await message.reply('Вы зарегистрированы!')
    await state.finish()


@dp.message_handler(commands=['chilldabrek'])
async def process_start_command1(message: types.Message):
    await message.reply("Да да он\ntelegram:\n@kerbadllihc\n\nhttps://github.com/childabrek")


# запускаем лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
