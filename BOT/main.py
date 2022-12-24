import random
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import numpy as np
import aiohttp

TOKEN = '5975651022:AAE3hp5VDW92XiJrNy4RkfkJiInU5Kcygsk'

bot = AsyncTeleBot(TOKEN)


@bot.message_handler(content_types=["new_chat_members"])
async def adding_new_member(message):
    global users_id
    await bot.send_message(message.chat.id, "Здарова, " + message.from_user.first_name)


jokes = ['Штирлиц надел шляпу набекрень.Набекрень ушла домой без шляпы.',
         'Штирлицу за шиворот упала гусеница. "Где-то взорвался танк," -- подумал Штирлиц.',
         'Штирлиц шёл в Дрезден с трудом разбирая дорогу.\nНаутро железная дорога от Берлина до Дрездена была полностью разобрана...',
         'Жена шизофреника и не подозревает, что её нет',
         'Штирлиц и Мюллер ездили по очереди на танке. Очередь редела, но не расходилась...',
         'Штирлицу попала в голову пуля. "Разрывная," - раскинул мозгами Штирлиц.',
         'Письмо из центра до Штиpлица не дошло... Пришлось читать во второй раз.',
         ]


@bot.message_handler(commands=['menu'])
async def menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text="Стата", callback_data="stat")
    button2 = types.InlineKeyboardButton(text="Кинь анекдот", callback_data="random_joke")
    button3 = types.InlineKeyboardButton(text="Голосовние на продление дедлайна", callback_data="deadline_postponement")
    button4 = types.InlineKeyboardButton(text="Выгнать бота", callback_data="leave")
    markup.add(button1, button2, button3, button4)
    await bot.send_message(message.chat.id, '...Меню...', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: len(callback.data) > 0)
async def actions(callback):
    if callback.data == "stat":
        ch_memb = await bot.get_chat_member_count(callback.message.chat.id)
        admins_list = await bot.get_chat_administrators(callback.message.chat.id)
        await bot.send_message(callback.message.chat.id, "Кол-во участников: " + str(ch_memb))
        await bot.send_message(callback.message.chat.id, "Админ: " + str(len(admins_list)))
        s = ""
        for i in admins_list:
            s += i.user.first_name + '\n'
        await bot.send_message(callback.message.chat.id, "Имя админа:\n" + s)

    elif callback.data == "leave":
        await bot.send_message(callback.message.chat.id, "ОБЩИЙ")
        await bot.leave_chat(callback.message.chat.id)

    elif callback.data == "random_joke":
        index = np.random.randint(0, len(jokes))
        await bot.send_message(callback.message.chat.id, jokes[index])

    elif callback.data == "deadline_postponement":
        await bot.send_poll(callback.message.chat.id, 'Продлить ддл по ИПР?', ['ДА', 'Конечно', 'Продлить'])


asyncio.run(bot.polling())
