import logging
import asyncio
from datetime import datetime
import parse_doc
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import re

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
# TOKEN = your API token
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def scheduled(wait_for):  
    while True:
        await asyncio.sleep(wait_for)
        parse_doc.one_use()
        parse_doc.hardware()
        parse_doc.liquids_standart()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton(text='ОДНОРАЗКИ')
    but2 = types.KeyboardButton(text='ЖЕЛЕЗО')
    but3 = types.KeyboardButton(text='ЖИДКОСТИ')
    but4 = types.KeyboardButton(text='Задать вопрос')
    keyboard.row(but1, but2, but3).add(but4)
    await message.reply("Привет!", reply_markup=keyboard)


@dp.message_handler(commands=['referal'])
async def referal_start(message: types.Message):
    my_channel_id = -1001478296614
    user_channel_status = await bot.get_chat_member(chat_id=my_channel_id, user_id=message.chat.id)
    user_channel_status = re.findall(r"\w*", str(user_channel_status))
    try:
        if user_channel_status[70] != 'left':
            with open('1.png', mode='rb') as f:
                await bot.send_photo(message.from_user.id, f)
            await bot.send_message(message.from_user.id, 'ок')

        else:
            with open('2.png', mode='rb') as f:
                await bot.send_photo(message.from_user.id, f)
            await bot.send_message(message.chat.id, 'ne ok')
            # Условие для тех, кто не подписан
    except:
        if user_channel_status[60] != 'left':
            with open('1.png', mode='rb') as f:
                await bot.send_photo(message.from_user.id, f)
            await bot.send_message(message.from_user.id, 'ok1')
            # Условие для "подписанных"
        else:
            with open('2.png', mode='rb') as f:
                await bot.send_photo(message.from_user.id, f)
            await bot.send_message(message.from_user.id, 'ne ok1')
            # Условие для тех, кто не подписан


@dp.message_handler(Text(equals='Задать вопрос'))
async def one_use_answer(message: types.Message):
    await message.answer('@siberian_vapor_102')


@dp.message_handler(Text(equals='ОДНОРАЗКИ'))
async def one_use_answer(message: types.Message):
    with open('one_use.txt', 'r', encoding='utf-8') as f:
        texts = f.read()
        await message.answer(texts)


@dp.message_handler(Text(equals='ЖЕЛЕЗО'))
async def hardware_answer(message: types.Message):
    with open('hardware.txt', 'r', encoding='utf-8') as f:
        texts = f.read()
        await message.answer(texts)


@dp.message_handler(Text(equals='ЖИДКОСТИ'))
async def liquids(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Щелочные", callback_data="liquids_standart"))
    keyboard.add(types.InlineKeyboardButton(text="Солевые", callback_data="liquids_standart"))
    await message.answer("Выберите какие жидкости вас интересуют", reply_markup=keyboard)


@dp.callback_query_handler(text='liquids_standart')
async def liq_answer(call: types.CallbackQuery):
    with open('liquids_standart.txt', 'r', encoding='utf-8') as f:
        texts = f.read()
        await call.message.answer(texts)
        await call.answer()


@dp.message_handler(commands=['chilldabrek'])
async def process_start_command(message: types.Message):
    await message.reply("Да да он\ntelegram:\n@kerbadllihc\n\nhttps://github.com/childabrek")


# запускаем лонг поллинг
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(60))  # поставим 10 секунд, в качестве теста

    executor.start_polling(dp, skip_updates=True)
