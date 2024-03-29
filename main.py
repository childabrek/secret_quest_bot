import logging
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, InputFile
from aiogram.utils import executor
from openpyxl import Workbook
from aiogram.dispatcher import FSMContext
import os
import config

# logs level
logging.basicConfig(level=logging.INFO)
DB_URI = config.DB

# initialization bot
# TOKEN = your API token
bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# DB config local
db_connection = psycopg2.connect(user=config.USER, password=config.PASSWORD,
                                 host=config.HOST,
                                 port=config.PORT, database=config.DATABASE)

# DB config with link
# db_connection = psycopg2.connect(DB_URI, sslmode='require')

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
    await message.reply(f"Чао, {username}!\n "
                        f"Состоишь ли ты в нашей семье?", reply_markup=keyboard)


@dp.message_handler(commands=['referal'])
async def referal_start(message: types.Message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b2 = types.KeyboardButton(text='Проверь ещё раз')
    b3 = types.KeyboardButton(text='Связь)')
    key.add(b2, b3)
    # message.chat.id
    try:
        user_channel_status = await bot.get_chat_member(chat_id=-1001994006638, user_id=message.chat.id)
        print(user_channel_status)
        with open('photo/screen2.jpg', 'rb') as photo:
            await message.answer_photo(photo)
            await process_start_command2(message)
    except:
        await message.answer('Пока тебя не примут в семью, мне не о чем с тобой говорить', reply_markup=key)


@dp.message_handler(text='Проверь ещё раз')
async def referal_start_recheck(message: types.Message):
    await referal_start(message)


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
        # with open('text.txt', 'r', encoding='utf-8') as f:
        #     texts = f.read()
        # await bot.send_photo(message.chat.id, photo=InputFile('1.jpg'), caption=texts, reply_markup=keyboard)
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
    await message.reply(f'Отлично, твой номер: {result1}', reply_markup=keyboard)
    await state.finish()


@dp.message_handler(Text(equals='excel'))
async def excel(message: types.Message):
    db_object.execute(f'SELECT * FROM users')
    for i in db_object.fetchall():
        ws.append(i)
    # Save the file
    wb.save("sample.xlsx")
    await message.answer_document(open("sample.xlsx", 'rb'))
    os.remove('sample.xlsx')


# @dp.message_handler(commands=['tellall'])
# async def mailing(message: types.Message):
#     keyboard.add(types.reply_keyboard.KeyboardButton(text='Зарегистрироваться'))
#     for i in range(1):
#         await bot.send_message(chat_id='881012147',
#                                text="Тестовая рассылка", reply_markup=keyboard)


# запускаем лонг поллинг
if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception:
            pass
