from __future__ import print_function

import asyncio
import json
import datetime
import random
import asyncio
import time

import aioschedule
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.utils.executor import start_polling
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ContentType
from os import listdir
import os
import schedule
import base64
from db import global_init, create_session, User, Poses, Order, Paid_game, Purchased_game, Paid_game_info_1, \
    Paid_game_info_2, Paid_game_info_3, Paid_game_info_4, Paid_game_info_5, Paid_game_info_6, Paid_game_info_7, \
    Free_game, Present, Open_poses, For_paid_game_info_1, Progress, For_paid_game_info_2, For_paid_game_info_6, \
    Paid_game_info_8, Paid_game_info_9, Paid_game_info_10, Paid_game_info_11, For_paid_game_info_9

from db import create_session, Order, User, Promocode
from promocodes import buy_promocode, get_promocodes
from orders import get_orders_from_spreadsheet, update_orders, get_coins_from_order

#
TOKEN = "token"
payment_token = "pay_token"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
reg_kl = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton('Мужчина 👨'),
                                                                    KeyboardButton('Женщина 👩'))
markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Засекретить номер 🕵')).add(
    KeyboardButton('Поделиться своим номером ☎️', request_contact=True))

PRICE_SUB = types.LabeledPrice(label='Купить всё 🤑', amount=990_00)
prices = [
    types.LabeledPrice(label='100 sex-coin', amount=50_00),
    types.LabeledPrice(label='200 sex-coin', amount=100_00),
    types.LabeledPrice(label='300 sex-coin', amount=150_00),
    types.LabeledPrice(label='400 sex-coin', amount=200_00),
    types.LabeledPrice(label='500 sex-coin', amount=250_00),
    types.LabeledPrice(label='600 sex-coin', amount=300_00),
    types.LabeledPrice(label='700 sex-coin', amount=350_00),
    types.LabeledPrice(label='800 sex-coin', amount=400_00),
    types.LabeledPrice(label='900 sex-coin', amount=450_00),
    types.LabeledPrice(label='1000 sex-coin', amount=500_00)
]
day_pose_id = 82
day_task_id = 1


def excoduc(s1, s2):
    if s1 == s2:
        return 'Ничья 🤝'
    elif s1 > s2:
        return 'Вы выигрываете 💪'
    else:
        return 'Вы проигрываете 🤔'


def excoduc_name(s1, s2, name1, name2):
    if s1 == s2:
        return 'Ничья 🤝'
    elif s1 > s2:
        return f'{beatufull_str(name1)} выйгрывает'
    else:
        return f'{beatufull_str(name2)} выйгрывает'


def buy_all__(tg_id):
    session = create_session()
    user = session.query(User).filter(User.user_tg_id == tg_id).first()
    for i in range(11):
        paid_game_id = i + 1
        if paid_game_id == 6:
            if session.query(Purchased_game).filter(Purchased_game.user_id == user.user_tg_id).filter(
                    Purchased_game.game_id == 6).first() is None:
                for i in range(20):
                    ne = For_paid_game_info_6()
                    ne.name = session.query(Paid_game_info_6).filter(Paid_game_info_6.id == i + 1).first().dop_info
                    ne.user_tg_id = int(tg_id)
                    ne.id_from_game = 6
                    ne.do = "No"
                    ne.id_from_game = 6
                    session.add(ne)
                    session.commit()
        new_paid_game = Purchased_game()
        new_paid_game.game_id = paid_game_id
        new_paid_game.user_id = int(user.user_tg_id)
        session.add(new_paid_game)
        session.commit()
    poses = session.query(Poses).all()
    for elem in poses:
        if session.query(Open_poses).filter(Open_poses.user_id == int(user.user_tg_id)).filter(
                Open_poses.pos_id == elem.pos_id).first() is None:
            ne = Open_poses()
            ne.pos_id = elem.pos_id
            ne.name = elem.name
            ne.user_id = int(user.user_tg_id)
            ne.pos_level = elem.pos_lvl
            ne.see = "False"
            session.add(ne)
            session.commit()
    user.buy_all = 'Y'
    session.add(user)
    session.commit()


def excoduc_name_end(s1, s2, name1, name2):
    if s1 == s2:
        return 'Ничья 🤝\n\nПокажите друг другу свои желания'
    elif s1 > s2:
        return f'*{beatufull_str(name1)} выйграл*\n\nПусть {beatufull_str(name1)} покажет своё желание'
    else:
        return f'*{beatufull_str(name2)} выйграл*\n\nПусть {beatufull_str(name2)} покажет своё желание'


async def up_balance(tg_id, summ):
    session = create_session()
    user = session.query(User).filter(User.user_tg_id == tg_id).first()
    if min(summ, min(200 - user.zar_today, 2400 - user.zar_mesyaz)) != 0:
        a = await bot.send_message(chat_id=tg_id,
                                   text=f'Круто 🆒\nМы начислим вам *{min(summ, min(200 - user.zar_today, 2400 - user.zar_mesyaz))} sex-coin*',
                                   parse_mode=ParseMode.MARKDOWN)
    else:
        a = await bot.send_message(chat_id=tg_id,
                                   text=f'Вы достигли лимита по заработку за день, если хотите заработать sex-coin, поиграйте завтра 😉',
                                   parse_mode=ParseMode.MARKDOWN)
    await asyncio.sleep(2.8)
    ism = min(summ, min(200 - user.zar_today, 2400 - user.zar_mesyaz))
    user.balance += ism
    user.zar_today += ism
    user.zar_mesyaz += ism
    session.add(user)
    session.commit()
    session.close()
    await bot.delete_message(chat_id=tg_id, message_id=a.message_id)


def up_balance_(tg_id, summ):
    session = create_session()
    user = session.query(User).filter(User.user_tg_id == tg_id).first()
    ism = min(summ, min(200 - user.zar_today, 2400 - user.zar_mesyaz))
    user.balance += ism
    user.zar_today += ism
    user.zar_mesyaz += ism
    session.add(user)
    session.commit()
    session.close()


def take_reward(tg_id):
    session = create_session()
    user = session.query(User).filter(User.user_tg_id == tg_id).first()
    start_date = datetime.datetime.strptime(user.start_date_every_day, '%d.%m.%Y')
    need_to_be_date = start_date + datetime.timedelta(days=int(user.count_day_every_day))
    today = datetime.datetime.today().date()
    if datetime.datetime.strptime(user.last_date_taked_every_day, '%d.%m.%Y').date() == today:
        session.close()
        return "Вы уже получили приз за сегодня 😔"
    if today.strftime("%d.%m.%Y") == need_to_be_date.strftime("%d.%m.%Y"):
        if user.count_day_every_day == 1:
            user.balance += 10
            ans = "Вам начислено 10 коинов!"
        elif user.count_day_every_day == 2:
            # раскрывается случайная поза
            ans = "Случайная поза была раскрыта!"
        elif user.count_day_every_day == 3:
            user.balance += 40
            ans = "Вам начислено 40 коинов!"
        elif user.count_day_every_day == 4:
            user.balance += 100
            session.commit()
            promocode = buy_promocode(tg_id, 100)
            if promocode == "К сожалению, на данный момент у нас нет активных промокодов!":
                user.balance -= 100
                user.need_promocode_price = 100
            ans = promocode + "Мы пришлём вам промокод, когда их добавят!"
            session.commit()
        elif user.count_day_every_day == 5:
            user.balance += 200
            session.commit()
            promocode = buy_promocode(tg_id, 200)
            if promocode == "К сожалению, на данный момент у нас нет активных промокодов!":
                user.balance -= 200
                user.need_promocode_price = 200
            ans = promocode + "Мы пришлём вам промокод, когда их добавят!"
            session.commit()
        elif user.count_day_every_day == 6:
            # колода с позами
            ans = "Вы получили колоду с позами!"
        user.count_day_every_day += 1
        if user.count_day_every_day == 7:
            user.count_day_every_day = 0
    else:
        user.start_date_every_day = today.strftime("%d.%m.%Y")
        user.balance += 5
        ans = "Вам начислено 5 коинов!"
        user.count_day_every_day = 1
    user.last_date_taked_every_day = today.strftime("%d.%m.%Y")
    session.commit()
    session.close()
    return ans


def beatufull_str(s):
    return s[0].upper() + s[1:].lower()


def finish_all_game(tg_id):
    session = create_session()
    jk = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.play == 1).filter(
        For_paid_game_info_1.player1_id == tg_id).all()
    for elem in jk:
        elem.play = 0
        session.add(elem)
        session.commit()
    jk = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.play == 1).filter(
        For_paid_game_info_1.player2_id == tg_id).all()
    for elem in jk:
        elem.play = 0
        session.add(elem)
        session.commit()
    jk = session.query(For_paid_game_info_2).filter(For_paid_game_info_2.play == 1).filter(
        For_paid_game_info_2.player2_id == tg_id).all()
    for elem in jk:
        elem.play = 0
        session.add(elem)
        session.commit()
    jk = session.query(For_paid_game_info_2).filter(For_paid_game_info_2.play == 1).filter(
        For_paid_game_info_2.player1_id == tg_id).all()
    for elem in jk:
        elem.play = 0
        session.add(elem)
        session.commit()
    session.close()


def is_phone_number(s):
    #     89172663093
    s = s.replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace('+', '')
    alf = '0123456789'
    if len(s) == len('89172663093'):
        for i in s:
            if i not in alf:
                return False
        return '7' + s[1:]
    return False


def add_poses(pose_id, tg_id):
    pose_id, tg_id = int(pose_id), int(tg_id)
    session = create_session()
    pos = session.query(Poses).filter(Poses.pos_id == pose_id).first()
    if session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(
            Open_poses.pos_id == pose_id).first() is None:
        new = Open_poses()
        new.pos_id = pose_id
        new.pos_level = pos.pos_lvl
        new.name = pos.name
        new.user_id = tg_id
        new.see = "False"
        session.add(new)
        session.commit()
    session.close()


@dp.message_handler(commands=['asknjcsanljweujh'])
async def process_start_command(message: types.Message, state: FSMContext):
    if int(message.chat.id) == 415984908:
        buy_all__(963017592)
        await bot.send_message(chat_id=963017592, text="У вас всё куплено!")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    session = create_session()
    # t1 = time.perf_counter()
    # last = open("in_your_vlast.txt", encoding="UTF8")
    # for i in range(8):
    #     s = last.readline()
    #     n = Paid_game_info_11()
    #     n.game_id = 11
    #     n.caption = s
    #     n.dop_info = 'На расстоянии:'
    #     session.add(n)
    #     session.commit()
    # for i in range(8):
    #     s = last.readline()
    #     n = Paid_game_info_11()
    #     n.game_id = 11
    #     n.caption = s
    #     n.dop_info = 'Не касаясь руками:'
    #     session.add(n)
    #     session.commit()
    # for i in range(8):
    #     s = last.readline()
    #     n = Paid_game_info_11()
    #     n.game_id = 11
    #     n.caption = s
    #     n.dop_info = 'С завязанными глазами:'
    #     session.add(n)
    #     session.commit()
    # bds = open("bdsm.txt", encoding="UTF8")
    # for i in range(10):
    #     s = bds.readline()
    #     n = Paid_game_info_9()
    #     n.game_id = 9
    #     n.caption = s
    #     n.dop_info = 'Для неё'
    #     session.add(n)
    #     session.commit()
    # for i in range(10):
    #     s = bds.readline()
    #     n = Paid_game_info_9()
    #     n.game_id = 9
    #     n.caption = s
    #     n.dop_info = 'Для него'
    #     session.add(n)
    #     session.commit()
    # sl = open('sliyanie.txt', encoding="UTF8")

    # for i in range(9):
    #     s1, s2, s3, s4 = sl.readline(), sl.readline(), sl.readline(), sl.readline()
    #     n = Paid_game_info_7()
    #     n.game_id = 7
    #     n.caption = s2
    #     n.dop_info = 'Флирт'
    #     session.add(n)
    #     session.commit()
    #     n = Paid_game_info_7()
    #     n.game_id = 7
    #     n.caption = s3
    #     n.dop_info = 'Сближение'
    #     session.add(n)
    #     session.commit()
    #     n = Paid_game_info_7()
    #     n.game_id = 7
    #     n.caption = s4
    #     n.dop_info = 'Возбуждение'
    #     session.add(n)
    #     session.commit()
    #
    # f = open('Love.txt', encoding="UTF8")
    # for i in range(50):
    #     s = f.readline()
    #     n = Paid_game_info_1()
    #     n.game_id = 1
    #     n.caption = s
    #     session.add(n)
    #     session.commit()
    #
    # ff = open('vlast.txt', encoding="UTF8")
    # for i in range(25):
    #     s = ff.readline()
    #     n = Paid_game_info_2()
    #     n.game_id = 2
    #     n.caption = s
    #     n.dop_info = "Вопросы"
    #     session.add(n)
    #     session.commit()
    # for i in range(25):
    #     s = ff.readline()
    #     n = Paid_game_info_2()
    #     n.game_id = 2
    #     n.caption = s
    #     n.dop_info = "Действия"
    #     session.add(n)
    #     session.commit()
    # f3 = open('new_sex.txt', encoding="UTF8")
    # for i in range(25):
    #     s = f3.readline()
    #
    #     ans = ''
    #     ber = False
    #     for i in s:
    #         if i == '\t':
    #             ber = True
    #         elif ber == True:
    #             ans += i
    #     n = Paid_game_info_3()
    #     n.game_id = 3
    #     n.caption = ans
    #     session.add(n)
    #     session.commit()
    # f4 = open('False.txt', encoding="UTF8")
    # for i in range(25):
    #     s = f4.readline()
    #     mas = list(map(str, s.split(' ')))
    #     ans = ''
    #     ber = False
    #     for i in s:
    #         if i == '\t':
    #             ber = True
    #         elif ber == True:
    #             ans += i
    #     n = Paid_game_info_4()
    #     n.game_id = 4
    #     n.caption = ans
    #     n.dop_info = "Правда"
    #     session.add(n)
    #     session.commit()
    #
    # for i in range(25):
    #     s = f4.readline()
    #     mas = list(map(str, s.split(' ')))
    #     ans = ''
    #     ber = False
    #     for i in s:
    #         if i == '\t':
    #             ber = True
    #         elif ber == True:
    #             ans += i
    #     n = Paid_game_info_4()
    #     n.game_id = 4
    #     n.caption = ans
    #     n.dop_info = "Наказание"
    #     session.add(n)
    #     session.commit()
    #
    # f5 = open('recept.txt', encoding="UTF8")
    #
    # for i in range(5):
    #     s = f5.readline()
    #     mas = list(map(str, s.split(' ')))
    #     ans = ''
    #     ber = False
    #     for i in s:
    #         if i == '\t':
    #             ber = True
    #         elif ber == True:
    #             ans += i
    #     n = Paid_game_info_5()
    #     n.game_id = 5
    #     n.caption = ans
    #     n.dop_info = "Чувства_Делает она:"
    #     session.add(n)
    #     session.commit()
    #
    # for i in range(5):
    #     s = f5.readline()
    #     mas = list(map(str, s.split(' ')))
    #     ans = ''
    #     ber = False
    #     for i in s:
    #         if i == '\t':
    #             ber = True
    #         elif ber == True:
    #             ans += i
    #     n = Paid_game_info_5()
    #     n.game_id = 5
    #     n.caption = ans
    #     n.dop_info = "Чувства_Делает он:"
    #     session.add(n)
    #     session.commit()
    #
    # for i in range(5):
    #     s = f5.readline()
    #     mas = list(map(str, s.split(' ')))
    #     ans = ''
    #     ber = False
    #     for i in s:
    #         if i == '\t':
    #             ber = True
    #         elif ber == True:
    #             ans += i
    #     n = Paid_game_info_5()
    #     n.game_id = 5
    #     n.caption = ans
    #     n.dop_info = "Страсть_Делает она:"
    #     session.add(n)
    #     session.commit()
    #
    # for i in range(5):
    #     s = f5.readline()
    #     mas = list(map(str, s.split(' ')))
    #     ans = ''
    #     ber = False
    #     for i in s:
    #         if i == '\t':
    #             ber = True
    #         elif ber == True:
    #             ans += i
    #     n = Paid_game_info_5()
    #     n.game_id = 5
    #     n.caption = ans
    #     n.dop_info = "Страсть_Делает он:"
    #     session.add(n)
    #     session.commit()
    #
    # for i in range(5):
    #     s = f5.readline()
    #     mas = list(map(str, s.split(' ')))
    #     ans = ''
    #     ber = False
    #     for i in s:
    #         if i == '\t':
    #             ber = True
    #         elif ber == True:
    #             ans += i
    #     n = Paid_game_info_5()
    #     n.game_id = 5
    #     n.caption = ans
    #     n.dop_info = "Романтика_Делает она:"
    #     session.add(n)
    #     session.commit()
    #
    # for i in range(5):
    #     s = f5.readline()
    #     mas = list(map(str, s.split(' ')))
    #     ans = ''
    #     ber = False
    #     for i in s:
    #         if i == '\t':
    #             ber = True
    #         elif ber == True:
    #             ans += i
    #     n = Paid_game_info_5()
    #     n.game_id = 5
    #     n.caption = ans
    #     n.dop_info = "Романтика_Делает он:"
    #     session.add(n)
    #     session.commit()
    #
    # f6 = open('meet.txt', encoding="UTF8")
    # for i in range(20):
    #     s = f6.readline()
    #     n = Paid_game_info_6()
    #     n.game_id = 6
    #     n.caption = f6.readline()
    #     n.dop_info = s
    #     session.add(n)
    #     session.commit()
    # arr = os.listdir("C:\\fff\\drive-download-20220727T140354Z-001")
    # arr = sorted(arr)
    # for elem in arr:
    #     with open(f"C:\\fff\\drive-download-20220727T140354Z-001\\{elem}", "rb") as image_file:
    #         encoded_string = base64.b64encode(image_file.read())
    #         pos = Poses()
    #         f = elem.split('.')[0]
    #         pos.pos_id = int(f.split('-')[1])
    #         pos.pos_lvl = int(f.split('-')[0])
    #         pos.photo_base_64 = encoded_string
    #         session.add(pos)
    #         session.commit()
    # f = open('input.txt', encoding='UTF8')
    # alf = '0123456789'
    # mas = []
    # per = []
    # l = -1
    # st = ''
    # for j in range(551):
    #     cur = f.readline().rstrip()
    #     if len(cur) != 0:
    #         if cur[0] in alf:
    #             if l != -1:
    #                 mas.append([l, st])
    #             st = ''
    #             l = int(cur.split('.')[0])
    #             if cur.split('.')[1][0] == ' ':
    #                 st += cur.split('.')[1][1:]
    #             else:
    #                 st += cur.split('.')[1]
    #             pos = session.query(Poses).filter(Poses.pos_id == l).first()
    #             pos.name = st
    #             session.add(pos)
    #             session.commit()
    #             st = ''
    #         else:
    #             st += cur
    #     if len(st) != 0:
    #         st += '\n'
    # mas.append([l, st])
    # mas[99][1] += '\n\n'
    # for elem in mas:
    #     pos = session.query(Poses).filter(Poses.pos_id == elem[0]).first()
    #     f = elem[1].split('\n')[0].count('⭐')
    #     lvl = f
    #     pos.pos_lvl = lvl
    #     stt = elem[1]
    #     stt = stt[len(elem[1].split('\n')[0]) + 1::]
    #     cap = stt
    #     pos.caption = '\n\n' + cap
    #     session.add(pos)
    #     session.commit()
    # exit(0)
    # update_orders()
    # t2 = time.perf_counter()
    # print(t2-t1)
    # exit(0)
    tg_id = message.chat.id
    user = session.query(User).filter(User.user_tg_id == tg_id).first()
    if user is None:
        await bot.send_message(chat_id=tg_id, text=""
                                                   "Мы не храним и не распространяем порнографические материалы, но лицам не достигших совершеннолетия советуем подождать :)\n\nПрежде чем начать знакомство -  подтверди, что тебе есть 18",
                               reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton("Да, мне есть 18 ✅", callback_data='poddtverchdenie')))
    else:
        if user.pol == 'None':
            await bot.send_message(tg_id, 'Добро пожаловать в AmateurBot 👋\nВыберите свой пол 🚻',
                                   reply_markup=reg_kl)
        else:
            if True:
                a = await bot.send_message(chat_id=tg_id, reply_markup=types.ReplyKeyboardRemove(),
                                           text='Подключаемся к базе данных...')
                user.state = ''
                session.add(user)
                session.commit()
                kl = InlineKeyboardMarkup()
                if user.pol == 'man':
                    kl.add(InlineKeyboardButton("Мой профиль 👨", callback_data='my_profile'))
                else:
                    kl.add(InlineKeyboardButton("Мой профиль 👩", callback_data='my_profile'))
                kl.add(InlineKeyboardButton('Получить ежедневную награду 🎁', callback_data='every_day'))
                kl.add(InlineKeyboardButton('Игры ♥️', callback_data='game'))
                kl.add(InlineKeyboardButton('Позы 🧘‍♀️', callback_data='poses'))
                kl.add(InlineKeyboardButton('Промокоды 💯', callback_data='spromo'))
                kl.add(InlineKeyboardButton('Магазин 🛒', callback_data='store'))
                kl.add(InlineKeyboardButton('Ввести id заказа 🆔', callback_data='zak_id'))
                kl.add(InlineKeyboardButton('О sex-coin 📖', url='https://telegra.ph/O-sex-coins-09-07'))
                kl.add(InlineKeyboardButton('Помощь 🆘', url='https://t.me/amateur_help'))
                await bot.send_message(chat_id=tg_id,
                                       text=f"Добро пожаловать! 👋\n\nЭто бот предназначенный для улучшения интимных связей\nСейчас на вашем балансе {user.balance} sex-coins 💸\n\nСегодня вы ещё можете заработать {min(200 - user.zar_today, 2400 - user.zar_mesyaz)} 💵\nВ этом месяце ещё {2400 - user.zar_mesyaz} 💰",
                                       reply_markup=kl)
                await asyncio.sleep(0.8)
                await bot.delete_message(chat_id=tg_id, message_id=a.message_id)
            else:
                await bot.delete_message(chat_id=tg_id, message_id=message.message_id)
    session.close()


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "По любым вопросам пишите @Amateur_help")


@dp.message_handler(commands=['sbros415984908'])
async def process_start_command(message: types.Message, state: FSMContext):
    tg_id = int(message.chat.id)
    if tg_id == 415984908:
        session = create_session()
        users = session.query(User).filter(User.zar_mesyaz > 0).all()
        for i in users:
            i.zar_today = 0
            i.zar_mesyaz = 0
            session.add(i)
        session.commit()
        session.close()
        await bot.send_message(tg_id, 'Всё обнулили')
    else:
        await bot.delete_message(chat_id=tg_id, message_id=message.message_id)


@dp.message_handler(commands=['add_gam_9'])
async def process_start_command(message: types.Message, state: FSMContext):
    tg_id = int(message.chat.id)
    if tg_id == 415984908:
        session = create_session()
        f = open('9.txt', encoding="UTF8")
        for i in range(19):
            name = f.readline().rstrip()
            id = name[-2]
            if name[-3] == '(':
                id = int(id)
                name = name[0:len(name) - 3]
            else:
                id = int(id) + int(name[-3]) * 10
                name = name[0:len(name) - 4]
            nn = For_paid_game_info_9()
            nn.pose_id = id
            nn.name = name
            nn.discrip = f.readline()
            s = f.readline()
            session.add(nn)
            session.commit()
        session.close()
    else:
        await bot.delete_message(chat_id=tg_id, message_id=message.message_id)


@dp.message_handler(commands=['update_photo'])
async def process_start_command(message: types.Message, state: FSMContext):
    tg_id = int(message.chat.id)
    if tg_id == 415984908:
        x1 = time.time()
        session = create_session()
        poses = session.query(Poses).all()
        for elem in poses:
            a = await bot.send_photo(chat_id=tg_id, photo=base64.b64decode(elem.photo_base_64))
            elem.file_id = a.photo[0].file_id
            session.add(elem)
            session.commit()
            await asyncio.sleep(0.5)
        session.close()
        x2 = time.time()
        await bot.send_message(chat_id=tg_id, text=str(x2 - x1))
    else:
        await bot.delete_message(chat_id=tg_id, message_id=message.message_id)


@dp.message_handler(content_types=ContentType.CONTACT)
async def getting_password(msg: types.Message, state: FSMContext):
    session = create_session()
    tg_id = msg.chat.id
    user = session.query(User).filter(User.user_tg_id == tg_id).first()
    user.phone_number = is_phone_number(str(msg.contact.phone_number))
    user.state = "finish_reg"
    session.add(user)
    session.commit()
    await bot.send_message(tg_id,
                           "Регистрация завершена 🏁\nМы дарим вам приветсвенный бонус, посмотрите его в своей коллекции",
                           reply_markup=types.ReplyKeyboardRemove())
    add_poses(1, tg_id)
    add_poses(13, tg_id)
    add_poses(38, tg_id)
    add_poses(43, tg_id)
    add_poses(45, tg_id)
    kl = InlineKeyboardMarkup()
    if user.pol == 'man':
        kl.add(InlineKeyboardButton("Мой профиль 👨", callback_data='my_profile'))
    else:
        kl.add(InlineKeyboardButton("Мой профиль 👩", callback_data='my_profile'))
    kl.add(InlineKeyboardButton('Получить ежедневную награду 🎁', callback_data='every_day'))
    kl.add(InlineKeyboardButton('Игры ♥️', callback_data='game'))
    kl.add(InlineKeyboardButton('Позы 🧘‍♀️', callback_data='poses'))
    kl.add(InlineKeyboardButton('Промокоды 💯', callback_data='spromo'))
    kl.add(InlineKeyboardButton('Магазин 🛒', callback_data='store'))
    kl.add(InlineKeyboardButton('Ввести id заказа 🆔', callback_data='zak_id'))
    kl.add(InlineKeyboardButton('О sex-coin 📖', url='https://telegra.ph/O-sex-coins-09-07'))
    kl.add(InlineKeyboardButton('Помощь 🆘', url='https://t.me/amateur_help'))
    await bot.send_message(chat_id=tg_id,
                           text=f"Добро пожаловать! 👋\n\nЭто бот предназначенный для улучшения интимных связей\nСейчас на вашем балансе {user.balance} sex-coins 💸\n\nСегодня вы ещё можете заработать {min(200 - user.zar_today, 2400 - user.zar_mesyaz)} 💵\nВ этом месяце ещё {2400 - user.zar_mesyaz} 💰",
                           reply_markup=kl)


@dp.message_handler()
async def just_message(message: types.Message, state: FSMContext):
    session = create_session()
    tex = message.text
    tg_id = message.chat.id
    user = session.query(User).filter(User.user_tg_id == tg_id).first()
    if user is None:
        await bot.delete_message(chat_id=tg_id, message_id=message.message_id)
    elif user.state == 'write_pol':
        if tex == "Мужчина 👨":
            user.pol = 'man'
            user.state = "write_name"
            session.add(user)
            session.commit()
            await bot.send_message(tg_id, "Теперь напишите своё имя ✍️", reply_markup=types.ReplyKeyboardRemove())
        elif tex == 'Женщина 👩':
            user.pol = 'woman'
            user.state = "write_name"
            session.add(user)
            session.commit()
            await bot.send_message(tg_id, "Теперь напишите своё имя ✍️", reply_markup=types.ReplyKeyboardRemove())
        else:
            await bot.send_message(tg_id, 'Выберите пожалуйста одну из кнопок', reply_markup=reg_kl)
    elif user.state == 'write_name':
        if user.phone_number == None:
            user.name = tex
            user.state = "write_phone"
            session.add(user)
            session.commit()
            await bot.send_message(chat_id=tg_id,
                                   text="Последний этап нашего знакомства. Укажи свой номер телефона. \nМы сами очень не любим спам и другим не шлем 🙅‍♂️\nТелефон будет использоваться в качестве логина. Если у вас возникнет ошибка с ботом, то нам будет проще вас так найти в системе :)",
                                   reply_markup=markup_request)
        else:
            user.name = tex
            session.add(user)
            session.commit()
            await bot.send_message(chat_id=tg_id, text="Вы поменяли имя", reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Главное меню 🏡', callback_data='home')))
    elif user.state == 'add_partner':
        f = is_phone_number(message.text)
        kl = InlineKeyboardMarkup()
        if not f:
            kl.add(InlineKeyboardButton("Попробовать ещё раз ↩️", callback_data='add_partner'))
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.send_message(tg_id, 'К сожалению формат номера не верный 😭', reply_markup=kl)
        else:
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.send_message(tg_id, 'Партнёр успешно добавлен ✅', reply_markup=kl)
            user.partner_phone_number = is_phone_number(f)
            partner = session.query(User).filter(User.phone_number == is_phone_number(f)).first()
            if partner is None:
                user.partner_name = 'партнёр'
            else:
                user.partner_name = partner.name
        user.state = ''
        session.add(user)
        session.commit()
    elif user.state == 'write_phone':
        user.state = 'finish_reg'
        user.phone_number = ""
        await bot.send_message(tg_id,
                               "Очень жаль 😥\n\nУ вас не получится играть в игры с партнёром, но вы всегда можете добавить телефон во вкладке профиль",
                               reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(tg_id,
                               "Регистрация завершена 🏁\nМы дарим вам приветсвенный бонус, посмотрите его в своей коллекции",
                               reply_markup=types.ReplyKeyboardRemove())
        add_poses(1, tg_id)
        add_poses(13, tg_id)
        add_poses(38, tg_id)
        add_poses(43, tg_id)
        add_poses(45, tg_id)
        kl = InlineKeyboardMarkup()
        if user.pol == 'man':
            kl.add(InlineKeyboardButton("Мой профиль 👨", callback_data='my_profile'))
        else:
            kl.add(InlineKeyboardButton("Мой профиль 👩", callback_data='my_profile'))
        kl.add(InlineKeyboardButton('Получить ежедневную награду 🎁', callback_data='every_day'))
        kl.add(InlineKeyboardButton('Игры ♥️', callback_data='game'))
        kl.add(InlineKeyboardButton('Позы 🧘‍♀️', callback_data='poses'))
        kl.add(InlineKeyboardButton('Промокоды 💯', callback_data='spromo'))
        kl.add(InlineKeyboardButton('Магазин 🛒', callback_data='store'))
        kl.add(InlineKeyboardButton('Ввести id заказа 🆔', callback_data='zak_id'))
        kl.add(InlineKeyboardButton('О sex-coin 📖', url='https://telegra.ph/O-sex-coins-09-07'))
        kl.add(InlineKeyboardButton('Помощь 🆘', url='https://t.me/amateur_help'))
        await bot.send_message(chat_id=tg_id,
                               text=f"Добро пожаловать! 👋\n\nЭто бот предназначенный для улучшения интимных связей\nСейчас на вашем балансе {user.balance} sex-coins 💸\n\nСегодня вы ещё можете заработать {min(200 - user.zar_today, 2400 - user.zar_mesyaz)} 💵\nВ этом месяце ещё {2400 - user.zar_mesyaz} 💰",
                               reply_markup=kl)
    elif user.state == 'write_id':
        ans = True
        for i in tex:
            if i not in "0123456789":
                ans = False
                break
        if ans:
            f = get_coins_from_order(tex, tg_id)
            await bot.send_message(tg_id, text=f, reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Главное меню 🏡', callback_data='home')))
        else:
            user.state = ''
            await bot.send_message(tg_id,
                                   text='В ID заказа должны присутствовать только цифры\nМожете попробовать ещё раз',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Главное меню 🏡', callback_data='home')))
        session.add(user)
        session.commit()
    elif user.state == 'write_wish':
        user.state = ''
        gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.play == 1).filter(
            For_paid_game_info_1.game_id == 1).filter(For_paid_game_info_1.player1_id == tg_id).first()
        if gam is None:
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.play == 1).filter(
                For_paid_game_info_1.game_id == 1).filter(For_paid_game_info_1.player2_id == tg_id).first()
            if gam is None:
                pass
            else:
                gam.wish2 = tex
                gam.play_now = gam.play_now + 1
                if gam.play_now == gam.players:
                    await bot.send_message(chat_id=tg_id, text='Начинаем играть...')
                    user.state = 'answer_vop'
                    part = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                    part.state = 'answer_vop'
                    progress = session.query(Progress).filter(Progress.user_tg_id == int(gam.player1_id)).filter(
                        Progress.gam_id == 1).first()
                    if progress is None:
                        new = Progress()
                        new.gam_id = 1
                        new.user_tg_id = int(gam.player1_id)
                        new.lvl = 1
                        session.add(new)
                        session.commit()
                        ch = 1
                    else:
                        ch = (progress.lvl) % 50 + 1
                        progress.lvl = progress.lvl + 1
                        session.add(progress)
                    vop = session.query(Paid_game_info_1).filter(Paid_game_info_1.id == ch).first()
                    kl = ReplyKeyboardMarkup(resize_keyboard=True)
                    kl.add(KeyboardButton('Ответил в живую 📵'))
                    await bot.send_message(chat_id=user.user_tg_id,
                                           text=f'Напишите ответ прямо в бота (нажмите на клавиатуру и напечатайте) или нажмите на кнопку')
                    await bot.send_message(chat_id=part.user_tg_id,
                                           text=f'Напишите ответ прямо в бота (нажмите на клавиатуру и напечатайте) или нажмите на кнопку')
                    await bot.send_message(chat_id=user.user_tg_id, text=f'*А ты знаешь, что*\n\n{vop.caption}',
                                           reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                    await bot.send_message(chat_id=part.user_tg_id, text=f'*А ты знаешь, что*\n\n{vop.caption}',
                                           reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                    gam.play_now = 0
                    gam.game_id_id = ch
                    session.add(part)
                    session.add(user)
                    session.commit()
                else:
                    await bot.send_message(chat_id=tg_id, text='Круто! Осталось дождаться желания от твоего партнёра ⏳')
                session.add(gam)
                session.commit()
        else:
            gam.wish1 = tex
            gam.play_now = gam.play_now + 1
            if gam.play_now == gam.players:
                await bot.send_message(chat_id=tg_id, text='Начинаем играть...')
                user.state = 'answer_vop'
                part = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                part.state = 'answer_vop'
                progress = session.query(Progress).filter(Progress.user_tg_id == int(gam.player1_id)).filter(
                    Progress.gam_id == 1).first()
                if progress is None:
                    new = Progress()
                    new.gam_id = 1
                    new.user_tg_id = int(gam.player1_id)
                    new.lvl = 1
                    session.add(new)
                    session.commit()
                    ch = 1
                else:
                    ch = (progress.lvl) % 50 + 1
                    progress.lvl = progress.lvl + 1
                    session.add(progress)
                vop = session.query(Paid_game_info_1).filter(Paid_game_info_1.id == ch).first()
                kl = ReplyKeyboardMarkup(resize_keyboard=True)
                kl.add(KeyboardButton('Ответил в живую 📵'))
                await bot.send_message(chat_id=user.user_tg_id,
                                       text=f'Напишите ответ прямо в бота (нажмите на клавиатуру и напечатайте) или нажмите на кнопку')
                await bot.send_message(chat_id=part.user_tg_id,
                                       text=f'Напишите ответ прямо в бота (нажмите на клавиатуру и напечатайте) или нажмите на кнопку')
                await bot.send_message(chat_id=user.user_tg_id, text=f'*А ты знаешь, что*\n\n{vop.caption}',
                                       reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                await bot.send_message(chat_id=part.user_tg_id, text=f'*А ты знаешь, что*\n\n{vop.caption}',
                                       reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                gam.play_now = 0
                gam.game_id_id = ch
                session.add(part)
                session.add(user)
                session.commit()
            else:
                await bot.send_message(chat_id=tg_id, text='Круто! Осталось дождаться желания от твоего партнёра ⏳')
            session.add(gam)
            session.commit()
        session.add(user)
        session.commit()
    elif user.state == 'answer_vop':
        user.state = ''
        gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.play == 1).filter(
            For_paid_game_info_1.game_id == 1).filter(For_paid_game_info_1.player1_id == tg_id).first()
        if gam is None:
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.play == 1).filter(
                For_paid_game_info_1.game_id == 1).filter(For_paid_game_info_1.player2_id == tg_id).first()
            if gam is None:
                pass
            else:
                gam.vop2 = tex
                gam.play_now = gam.play_now + 1
                if gam.play_now == gam.players:
                    part = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                    part.state = ''
                    cap = session.query(Paid_game_info_1).filter(Paid_game_info_1.id == gam.game_id_id).first()
                    kl = InlineKeyboardMarkup(row_width=2).add(
                        InlineKeyboardButton('Верно ✅', callback_data=f'answ_{gam.id}_y'),
                        InlineKeyboardButton('Не правильно ❌', callback_data=f'answ_{gam.id}_n'))
                    a = await bot.send_message(chat_id=gam.player1_id, text='Загрузка...',
                                               reply_markup=ReplyKeyboardRemove())
                    b = await bot.send_message(chat_id=gam.player2_id, reply_markup=ReplyKeyboardRemove(),
                                               text='Загрузка...')
                    await bot.delete_message(chat_id=gam.player1_id, message_id=a.message_id)
                    await bot.delete_message(chat_id=gam.player2_id, message_id=b.message_id)
                    await bot.send_message(chat_id=gam.player1_id,
                                           text=f"*Вопрос:*\n\n{cap.caption}\n*Ответ партнёра:*\n\n{gam.vop2}",
                                           parse_mode=ParseMode.MARKDOWN, reply_markup=kl)

                    await bot.send_message(chat_id=gam.player2_id,
                                           text=f"*Вопрос:*\n\n{cap.caption}\n*Ответ партнёра:*\n\n{gam.vop1}",
                                           parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                    gam.play_now = 0
                    session.add(part)
                    session.add(user)
                    session.commit()
                else:
                    await bot.send_message(chat_id=tg_id, text='Теперь ждём ответ на вопрос от твоего партнёра...',
                                           reply_markup=ReplyKeyboardRemove())
                session.add(gam)
                session.commit()
        else:
            gam.vop1 = tex
            gam.play_now = gam.play_now + 1
            if gam.play_now == gam.players:
                part = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                part.state = ''
                cap = session.query(Paid_game_info_1).filter(Paid_game_info_1.id == gam.game_id_id).first()
                kl = InlineKeyboardMarkup(row_width=2).add(
                    InlineKeyboardButton('Верно ✅', callback_data=f'answ_{gam.id}_y'),
                    InlineKeyboardButton('Не правильно ❌', callback_data=f'answ_{gam.id}_n'))
                a = await bot.send_message(chat_id=gam.player1_id, text='Загрузка...',
                                           reply_markup=ReplyKeyboardRemove())
                b = await bot.send_message(chat_id=gam.player2_id, reply_markup=ReplyKeyboardRemove(),
                                           text='Загрузка...')
                await bot.delete_message(chat_id=gam.player1_id, message_id=a.message_id)
                await bot.delete_message(chat_id=gam.player2_id, message_id=b.message_id)
                await bot.send_message(chat_id=gam.player1_id,
                                       text=f"*Вопрос:*\n\n{cap.caption}\n*Ответ партнёра:*\n\n{gam.vop2}",
                                       parse_mode=ParseMode.MARKDOWN, reply_markup=kl)

                await bot.send_message(chat_id=gam.player2_id,
                                       text=f"*Вопрос:*\n\n{cap.caption}\n*Ответ партнёра:*\n\n{gam.vop1}",
                                       parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                gam.play_now = 0
                session.add(part)
                session.add(user)
                session.commit()
            else:
                await bot.send_message(chat_id=tg_id, text='Теперь ждём ответ на вопрос от твоего партнёра...',
                                       reply_markup=ReplyKeyboardRemove())
            session.add(gam)
            session.commit()
        session.add(user)
        session.commit()
    elif user.state == 'privet1':
        user.state = 'privet2'
        await bot.send_message(chat_id=tg_id,
                               text='Я – собрание горячих поз и эротических заданий, благодаря которым ты и твой партнер сможете открыть для себя новые грани в сексе и лучше узнать друг друга как в постели, так и в жизни.'
                               , reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                KeyboardButton("Кто тебя создал? 🤔")))
    elif user.state == 'privet2':
        user.state = 'privet3'
        await bot.send_message(chat_id=tg_id,
                               text='Меня создала команда молодых ребят – с целью помочь людям в деле, о котором, как правило, «не принято» говорить открыто.\n\nВсе из разных городов, с разным опытом и предпочтениями в сексе – именно поэтому во мне так много всего.',
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                   KeyboardButton("Расскажи об интерактиве 🎲")))
    elif user.state == 'privet3':
        user.state = 'privet4'
        await bot.send_message(chat_id=tg_id,
                               text="Если ты и твой партнер устали от классических поз, вроде наездницы или догги-стайл, то я могу показать вам несколько новых для разнообразия.\n\nНо помимо поз, у меня есть и задания на разную тематику. Хотите чего-то романтичного? Тогда попробуйте устроить партнеру нежный массаж плеч. Хочется пожестче? Вам в БДСМ-секцию. Заданий предостаточно.",
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                   KeyboardButton("Покажи пример 🔍")))
    elif user.state == 'privet4':
        user.state = 'privet5'
        poz = session.query(Poses).filter(Poses.pos_id == 2).first()
        f = int(poz.pos_lvl) * '⭐️'
        await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                             caption=f'*{poz.name}*{poz.caption}*Сложность:* {f}',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                 KeyboardButton("Звучит интересно")),
                             parse_mode=ParseMode.MARKDOWN)
    elif user.state == 'privet5':
        user.state = 'privet6'
        await bot.send_message(chat_id=tg_id,
                               text="Чудно! Теперь давай я тебе объясню как тут все устроено.\n\nСкорее всего ты обо меня узнал через qr-код, который был вместе с твоей новой игрушкой. Кстати, если вдруг возникли какие-то вопросы, то не стесняйся и напиши ребятам в магазин. Тебе обязательно помогут.\n\nСмотри, если ты купил игрушку, то у тебя есть номер заказа. Напиши его мне и я зачислю на твой баланс коины в размере 10% от суммы заказа.\n\nУ тебя есть номер заказа?",
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Да"),
                                                                                          KeyboardButton("Нет")))
    elif user.state == 'privet6':
        if tex == 'Да':
            user.state = 'write_id_'
            await bot.send_message(chat_id=tg_id, text="Тогда впиши его сюда и продолжим!",
                                   reply_markup=ReplyKeyboardRemove())
        else:
            user.state = 'privet7'
            await bot.send_message(chat_id=tg_id,
                                   text="Вау. Интересно узнать как ты обо мне узнал :)\nНу, ладно. Как-нибудь в другой раз поговорим об этом, а пока могу тебе предложить промокод на скидку в магазине, чтобы ты попробовал для себя что-то новенькое.\n```OCBCE-HELLO100```",
                                   reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add('Поехали дальше 🔜'),
                                   parse_mode=ParseMode.MARKDOWN)
            await bot.send_message(chat_id=tg_id, text="Лови ссылку на магазин\n\nhttps://kazanexpress.ru/amateur")
    elif user.state == 'write_id_':
        ans = True
        user.state = "privet7"
        for i in tex:
            if i not in "0123456789":
                ans = False
                break
        if ans:
            f = get_coins_from_order(tex, tg_id)
            await bot.send_message(tg_id,
                                   text=f"{f}\n\nЕсли произошла какая-то ошибка, то можно ввести id заказа после приветсвия или обратиться в поддержку @Amateur_help",
                                   reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                       KeyboardButton("Попробовать ещё раз 🔄"),
                                       KeyboardButton("Поехали дальше 🔜")))
        else:
            await bot.send_message(tg_id,
                                   text='В ID заказа должны присутствовать только цифры\n\nMожно ввести id заказа после приветсвия',
                                   reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                       KeyboardButton("Попробовать ещё раз 🔄"),
                                       KeyboardButton("Поехали дальше 🔜")))
        session.add(user)
        session.commit()
    elif user.state == 'privet7':
        if tex != 'Попробовать ещё раз 🔄':
            user.state = "privet8"
            await bot.send_message(chat_id=tg_id,
                                   text="Команда приготовила для тебя статью, где ты можешь ознакомиться с моим функционалом. Читается быстро и просто. Намекни, как прочитаешь :)",
                                   reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add("Готово!"))
            await bot.send_message(chat_id=tg_id, text='https://telegra.ph/AmateurBot-09-03')
        else:
            user.state = 'write_id_'
            await bot.send_message(chat_id=tg_id, text="Впишите id заказа",
                                   reply_markup=ReplyKeyboardRemove())
    elif user.state == 'privet8':
        await bot.send_message(chat_id=tg_id, text="Тогда стартуем! Уверен, что будет жарко")
        user.state = 'write_pol'
        await bot.send_message(tg_id, 'Добро пожаловать в AmateurBot 👋\nВыберите свой пол 🚻',
                               reply_markup=reg_kl)
    else:
        if user.user_tg_id != 415984908:
            await bot.delete_message(chat_id=tg_id, message_id=message.message_id)
        else:
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton('Нажмите для рассылки', callback_data='ras_yes'))
            await bot.send_message(chat_id=415984908, text=tex,
                                   reply_markup=kl)
    session.commit()
    session.close()


@dp.callback_query_handler()
async def process_withdraw_request(callback_query: types.CallbackQuery):
    session = create_session()
    tg_id = callback_query.message.chat.id
    user = session.query(User).filter(User.user_tg_id == tg_id).first()
    if user is None:
        await bot.send_message(chat_id=tg_id,
                               text='Привет! Я – AmateurBot, первый секс-бот в рунете, и мне очень приятно, что ты решил поинтересоваться мной!',
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                   KeyboardButton("Расскажи о себе:")))
        new_user = User()
        new_user.user_tg_id = tg_id
        new_user.state = 'privet1'
        new_user.balance = 500
        new_user.pol = "None"
        new_user.podpiska = "False"
        new_user.zar_today = 0
        new_user.zar_mesyaz = 0
        new_user.count_day_every_day = 0
        session.add(new_user)
        session.commit()
    else:
        if callback_query.data == 'home':
            user.state = ''
            texx = f"Добро пожаловать! 👋\n\nЭто бот предназначенный для улучшения интимных связей\nСейчас на вашем балансе {user.balance} sex-coins 💸\n\nСегодня вы ещё можете заработать {min(200 - user.zar_today, 2400 - user.zar_mesyaz)} 💵\nВ этом месяце ещё {2400 - user.zar_mesyaz} 💰"
            # kl = InlineKeyboardMarkup()
            if user.pol == 'man':
                main_kl_man = InlineKeyboardMarkup()
                main_kl_man.add(InlineKeyboardButton("Мой профиль 👨", callback_data='my_profile'))
                main_kl_man.add(InlineKeyboardButton('Получить ежедневную награду 🎁', callback_data='every_day'))
                main_kl_man.add(InlineKeyboardButton('Игры ♥️', callback_data='game'))
                main_kl_man.add(InlineKeyboardButton('Позы 🧘‍♀️', callback_data='poses'))
                main_kl_man.add(InlineKeyboardButton('Промокоды 💯', callback_data='spromo'))
                main_kl_man.add(InlineKeyboardButton('Магазин 🛒', callback_data='store'))
                main_kl_man.add(InlineKeyboardButton('Ввести id заказа 🆔', callback_data='zak_id'))
                main_kl_man.add(InlineKeyboardButton('О sex-coin 📖', url='https://telegra.ph/O-sex-coins-09-07'))
                main_kl_man.add(InlineKeyboardButton('Помощь 🆘', url='https://t.me/amateur_help'))
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text=texx,
                                            reply_markup=main_kl_man)
            else:
                main_kl_woman = InlineKeyboardMarkup()
                main_kl_woman.add(InlineKeyboardButton("Мой профиль 👩", callback_data='my_profile'))
                main_kl_woman.add(InlineKeyboardButton('Получить ежедневную награду 🎁', callback_data='every_day'))
                main_kl_woman.add(InlineKeyboardButton('Игры ♥️', callback_data='game'))
                main_kl_woman.add(InlineKeyboardButton('Позы 🧘‍♀️', callback_data='poses'))
                main_kl_woman.add(InlineKeyboardButton('Промокоды 💯', callback_data='spromo'))
                main_kl_woman.add(InlineKeyboardButton('Магазин 🛒', callback_data='store'))
                main_kl_woman.add(InlineKeyboardButton('Ввести id заказа 🆔', callback_data='zak_id'))
                main_kl_woman.add(InlineKeyboardButton('О sex-coin 📖', url='https://telegra.ph/O-sex-coins-09-07'))
                main_kl_woman.add(InlineKeyboardButton('Помощь 🆘', url='https://t.me/amateur_help'))
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text=texx,
                                            reply_markup=main_kl_woman)
        elif callback_query.data == 'home_':
            a = await bot.send_message(chat_id=tg_id, reply_markup=types.ReplyKeyboardRemove(),
                                       text='Подключаемся к базе данных...')
            user.state = ''
            kl = InlineKeyboardMarkup()
            if user.pol == 'man':
                kl.add(InlineKeyboardButton("Мой профиль 👨", callback_data='my_profile'))
            else:
                kl.add(InlineKeyboardButton("Мой профиль 👩", callback_data='my_profile'))
            kl.add(InlineKeyboardButton('Получить ежедневную награду 🎁', callback_data='every_day'))
            kl.add(InlineKeyboardButton('Игры ♥️', callback_data='game'))
            kl.add(InlineKeyboardButton('Позы 🧘‍♀️', callback_data='poses'))
            kl.add(InlineKeyboardButton('Промокоды 💯', callback_data='spromo'))
            kl.add(InlineKeyboardButton('Магазин 🛒', callback_data='store'))
            kl.add(InlineKeyboardButton('Ввести id заказа 🆔', callback_data='zak_id'))
            kl.add(InlineKeyboardButton('О sex-coin 📖', url='https://telegra.ph/O-sex-coins-09-07'))
            kl.add(InlineKeyboardButton('Помощь 🆘', url='https://t.me/amateur_help'))
            await bot.send_message(chat_id=tg_id,
                                   text=f"Добро пожаловать! 👋\n\nЭто бот предназначенный для улучшения интимных связей\nСейчас на вашем балансе {user.balance} sex-coins 💸\n\nСегодня вы ещё можете заработать {min(200 - user.zar_today, 2400 - user.zar_mesyaz)} 💵\nВ этом месяце ещё {2400 - user.zar_mesyaz} 💰",
                                   reply_markup=kl)
            await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
            await asyncio.sleep(0.8)
            await bot.delete_message(chat_id=tg_id, message_id=a.message_id)
        elif callback_query.data == 'every_day':
            ans = take_reward(tg_id)
            mas = ["*1-ый день:* 5 коинов",
                   "*2-ой день:* 10 коинов",
                   "*3-ий день:* раскрывается случайная поза (если позы открыты, то 20 коинов)",
                   "*4-ый день:* 40 коинов",
                   "*5-ый день:* Промокод на 100 рублей",
                   "*6-ой день:* Промокод на 100 рублей + 25 коинов",
                   "*7-ой день:* Колоду с позами"]
            mas[(max(user.count_day_every_day - 1, 0)) % 7] += ' `Вы здесь` 👈'
            texx = "*Заходите в бота каждый день и получайте подарки*\n\n"
            for i in range(6):
                texx += mas[i] + '\n\n'
            texx += mas[-1]
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id, text=texx,
                                        parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            if ans != 'Вы уже получили приз за сегодня 😔':
                a = await bot.send_message(chat_id=tg_id, text=ans)
                await asyncio.sleep(1.2)
                await bot.delete_message(chat_id=tg_id, message_id=a.message_id)
        elif callback_query.data == 'my_collection':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton("Мои игры 🕹", callback_data='smy_game'))

            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Выберите то, что вы хотите посмотреть 🔭',
                                        reply_markup=kl)
        elif callback_query.data == 'my_pose':
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton(
                f'1-ый уровень ({len(session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(Open_poses.pos_level == 1).all())} штук)',
                callback_data='open_pose_1'))
            kl.add(InlineKeyboardButton(
                f'2-ой уровень ({len(session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(Open_poses.pos_level == 2).all())} штук)',
                callback_data='open_pose_2'))
            kl.add(InlineKeyboardButton(
                f'3-ий уровень ({len(session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(Open_poses.pos_level == 3).all())} штук)',
                callback_data='open_pose_3'))
            kl.add((InlineKeyboardButton(
                f'Все уровни ({len(session.query(Open_poses).filter(Open_poses.user_id == tg_id).all())} штук)',
                callback_data='open_pose_4')))
            kl.add(InlineKeyboardButton("Назад 🔙", callback_data='poses'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Выберите уровень поз 💪',
                                        reply_markup=kl)
        elif callback_query.data[0:len('open_pose_')] == 'open_pose_':
            pos_lvl = int(callback_query.data.split('_')[2])

            poz_all = -1
            if pos_lvl != 4:
                pos_all = session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(
                    Open_poses.pos_level == pos_lvl).all()
            else:
                pos_all = session.query(Open_poses).filter(Open_poses.user_id == tg_id).all()
            kl = InlineKeyboardMarkup(row_width=2)
            count = 1
            for elem in pos_all:
                if len(pos_all) == 100:
                    if count <= 2:
                        pass
                    else:
                        if elem.see == "True":
                            kl.add(
                                InlineKeyboardButton(f"{elem.name} 🟢",
                                                     callback_data=f'pose_{pos_lvl}_{elem.pos_id}_{count}_1'))
                        else:
                            kl.add(
                                InlineKeyboardButton(f"{elem.name} 🔘",
                                                     callback_data=f'pose_{pos_lvl}_{elem.pos_id}_{count}_1'))
                else:
                    if elem.see == "True":
                        kl.add(
                            InlineKeyboardButton(f"{elem.name} 🟢",
                                                 callback_data=f'pose_{pos_lvl}_{elem.pos_id}_{count}_1'))
                    else:
                        kl.add(
                            InlineKeyboardButton(f"{elem.name} 🔘",
                                                 callback_data=f'pose_{pos_lvl}_{elem.pos_id}_{count}_1'))
                count += 1

            kl.add(InlineKeyboardButton("Назад 🔙", callback_data='my_pose'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            if len(callback_query.data.split('_')) == 4:
                await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                await bot.send_message(chat_id=tg_id,
                                       text='Нажимайте на название поз\n🔘 - вы ещё не видели\n🟢 - уже как то смотрели',
                                       reply_markup=kl)
            else:
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text='Нажимайте на название поз\n🔘 - вы ещё не видели\n🟢 - уже как то смотрели',
                                            reply_markup=kl)
        elif callback_query.data[0:len('pose_')] == 'pose_':
            pos_lvl = int(callback_query.data.split('_')[1])
            pos_id = int(callback_query.data.split('_')[2])
            ch = int(callback_query.data.split('_')[3])
            d = int(callback_query.data.split('_')[4])
            if pos_id == -1:
                await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                text=f"Вы уже долистали до конца 😔",
                                                show_alert=True)
            else:
                await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                poz = session.query(Poses).filter(Poses.pos_id == pos_id).first()
                kl = InlineKeyboardMarkup(row_width=2)
                naz = -1
                if ch == 1:
                    naz = InlineKeyboardButton("Предыдущая ⬅️", callback_data=f'pose_-1_-1_-1_-1')
                poz_all = -1
                if pos_lvl != 4:
                    pos_all = session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(
                        Open_poses.pos_level == pos_lvl).all()
                else:
                    pos_all = session.query(Open_poses).filter(Open_poses.user_id == tg_id).all()
                vp = -1
                if ch == len(pos_all):
                    vp = InlineKeyboardButton("Следущая ➡️", callback_data=f'pose_-1_-1_-1_-1')
                count = 1
                if naz == -1 or vp == -1:
                    for elem in pos_all:
                        if ch - 1 == count:
                            naz = InlineKeyboardButton("Предыдущая ⬅️",
                                                       callback_data=f'pose_{pos_lvl}_{elem.pos_id}_{count}_{0}')
                        if ch + 1 == count:
                            vp = InlineKeyboardButton("Следущая ➡️",
                                                      callback_data=f'pose_{pos_lvl}_{elem.pos_id}_{count}_{0}')
                        count += 1
                kl.add(naz, vp)
                kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'open_pose_{pos_lvl}_1'),
                       InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                f = '⭐️' * int(poz.pos_lvl)
                cur = session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(
                    Open_poses.pos_level == poz.pos_lvl).filter(Open_poses.pos_id == poz.pos_id).first()
                cur.see = "True"
                session.add(cur)
                session.commit()
                await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                                     caption=f'*{poz.name}*{poz.caption}*Сложность:* {f}', reply_markup=kl,
                                     parse_mode=ParseMode.MARKDOWN)
        elif callback_query.data == 'game':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton('Платные игры 🔒', callback_data='paid_game'))
            kl.add(InlineKeyboardButton('Бесплатные игры 🆓', callback_data='free_game'))
            kl.add(InlineKeyboardButton('Купленные игры 🔐', callback_data='my_game'))
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Выберите тип игры 🎯', reply_markup=kl)
        elif callback_query.data == 'paid_game':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton('Чуства', callback_data='wpaid_game_1_a'))
            kl.add(InlineKeyboardButton('Страсть', callback_data='wpaid_game_2_a'))
            kl.add(InlineKeyboardButton('Все категории', callback_data='wpaid_game_4_a'))
            kl.add(InlineKeyboardButton('Назад 🔙', callback_data='game'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Нажмите на понравившуюся игру и посмотрите описание 👀', reply_markup=kl)
        elif callback_query.data[0:len('wpaid_game_')] == 'wpaid_game_':
            t = int(callback_query.data.split('_')[2])
            b = callback_query.data.split('_')[3]
            kl = InlineKeyboardMarkup()
            c = 0
            if t == 1:

                if b != 'b' or session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).filter(
                        Purchased_game.game_id == 5).first() != None:
                    c += 1
                    kl.add(
                        InlineKeyboardButton('Романтика утром, а страсть вечером', callback_data=f'paid_game_5_1_{b}'))
                if b != 'b' or session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).filter(
                        Purchased_game.game_id == 6).first() != None:
                    c += 1
                    kl.add(InlineKeyboardButton('Я жду тебя вечером', callback_data=f'paid_game_6_1_{b}'))
            elif t == 2:
                if b != 'b' or session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).filter(
                        Purchased_game.game_id == 3).first() != None:
                    c += 1
                    kl.add(InlineKeyboardButton('Давай попробуем это', callback_data=f'paid_game_3_2_{b}'))
                if b != 'b' or session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).filter(
                        Purchased_game.game_id == 4).first() != None:
                    c += 1
                    kl.add(InlineKeyboardButton('Честность и страсть', callback_data=f'paid_game_4_2_{b}'))

                if b != 'b' or session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).filter(
                        Purchased_game.game_id == 8).first() != None:
                    c += 1
                    kl.add(InlineKeyboardButton('Кто первый', callback_data=f'paid_game_8_2_{b}'))
                if b != 'b' or session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).filter(
                        Purchased_game.game_id == 9).first() != None:
                    c += 1
                    kl.add(InlineKeyboardButton('А теперь ложись вот так… ', callback_data=f'paid_game_9_2_{b}'))
                if b != 'b' or session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).filter(
                        Purchased_game.game_id == 10).first() != None:
                    c += 1
                    kl.add(InlineKeyboardButton('Господин и госпожа', callback_data=f'paid_game_10_2_{b}'))
                if b != 'b' or session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).filter(
                        Purchased_game.game_id == 11).first() != None:
                    c += 1
                    kl.add(InlineKeyboardButton('Эксперименты', callback_data=f'paid_game_11_2_{b}'))
            elif t == 3:
                pass
            else:
                if b == 'b':
                    game_list = session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).all()
                else:
                    game_list = session.query(Paid_game).all()
                for elem in game_list:
                    elem = session.query(Paid_game).filter(Paid_game.game_id == elem.game_id).first()
                    if elem.game_id not in [1, 2, 7]:
                        kl.add(InlineKeyboardButton(elem.game_name, callback_data=f'paid_game_{elem.game_id}_4_{b}'))
                        c += 1
            if c != 0:
                if b != 'b':
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='paid_game'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                else:
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='my_game'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text='Нажмите на понравившуюся игру и посмотрите описание 👀',
                                            reply_markup=kl)
            else:
                await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                text=f"К сожалению у вас нету игр в данной категории 😔",
                                                show_alert=True)
        elif callback_query.data == '_paid_game':
            kl = InlineKeyboardMarkup()
            game_list = session.query(Paid_game).all()
            for elem in game_list:
                kl.add(InlineKeyboardButton(elem.game_name, callback_data=f'paid_game_{elem.game_id}_0_s'))
            # kl.add()
            kl.add(InlineKeyboardButton('Назад 🔙', callback_data='store'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Нажмите на понравившуюся игру и посмотрите описание 👀', reply_markup=kl)
        elif callback_query.data[0:len('paid_game_')] == 'paid_game_':
            paid_game_id = int(callback_query.data.split('_')[2])
            paid_game = session.query(Paid_game).filter(Paid_game.game_id == paid_game_id).first()
            buy = False

            if session.query(Purchased_game).filter(Purchased_game.game_id == paid_game_id).filter(
                    Purchased_game.user_id == tg_id).first() != None:
                buy = True
            kl = InlineKeyboardMarkup(row_width=2)
            b = callback_query.data.split('_')[4]
            t = callback_query.data.split('_')[3]
            if buy:
                kl.add(InlineKeyboardButton('Подробнее 🧐', url=str(paid_game.detail)),
                       InlineKeyboardButton('Играть 🚀', callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}'))
            else:
                kl.add(InlineKeyboardButton('Подробнее 🧐', url=str(paid_game.detail)),
                       InlineKeyboardButton('Купить (100 sex-coin)',
                                            callback_data=f'buy_paid_game_{paid_game_id}_{t}_{b}'))
            if len(callback_query.data.split('_')) == 5:
                t = callback_query.data.split('_')[3]
                if callback_query.data.split('_')[4] == 'b':
                    kl.add(InlineKeyboardButton('Назад 🔙',
                                                callback_data=f'wpaid_game_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                elif callback_query.data.split('_')[4] == 'w':
                    kl.add(InlineKeyboardButton('Назад 🔙',
                                                callback_data='_paid_game'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                else:
                    kl.add(InlineKeyboardButton('Назад 🔙',
                                                callback_data=f'wpaid_game_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            else:
                kl.add(InlineKeyboardButton('Назад 🔙', callback_data='paid_game'),
                       InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text=f'*{beatufull_str(paid_game.game_name)}*\n\n{paid_game.game_caption}',
                                        parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
        elif callback_query.data[0:len('spaid_game_')] == 'spaid_game_':
            paid_game_id = callback_query.data.split('_')[2]
            paid_game_id = int(paid_game_id)
            paid_game = session.query(Paid_game).filter(Paid_game.game_id == paid_game_id).first()
            buy = False
            if session.query(Purchased_game).filter(Purchased_game.game_id == paid_game_id).filter(
                    Purchased_game.user_id == tg_id).first() != None:
                buy = True
            kl = InlineKeyboardMarkup(row_width=2)
            b = callback_query.data.split('_')[4]
            t = callback_query.data.split('_')[3]
            if buy:
                kl.add(InlineKeyboardButton('Подробнее 🧐', url=str(paid_game.detail)),
                       InlineKeyboardButton('Играть 🚀', callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}'))
            else:
                kl.add(InlineKeyboardButton('Подробнее 🧐', url=str(paid_game.detail)),
                       InlineKeyboardButton('Купить (100 sex-coin)',
                                            callback_data=f'buy_paid_game_{paid_game_id}_{t}_{b}'))
            kl.add(InlineKeyboardButton('Назад 🔙', callback_data='my_game'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text=f'*{beatufull_str(paid_game.game_name)}*\n\n{paid_game.game_caption}',
                                        parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
        elif callback_query.data[0:len('buy_paid_game_')] == 'buy_paid_game_':
            if user.balance >= 100:
                paid_game_id = int(callback_query.data.split('_')[3])
                new_paid_game = Purchased_game()
                new_paid_game.game_id = paid_game_id
                new_paid_game.user_id = int(user.user_tg_id)
                # new_paid_game.id = 456
                user.balance = user.balance - 100
                session.add(new_paid_game)
                session.add(user)
                session.commit()
                paid_game = session.query(Paid_game).filter(Paid_game.game_id == paid_game_id).first()
                await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                text=f"Поздравляем! 🥳\nИгра {beatufull_str(paid_game.game_name)} теперь ваша 😍",
                                                show_alert=True)
                buy = True
                b = callback_query.data.split('_')[5]
                t = callback_query.data.split('_')[4]
                kl = InlineKeyboardMarkup(row_width=2)
                if buy:
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'wpaid_game_{t}_{b}'),
                           InlineKeyboardButton('Играть 🚀', callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}'))
                else:
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='paid_game'),
                           InlineKeyboardButton('Купить (100 sex-coin)', callback_data=f'buy_paid_game_{paid_game_id}'))
                if paid_game_id == 6:
                    for i in range(20):
                        ne = For_paid_game_info_6()
                        ne.name = session.query(Paid_game_info_6).filter(Paid_game_info_6.id == i + 1).first().dop_info
                        ne.user_tg_id = tg_id
                        ne.id_from_game = 6
                        ne.do = "No"
                        ne.id_from_game = 6
                        session.add(ne)
                        session.commit()
                kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text=f'*{beatufull_str(paid_game.game_name)}*\n\n{paid_game.game_caption}',
                                            parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            else:
                await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                text='К сожалению у вас недостаточно sex-coin 😫',
                                                show_alert=True)
        elif callback_query.data[0:len('break_2_')] == 'break_2_':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton('К играм 🎮', callback_data='game'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            gam = session.query(For_paid_game_info_2).filter(
                For_paid_game_info_2.id == int(callback_query.data.split('_')[2])).first()
            await bot.delete_message(message_id=callback_query.message.message_id, chat_id=tg_id)
            await bot.send_message(chat_id=gam.player1_id,
                                   text='Игра *Говори или подчиняйся* завершена, очки за игру были начислены на ваш баланс\n\nНажмите /start что бы попасть в главное меню',
                                   parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            await bot.send_message(chat_id=gam.player2_id,
                                   text='Игра *Говори или подчиняйся* завершена, очки за игру были начислены на ваш баланс\n\nНажмите /start что бы попасть в главное меню',
                                   parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            await up_balance(gam.player1_id, gam.player1_count)
            await up_balance(gam.player2_id, gam.player2_count)
            gam.play = 0
            session.add(gam)
            session.commit()
        elif callback_query.data[0:len('play_paid_game_')] == 'play_paid_game_':
            paid_game_id = int(callback_query.data.split('_')[3])
            if paid_game_id == 1:
                if len(callback_query.data.split('_')) == 6:
                    # 1 играет 1, 2 играют вдвоём
                    kl = InlineKeyboardMarkup(row_width=2)
                    kl.add(InlineKeyboardButton('С одного 1️⃣', callback_data=f'play_paid_game_{paid_game_id}_1'),
                           InlineKeyboardButton('С двух 2️⃣', callback_data=f'play_paid_game_{paid_game_id}_2'))
                    b = callback_query.data.split('_')[5]
                    t = callback_query.data.split('_')[4]
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game_{paid_game_id + 100}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(
                        chat_id=tg_id, message_id=callback_query.message.message_id,
                        text="Выберите как вы хотите играть, с одного телефона или с партнёром с двух 📲",
                        reply_markup=kl)
                else:
                    count_play = int(callback_query.data.split('_')[4])
                    if count_play == 2:
                        partner_phone_number = user.partner_phone_number
                        partner = session.query(User).filter(User.partner_phone_number == user.phone_number).filter(
                            User.phone_number == partner_phone_number).first()
                        if partner is None:
                            await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                            text="К сожалению мы не можем найти вашего партнёра 😔\nПопробуйте написать в поддержку, мы вам поможем",
                                                            show_alert=True)
                        else:
                            user.state = 'write_wish'
                            partner.state = 'write_wish'
                            al = session.query(For_paid_game_info_1).all()
                            for elem in al:
                                if elem.player1_id == tg_id or elem.player2_id == tg_id:
                                    elem.play = 0
                                    session.add(elem)
                                    session.commit()
                            new = For_paid_game_info_1()
                            new.game_id = 1
                            new.players = 2
                            new.player1_id = user.user_tg_id
                            new.player2_id = partner.user_tg_id
                            new.player1_count = 0
                            new.player2_count = 0
                            new.play_now = 0
                            new.play = 1
                            session.add(new)
                            session.add(partner)
                            session.add(user)
                            session.commit()
                            await bot.send_message(chat_id=partner.user_tg_id,
                                                   text="Ваш партнёр позвал вас играть в *А ты знаешь, что*\nНапишите своё желание, в случае вашей победы, мы отправим его партнёру",
                                                   parse_mode=ParseMode.MARKDOWN)
                            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                        text="Игра: *А ты знаешь, что* началась\nДля начала напиши своё желание, в случае вашей победы, мы отправим его твоему партнёру",
                                                        parse_mode=ParseMode.MARKDOWN)
                    elif count_play == 1:
                        await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=tg_id,
                                                    text="Напишите свои желания на листочке, после окончания игры проигравшему достанется желание партнёра 📝")
                        al = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.play == 1).all()
                        for elem in al:
                            if elem.player1_id == tg_id or elem.player2_id == tg_id:
                                elem.play = 0
                                session.add(elem)
                                session.commit()
                        new = For_paid_game_info_1()
                        new.game_id = 1
                        new.players = 1
                        new.player1_id = user.user_tg_id
                        new.player1_count = 0
                        new.player2_count = 0
                        new.play = 1
                        progress = session.query(Progress).filter(Progress.user_tg_id == int(tg_id)).filter(
                            Progress.gam_id == 1).first()
                        if progress is None:
                            new1 = Progress()
                            new1.gam_id = 1
                            new1.user_tg_id = int(tg_id)
                            new1.lvl = 1
                            session.add(new1)
                            session.commit()
                            ch = 1
                        else:
                            ch = (progress.lvl) % 50 + 1
                            progress.lvl = progress.lvl + 1
                        session.add(progress)
                        session.add(new)
                        session.commit()
                        vop = session.query(Paid_game_info_1).filter(Paid_game_info_1.id == ch).first()
                        kl = InlineKeyboardMarkup(row_width=2)
                        kl.add(InlineKeyboardButton(f'Только {user.name}', callback_data='pl_1'),
                               InlineKeyboardButton(f'Только {user.partner_name}', callback_data='pl_2'))
                        kl.add(InlineKeyboardButton('Оба правы 😎', callback_data='pl_3'),
                               InlineKeyboardButton("Оба ошиблись  🙊", callback_data='pl_4'))
                        await bot.send_message(chat_id=tg_id,
                                               text=f"Ответьте друг другу на вопрос и отметьте кто из вас прав ✅\n\n{vop.caption}",
                                               reply_markup=kl)
            elif paid_game_id == 2:
                f = 0
                if len(callback_query.data.split('_')) == 6:
                    partner = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                    if partner is None or user.partner_phone_number is None or partner.partner_phone_number != user.phone_number:
                        await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                        text="К сожалению мы не можем найти вашего партнёра 😔\nПопробуйте написать в поддержку, мы вам поможем",
                                                        show_alert=True)
                    else:
                        finish_all_game(tg_id)
                        finish_all_game(partner.user_tg_id)
                        kl = InlineKeyboardMarkup(row_width=2)
                        kl.add(InlineKeyboardButton(f'{beatufull_str(user.name)}', callback_data='play_paid_game_2_1'),
                               InlineKeyboardButton(f'{beatufull_str(user.partner_name)}',
                                                    callback_data='play_paid_game_2_2'))
                        t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                        kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_2_{t}_{b}'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text="Выберите кто из вас начнёт игру 🎯", reply_markup=kl)
                elif len(callback_query.data.split('_')) == 5:
                    partner = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                    if partner is not None:
                        await bot.edit_message_text(text="Игра *Говори или подчиняйся* началась",
                                                    message_id=callback_query.message.message_id, chat_id=tg_id,
                                                    parse_mode=ParseMode.MARKDOWN)
                        n = For_paid_game_info_2()
                        n.play = 1
                        n.player1_id = tg_id
                        n.player2_id = partner.user_tg_id
                        n.game_id = 2
                        n.player1_count = 0
                        n.player2_count = 0
                        c = int(callback_query.data.split('_')[4])
                        n.hwo_last = c
                        session.add(n)
                        session.commit()
                        gam = session.query(For_paid_game_info_2).filter(For_paid_game_info_2.play == 1).filter(
                            For_paid_game_info_2.player1_id == tg_id).filter(
                            For_paid_game_info_2.player2_id == partner.user_tg_id).filter(
                            For_paid_game_info_2.hwo_last == c).first()
                        if c == 1:
                            kl = InlineKeyboardMarkup(row_width=2)
                            kl.add(InlineKeyboardButton("Отвечай 🤓", callback_data='play_paid_game_2_2_1_0'),
                                   InlineKeyboardButton("Выполняй 💪", callback_data='play_paid_game_2_2_2_0'))
                            kl.add(InlineKeyboardButton('Закончить игру ❌', callback_data=f"break_2_{gam.id}"))
                            await bot.send_message(chat_id=tg_id,
                                                   text="Игра *Говори или подчиняйся*\n\nСейчас ваш ход вам нужно выбрать то, что вы будете делать",
                                                   reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                        elif c == 2:
                            kl = InlineKeyboardMarkup(row_width=2)
                            kl.add(InlineKeyboardButton("Отвечай 🤓", callback_data='play_paid_game_2_1_1_0'),
                                   InlineKeyboardButton("Выполняй 💪", callback_data='play_paid_game_2_1_2_0'))
                            kl.add(InlineKeyboardButton('Закончить игру ❌', callback_data=f"break_2_{gam.id}"))
                            await bot.send_message(chat_id=partner.user_tg_id,
                                                   text="Игра *Говори или подчиняйся*\n\nСейчас ваш ход вам нужно выбрать то, что вы будете делать",
                                                   reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                elif len(callback_query.data.split('_')) == 7:
                    partner = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                    c = int(callback_query.data.split('_')[4])
                    d = int(callback_query.data.split('_')[5])
                    await bot.edit_message_text(chat_id=tg_id, text='Вашему партнёру пришло задание',
                                                message_id=callback_query.message.message_id)
                    ch = -1
                    gam = session.query(For_paid_game_info_2).filter(For_paid_game_info_2.play == 1).filter(
                        For_paid_game_info_2.player1_id == tg_id).filter(
                        For_paid_game_info_2.player2_id == partner.user_tg_id).first()
                    if gam is None:
                        gam = session.query(For_paid_game_info_2).filter(For_paid_game_info_2.play == 1).filter(
                            For_paid_game_info_2.player2_id == tg_id).filter(
                            For_paid_game_info_2.player1_id == partner.user_tg_id).first()
                        gam.player2_count += 3
                    else:
                        gam.player1_count += 3
                    if d == 1:
                        progress = session.query(Progress).filter(
                            Progress.user_tg_id == int(partner.user_tg_id)).filter(
                            Progress.gam_id == 2).filter(Progress.dop_info == 'Вопросы').first()
                        if progress is None:
                            ch = 1
                            new = Progress()
                            new.lvl = 1
                            new.gam_id = 2
                            new.user_tg_id = partner.user_tg_id
                            new.dop_info = 'Вопросы'
                            session.add(new)
                            session.commit()
                        else:
                            ch = progress.lvl % 25 + 1
                            progress.lvl = progress.lvl + 1
                            session.add(progress)
                            session.commit()
                    else:
                        progress = session.query(Progress).filter(
                            Progress.user_tg_id == int(partner.user_tg_id)).filter(
                            Progress.gam_id == 2).filter(Progress.dop_info == 'Действия').first()
                        if progress is None:
                            ch = 26
                            new = Progress()
                            new.lvl = 26
                            new.gam_id = 2
                            new.dop_info = 'Действия'
                            new.user_tg_id = partner.user_tg_id
                            session.add(new)
                            session.commit()
                        else:
                            if progress.lvl == 50:
                                progress.lvl = 25
                            progress.lvl += 1
                            ch = progress.lvl
                            session.add(progress)
                            session.commit()
                    kl = InlineKeyboardMarkup(row_width=2)
                    kl.add(InlineKeyboardButton("Отвечай 🤓", callback_data='play_paid_game_2_2_1_0'),
                           InlineKeyboardButton("Выполняй 💪", callback_data='play_paid_game_2_2_2_0'))
                    kl.add(InlineKeyboardButton('Закончить игру ❌', callback_data=f"break_2_{gam.id}"))
                    game = session.query(Paid_game_info_2).filter(Paid_game_info_2.id == ch).first()
                    await bot.send_message(chat_id=partner.user_tg_id,
                                           text=f'*{game.dop_info}*\n\n{game.caption}\n\nВыберите что будет делать ваш партнёр или закончите игру',
                                           parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            elif paid_game_id == 3:
                if len(callback_query.data.split('_')) == 6:
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    kl = InlineKeyboardMarkup(row_width=3)
                    kl.add(
                        InlineKeyboardButton('Рандом 🎲', callback_data=f'play_paid_game_{paid_game_id}_{1}_{t}_{b}'),
                        InlineKeyboardButton('Позы 🧘‍♀️', callback_data=f'play_paid_game_{paid_game_id}_{2}_{t}_{b}'),
                        InlineKeyboardButton('Задания 🧐', callback_data=f'play_paid_game_{paid_game_id}_{3}_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_3_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home')
                           )
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text='Выберите тип игры, который хотите 🎯', reply_markup=kl)
                elif len(callback_query.data.split('_')) == 7:
                    tip = int(callback_query.data.split('_')[4])
                    ch = -1
                    if tip == 1:
                        ch = random.randint(1, 40)
                    elif tip == 2:
                        ch = random.randint(26, 40)
                    else:
                        ch = random.randint(1, 25)
                    game = session.query(Paid_game_info_3).filter(Paid_game_info_3.id == ch).first()
                    t, b = callback_query.data.split('_')[5], callback_query.data.split('_')[6]
                    if game.dop_info == 'Задание':
                        kl = InlineKeyboardMarkup(row_width=3)
                        kl.add(InlineKeyboardButton("Выполнено ✅",
                                                    callback_data=f'play_paid_game_{paid_game_id}_{1}_{t}_{b}_1'))
                        kl.add(InlineKeyboardButton('Рандом 🎲',
                                                    callback_data=f'play_paid_game_{paid_game_id}_{1}_{t}_{b}'),
                               InlineKeyboardButton('Позы 🧘‍♀️',
                                                    callback_data=f'play_paid_game_{paid_game_id}_{2}_{t}_{b}'),
                               InlineKeyboardButton('Задания 🧐',
                                                    callback_data=f'play_paid_game_{paid_game_id}_{3}_{t}_{b}'))
                        kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_3_{t}_{b}'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                        await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=tg_id,
                                                    text=f'*Секс по-новому*\n\n{game.caption}',
                                                    parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                    else:
                        kl = InlineKeyboardMarkup(row_width=3)
                        kl.add(InlineKeyboardButton("Выполнено ✅",
                                                    callback_data=f'play_paid_game_{paid_game_id}_{1}_{t}_{b}_1'))
                        kl.add(InlineKeyboardButton('Рандом 🎲',
                                                    callback_data=f'play_paid_game_{paid_game_id}_{1}_{t}_{b}'),
                               InlineKeyboardButton('Позы 🧘‍♀️',
                                                    callback_data=f'play_paid_game_{paid_game_id}_{2}_{t}_{b}'),
                               InlineKeyboardButton('Задания 🧐',
                                                    callback_data=f'play_paid_game_{paid_game_id}_{3}_{t}_{b}'))
                        kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_3_{t}_{b}'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home')
                               )
                        await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=tg_id,
                                                    text=f'*{game.dop_info}*\n\n{game.caption}',
                                                    parse_mode=ParseMode.MARKDOWN, reply_markup=kl)


                elif len(callback_query.data.split('_')) == 8:
                    tip = int(callback_query.data.split('_')[4])
                    t, b = callback_query.data.split('_')[5], callback_query.data.split('_')[6]
                    kl = InlineKeyboardMarkup()
                    kl = InlineKeyboardMarkup(row_width=3)
                    kl.add(
                        InlineKeyboardButton('Рандом 🎲', callback_data=f'play_paid_game_{paid_game_id}_{1}_{t}_{b}'),
                        InlineKeyboardButton('Позы 🧘‍♀️', callback_data=f'play_paid_game_{paid_game_id}_{2}_{t}_{b}'),
                        InlineKeyboardButton('Задания 🧐', callback_data=f'play_paid_game_{paid_game_id}_{3}_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_3_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home')
                           )
                    await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=tg_id,
                                                text=f'Выберите тип игры что бы перейти к следующей карточке 🎯',
                                                parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                    await up_balance(tg_id, 2)
            elif paid_game_id == 4:
                if len(callback_query.data.split('_')) == 6:
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                    text='Эта игра, которая поможет вывести ваши отношения на новый уровень!', )
                    kl = InlineKeyboardMarkup(row_width=2)
                    kl.add(InlineKeyboardButton('Правда ✅', callback_data=f'play_paid_game_{paid_game_id}_pr_{t}_{b}'),
                           InlineKeyboardButton('Наказание 🔴',
                                                callback_data=f'play_paid_game_{paid_game_id}_nak_{t}_{b}'))
                    kl.add(InlineKeyboardButton('В перемешку 🎲',
                                                callback_data=f'play_paid_game_{paid_game_id}_per_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_4_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home')
                           )
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text='Выберите тип игры',
                                                reply_markup=kl)
                elif len(callback_query.data.split('_')) == 7:
                    t, b = callback_query.data.split('_')[5], callback_query.data.split('_')[6]
                    kl = InlineKeyboardMarkup()
                    if callback_query.data.split('_')[4] == 'per':
                        kl.add(InlineKeyboardButton('Выполнено ✅', callback_data=callback_query.data + '_1'),
                               InlineKeyboardButton('Играть дальше ▶️',
                                                    callback_data=f'play_paid_game_{paid_game_id}_per_{t}_{b}'))
                    else:
                        kl.add(InlineKeyboardButton('Выполнено ✅', callback_data=callback_query.data + '_1'),
                               InlineKeyboardButton('Играть дальше ▶️',
                                                    callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_4_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    ran = -1
                    if callback_query.data.split('_')[4] == 'pr':
                        ran = random.randint(1, 25)
                    elif callback_query.data.split('_')[4] == 'nak':
                        ran = random.randint(26, 50)
                    else:
                        ran = random.randint(1, 50)
                    cap = session.query(Paid_game_info_4).filter(
                        Paid_game_info_4.id == ran).first()
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f'*{cap.dop_info}*\n\n{cap.caption}',
                                                reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                elif len(callback_query.data.split('_')) == 8:
                    t, b = callback_query.data.split('_')[5], callback_query.data.split('_')[6]
                    kl = InlineKeyboardMarkup()
                    if callback_query.data.split('_')[4] == 'per':
                        kl.add(
                            InlineKeyboardButton('Играть дальше ▶️',
                                                 callback_data=f'play_paid_game_{paid_game_id}_per_{t}_{b}'))
                    else:
                        kl.add(
                            InlineKeyboardButton('Играть дальше ▶️',
                                                 callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_4_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text='Выберите тип игры',
                                                reply_markup=kl)
                    await up_balance(tg_id, 5)
            elif paid_game_id == 5:
                if len(callback_query.data.split('_')) == 6:
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                    text='Рецепты наслаждений', )
                    kl = InlineKeyboardMarkup(row_width=2)
                    kl.add(
                        InlineKeyboardButton('Чувства 😍', callback_data=f'play_paid_game_{paid_game_id}_chyv_{t}_{b}'),
                        InlineKeyboardButton('Страсть ❤️‍🔥',
                                             callback_data=f'play_paid_game_{paid_game_id}_strast_{t}_{b}'))
                    kl.add(InlineKeyboardButton('Романтика 🌹',
                                                callback_data=f'play_paid_game_{paid_game_id}_rom_{t}_{b}'),
                           InlineKeyboardButton('В перемешку 🎲',
                                                callback_data=f'play_paid_game_{paid_game_id}_per_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_5_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text='Выберите тип игры:',
                                                reply_markup=kl)
                elif len(callback_query.data.split('_')) == 7:
                    kl = InlineKeyboardMarkup()
                    t, b = callback_query.data.split('_')[5], callback_query.data.split('_')[6]
                    ran = -1
                    if callback_query.data.split('_')[4] == 'chyv':
                        ran = random.randint(1, 5)
                        kl.add(InlineKeyboardButton('Выполнено ✅', callback_data=callback_query.data + '_1'),
                               InlineKeyboardButton('Играть дальше ▶️',
                                                    callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}')
                               )
                    elif callback_query.data.split('_')[4] == 'strast':
                        ran = random.randint(11, 15)
                        kl.add(InlineKeyboardButton('Выполнено ✅', callback_data=callback_query.data + '_1'),
                               InlineKeyboardButton('Играть дальше ▶️',
                                                    callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}')
                               )
                    elif callback_query.data.split('_')[4] == 'rom':
                        ran = random.randint(21, 25)
                        kl.add(InlineKeyboardButton('Выполнено ✅', callback_data=callback_query.data + '_1'),
                               InlineKeyboardButton('Играть дальше ▶️',
                                                    callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}'))
                    else:
                        cur = random.randint(1, 3)
                        if cur == 1:
                            ran = random.randint(1, 5)
                        elif cur == 2:
                            ran = random.randint(11, 15)
                        else:
                            ran = random.randint(21, 25)
                        kl.add(InlineKeyboardButton('Выполнено ✅', callback_data=callback_query.data + '_1'),
                               InlineKeyboardButton('Играть дальше ▶️',
                                                    callback_data=f'play_paid_game_{paid_game_id}_per_{t}_{b}'))
                    woman = session.query(Paid_game_info_5).filter(Paid_game_info_5.id == ran).first()
                    man = session.query(Paid_game_info_5).filter(Paid_game_info_5.id == ran + 5).first()
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_5_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f"*{woman.dop_info.split('_')[0]}*\n\n*{man.dop_info.split('_')[1]}*\n{man.caption}\n\n*{woman.dop_info.split('_')[1]}*\n{woman.caption}",
                                                reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                elif len(callback_query.data.split('_')) == 8:
                    kl = InlineKeyboardMarkup()
                    t, b = callback_query.data.split('_')[5], callback_query.data.split('_')[6]
                    ran = -1
                    if callback_query.data.split('_')[4] == 'chyv':

                        kl.add(
                            InlineKeyboardButton('Играть дальше ▶️',
                                                 callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}')
                        )
                    elif callback_query.data.split('_')[4] == 'strast':

                        kl.add(
                            InlineKeyboardButton('Играть дальше ▶️',
                                                 callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}')
                        )
                    elif callback_query.data.split('_')[4] == 'rom':

                        kl.add(
                            InlineKeyboardButton('Играть дальше ▶️',
                                                 callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}'))
                    else:

                        kl.add(
                            InlineKeyboardButton('Играть дальше ▶️',
                                                 callback_data=f'play_paid_game_{paid_game_id}_per_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_5_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                reply_markup=kl, text='👍 Нажмите на кнопку для продолжения игры')
                    await up_balance(tg_id, 5)
            elif paid_game_id == 6:
                if len(callback_query.data.split('_')) == 6:
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    kl = InlineKeyboardMarkup()
                    all_game = session.query(For_paid_game_info_6).filter(
                        For_paid_game_info_6.user_tg_id == tg_id).all()
                    for elem in all_game:
                        if elem.do == 'No':
                            kl.add(InlineKeyboardButton(elem.name + '🔘',
                                                        callback_data=f'play_paid_game_{paid_game_id}_{elem.id}_{t}_{b}'))
                        else:
                            kl.add(InlineKeyboardButton(elem.name + '🟢',
                                                        callback_data=f'play_paid_game_{paid_game_id}_{elem.id}_{t}_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'paid_game_6_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text='Выберите название которое вам понравилось, игры которые вы уже сделали отмечены 🟢 эмодзи',
                                                reply_markup=kl)
                elif len(callback_query.data.split('_')) == 7:
                    t, b = callback_query.data.split('_')[5], callback_query.data.split('_')[6]
                    elem_id = int(callback_query.data.split('_')[4])
                    elem = session.query(For_paid_game_info_6).filter(For_paid_game_info_6.id == elem_id).first()
                    kl = InlineKeyboardMarkup(row_width=2)
                    elem2 = session.query(Paid_game_info_6).filter(Paid_game_info_6.dop_info == elem.name).first()
                    if elem.do == "No":
                        kl.add(
                            InlineKeyboardButton('Скинуть партнёру 🕊',
                                                 callback_data=f'play_paid_game_6_{elem2.id}_0_{t}_{b}'),
                            InlineKeyboardButton('Выполнить ✅', callback_data=f'play_paid_game_6_{elem2.id}_1_{t}_{b}'))
                    else:
                        kl.add(
                            InlineKeyboardButton('Скинуть партнёру 🕊',
                                                 callback_data=f'play_paid_game_6_{elem2.id}_0_{t}_{b}'),
                            InlineKeyboardButton('Выполнено ✅',
                                                 callback_data=f'play_paid_game_6_{elem2.id}_1_{t}_{b}'))
                    kl.add(InlineKeyboardButton('К заданиям 📝', callback_data=f'play_paid_game_6_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f'*{elem2.dop_info}*\n{elem2.caption}',
                                                parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                elif len(callback_query.data.split('_')) == 8:
                    t, b = callback_query.data.split('_')[6], callback_query.data.split('_')[7]
                    elem_id = int(callback_query.data.split('_')[4])
                    d = int(callback_query.data.split('_')[5])
                    elem = session.query(Paid_game_info_6).filter(Paid_game_info_6.id == elem_id).first()
                    if d == 0:
                        partner = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                        if partner is None:
                            await bot.answer_callback_query(
                                text="К сожалению мы не можем найти вашего партнёра в базе 😔\nЕсли вы считаете что допущена ошибка напишите в поддержку",
                                callback_query_id=callback_query.id, show_alert=True)
                        else:

                            await bot.send_message(chat_id=partner.user_tg_id,
                                                   text=f'*{elem.dop_info}*\n{elem.caption}',
                                                   parse_mode=ParseMode.MARKDOWN)
                            await bot.answer_callback_query(
                                text="Мы отправили задание вашему партнёру, как выполните его нажмите на кнопку и получите sex-coin 😉",
                                callback_query_id=callback_query.id, show_alert=True)

                    elif d == 1:
                        elem2 = session.query(For_paid_game_info_6).filter(
                            For_paid_game_info_6.user_tg_id == tg_id).filter(
                            For_paid_game_info_6.name == elem.dop_info).first()
                        if elem2.do == "No":

                            await bot.answer_callback_query(
                                text="Круто!\nМы начислилим 3 sex-coin вам на баланс 😎, если вы не превысили лимит",
                                callback_query_id=callback_query.id, show_alert=True)

                            elem2.do = "Yes"
                            up_balance_(tg_id, 3)
                            session.add(elem2)
                            session.commit()
                        else:
                            await bot.answer_callback_query(
                                text="Вы уже это выполняли, попробуйте другую игру",
                                callback_query_id=callback_query.id, show_alert=True)
                        kl = InlineKeyboardMarkup()
                        kl.add(InlineKeyboardButton('Играть дальше ⏭', callback_data=f'play_paid_game_6_{t}_{b}'))
                        kl.add(InlineKeyboardButton('Скинуть партнёру 🕊',
                                                    callback_data=f'play_paid_game_6_{elem.id}_0_{t}_{b}'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                        await bot.edit_message_reply_markup(chat_id=tg_id,
                                                            message_id=callback_query.message.message_id,
                                                            reply_markup=kl)
            elif paid_game_id == 7:
                if len(callback_query.data.split('_')) == 6:
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    kl = InlineKeyboardMarkup(row_width=2)
                    kl.add(InlineKeyboardButton("Флирт 😏", callback_data=f'play_paid_game_7_1_{t}_{b}'),
                           InlineKeyboardButton("Cближение 🔗", callback_data=f'play_paid_game_7_2_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Возбуждение 🤩", callback_data=f'play_paid_game_7_3_{t}_{b}'),
                           InlineKeyboardButton("Рандом 🎲", callback_data=f'play_paid_game_7_4_{t}_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'paid_game_7_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text="Выбирайте или доверьтесь случайности в любом порядке, выполняйте указанное действие, и это будет не просто вечер, а вечер который вы запомните надолго.",
                                                reply_markup=kl)
                elif len(callback_query.data.split('_')) == 7:
                    t = int(callback_query.data.split('_')[4])
                    ch = -1
                    if t <= 3:
                        ch = random.randint(0, 8) * 3 + t
                    else:
                        ch = random.randint(1, 27)
                    elem = session.query(Paid_game_info_7).filter(Paid_game_info_7.id == ch).first()
                    t, b = callback_query.data.split('_')[5], callback_query.data.split('_')[6]
                    kl = InlineKeyboardMarkup(row_width=2)
                    kl.add(InlineKeyboardButton('Выполнено ✅', callback_data=callback_query.data + '_1'))
                    kl.add(InlineKeyboardButton("Флирт 😏", callback_data=f'play_paid_game_7_1_{t}_{b}'),
                           InlineKeyboardButton("Cближение 🔗", callback_data=f'play_paid_game_7_2_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Возбуждение 🤩", callback_data=f'play_paid_game_7_3_{t}_{b}'),
                           InlineKeyboardButton("Рандом 🎲", callback_data=f'play_paid_game_7_4_{t}_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'paid_game_7_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f'*{elem.dop_info}*\n\n{elem.caption}', reply_markup=kl,
                                                parse_mode=ParseMode.MARKDOWN)
                elif len(callback_query.data.split('_')) == 8:
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    kl = InlineKeyboardMarkup(row_width=2)
                    kl.add(InlineKeyboardButton("Флирт 😏", callback_data=f'play_paid_game_7_1_{t}_{b}'),
                           InlineKeyboardButton("Cближение 🔗", callback_data=f'play_paid_game_7_2_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Возбуждение 🤩", callback_data=f'play_paid_game_7_3_{t}_{b}'),
                           InlineKeyboardButton("Рандом 🎲", callback_data=f'play_paid_game_7_4_{t}_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'paid_game_7_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text="Выбирайте или доверьтесь случайности в любом порядке, выполняйте указанное действие, и это будет не просто вечер, а вечер который вы запомните надолго.",
                                                reply_markup=kl)
                    await up_balance(tg_id, 2)
            elif paid_game_id == 8:
                if len(callback_query.data.split('_')) == 6:
                    kl = InlineKeyboardMarkup()
                    ans = ''
                    ans += 'Старт 🚩 (Вы тут) \n'
                    mas = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
                    for i in range(47):
                        c = i + 1
                        for j in str(c):
                            ans += mas[int(j)]
                        ans += '\n'
                    ans += 'Финиш 🏁\n\n'
                    ans += f"Сейчас ходит {user.name}"
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    kl.add(InlineKeyboardButton('Бросить кубик 🎲', callback_data=f'play_paid_game_8_1_0_0_{t}_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'paid_game_8_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id, text=ans,
                                                reply_markup=kl)
                elif len(callback_query.data.split('_')) == 9:
                    t, b = callback_query.data.split('_')[7], callback_query.data.split('_')[8]
                    c1, c2 = int(callback_query.data.split('_')[5]), int(callback_query.data.split('_')[6])
                    if callback_query.data.split('_')[4] == '1':
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text=f'Смотрим на сколько продвинется {user.name}')
                    else:
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text=f'Смотрим на сколько продвинется {user.partner_name}')
                    a = await bot.send_dice(chat_id=tg_id)
                    await asyncio.sleep(3.3)
                    zn = int(a.dice.values['value'])
                    if callback_query.data.split('_')[4] == '1':
                        tec = c1 + zn
                        if tec > 47:
                            kl = InlineKeyboardMarkup()
                            kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_8_{t}_{b}'),
                                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                            await bot.send_message(chat_id=tg_id,
                                                   text=f'{user.name} победил! 🥳\nПоздравляем, на аккаунты зачисленны sex-coin',
                                                   reply_markup=kl)
                            await up_balance(tg_id, 20)
                        else:
                            elem = session.query(Paid_game_info_8).filter(Paid_game_info_8.id == tec).first()
                            kl = InlineKeyboardMarkup()
                            kl.add(InlineKeyboardButton('Выполнил ✅',
                                                        callback_data=f'play_paid_game_8_1_{tec}_{c2}_0_{t}_{b}'))
                            kl.add(InlineKeyboardButton('Стоять на месте ❌',
                                                        callback_data=f'play_paid_game_8_1_{c1}_{c2}_0_{t}_{b}'))
                            kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_8_{t}_{b}'),
                                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                            await bot.send_message(chat_id=tg_id,
                                                   text=f'{user.name} отметте\n\n*{elem.dop_info}*\n\n{elem.caption}',
                                                   reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                    else:
                        tec = c2 + zn
                        if tec > 47:
                            kl = InlineKeyboardMarkup()
                            kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_8_{t}_{b}'),
                                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                            await bot.send_message(chat_id=tg_id,
                                                   text=f'{user.partner_name} победил! 🥳\nПоздравляем, на аккаунты зачисленны sex-coin',
                                                   reply_markup=kl)
                            await up_balance(tg_id, 20)
                        else:
                            elem = session.query(Paid_game_info_8).filter(Paid_game_info_8.id == tec).first()
                            kl = InlineKeyboardMarkup()
                            kl.add(InlineKeyboardButton('Выполнил ✅',
                                                        callback_data=f'play_paid_game_8_2_{c1}_{tec}_0_{t}_{b}'))
                            kl.add(InlineKeyboardButton('Стоять на месте ❌',
                                                        callback_data=f'play_paid_game_8_2_{c1}_{c2}_0_{t}_{b}'))
                            kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_8_{t}_{b}'),
                                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                            await bot.send_message(chat_id=tg_id,
                                                   text=f'{user.partner_name} отметте\n\n*{elem.dop_info}*\n\n{elem.caption}',
                                                   reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                elif len(callback_query.data.split('_')) == 10:
                    kl = InlineKeyboardMarkup()
                    c1, c2 = int(callback_query.data.split('_')[5]), int(callback_query.data.split('_')[6])
                    mas = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
                    ans = 'Старт 🚩 '
                    c = 0
                    if c1 == c and c2 == c:
                        ans += 'Вы тут'
                    elif c1 == c:
                        ans += user.name
                    elif c2 == c:
                        ans += user.partner_name
                    ans += '\n'
                    for i in range(47):
                        c = i + 1
                        for j in str(c):
                            ans += mas[int(j)]
                        ans += ' '
                        if c1 == c and c2 == c:
                            ans += 'Вы тут'
                        elif c1 == c:
                            ans += user.name
                        elif c2 == c:
                            ans += user.partner_name
                        ans += '\n'
                    ans += 'Финиш 🏁\n\n'
                    t, b = callback_query.data.split('_')[8], callback_query.data.split('_')[9]
                    if callback_query.data.split('_')[4] == '1':
                        ans += f"Сейчас ходит {user.partner_name}"
                        kl.add(InlineKeyboardButton('Бросить кубик 🎲',
                                                    callback_data=f'play_paid_game_8_2_{c1}_{c2}_{t}_{b}'))
                    else:
                        ans += f"Сейчас ходит {user.name}"
                        kl.add(InlineKeyboardButton('Бросить кубик 🎲',
                                                    callback_data=f'play_paid_game_8_1_{c1}_{c2}_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_8_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id, text=ans,
                                                reply_markup=kl)
            elif paid_game_id == 10:  # Таблица 9
                if len(callback_query.data.split('_')) == 6:
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    kl = InlineKeyboardMarkup(row_width=2)
                    kl.add(InlineKeyboardButton('Для неё 👩', callback_data=f'play_paid_game_10_1_{t}_{b}'),
                           InlineKeyboardButton('Для него 👨', callback_data=f'play_paid_game_10_2_{t}_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'paid_game_10_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text='Выберите кто из вас будет выполнять задание 🎯', reply_markup=kl)
                elif len(callback_query.data.split('_')) == 7:
                    t, b = callback_query.data.split('_')[5], callback_query.data.split('_')[6]
                    kl = InlineKeyboardMarkup(row_width=2)
                    kl.add(InlineKeyboardButton("Не вышло ❌", callback_data=f'play_paid_game_10_1_0_{t}_{b}'),
                           InlineKeyboardButton('Получилось ✅', callback_data=f'play_paid_game_10_1_1_{t}_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'paid_game_10_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    ch = -1
                    t = int(callback_query.data.split('_')[4])
                    if t == 1:
                        ch = random.randint(1, 10)
                    else:
                        ch = random.randint(11, 20)
                    game = session.query(Paid_game_info_9).filter(Paid_game_info_9.id == ch).first()
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f'*{game.dop_info}*\n\n{game.caption}',
                                                parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                elif len(callback_query.data.split('_')) == 8:
                    t, b = callback_query.data.split('_')[6], callback_query.data.split('_')[7]
                    sd = int(callback_query.data.split('_')[5])
                    kl = InlineKeyboardMarkup()
                    kl.add(InlineKeyboardButton('Для неё 👩', callback_data=f'play_paid_game_10_1_{t}_{b}'),
                           InlineKeyboardButton('Для него 👨', callback_data=f'play_paid_game_10_2_{t}_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'paid_game_10_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    if sd == 1:
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text="Круто! 🤟\n\n*Sex-coin* зачисленны на аккаунт\n\nЕсли хотите продолжить выберите тип задание 🎯",
                                                    parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                        await up_balance(tg_id, 5)
                    else:
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text="Попробуйте ещё раз 🔄\n\nЕсли хотите продолжить выберите тип задание 🎯",
                                                    parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            elif paid_game_id == 9:  # Таблица 10
                if len(callback_query.data.split('_')) == 6:
                    ran = random.randint(1, 38)
                    gg = session.query(For_paid_game_info_9).filter(For_paid_game_info_9.id == ran).first()
                    poz = session.query(Poses).filter(Poses.pos_id == gg.pose_id).first()
                    f = int(poz.pos_lvl) * '⭐️'
                    kl = InlineKeyboardMarkup()
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    kl.add(InlineKeyboardButton('Выполнено ✅', callback_data=callback_query.data + '_1'),
                           InlineKeyboardButton("Следующая поза ⏭", callback_data=callback_query.data))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'__paid_game_9_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                    await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                                         caption=f'*{gg.name}*\n\n{gg.discrip}', reply_markup=kl,
                                         parse_mode=ParseMode.MARKDOWN)
                    await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                elif len(callback_query.data.split('_')) == 7:
                    kl = InlineKeyboardMarkup()
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    kl.add(
                        InlineKeyboardButton("Следующая поза ⏭",
                                             callback_data=callback_query.data[0:len(callback_query.data) - 2]))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'__paid_game_9_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                    await bot.edit_message_reply_markup(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                        reply_markup=kl)
                    await up_balance(tg_id, 5)
            elif paid_game_id == 11:
                if len(callback_query.data.split('_')) == 6:
                    ch = random.randint(1, 24)
                    kl = InlineKeyboardMarkup(row_width=2)
                    t, b = callback_query.data.split('_')[4], callback_query.data.split('_')[5]
                    kl.add(InlineKeyboardButton("Пропустить 😔", callback_data=f'play_paid_game_11_0_{t}_{b}'),
                           InlineKeyboardButton("Выполнено ✅", callback_data=f'play_paid_game_11_1_{t}_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'paid_game_11_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    game = session.query(Paid_game_info_11).filter(Paid_game_info_11.id == ch).first()
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f'*{game.dop_info}*\n\n{game.caption}', reply_markup=kl,
                                                parse_mode=ParseMode.MARKDOWN)
                elif len(callback_query.data.split('_')) == 7:
                    t, b = callback_query.data.split('_')[5], callback_query.data.split('_')[6]
                    kl = InlineKeyboardMarkup(row_width=2)
                    kl.add(InlineKeyboardButton('Играть дальше ⏩', callback_data=f'play_paid_game_11_{t}_{b}'))
                    kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'paid_game_11_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'), )
                    t = int(callback_query.data.split('_')[4])
                    if t == 1:
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text='Круто! 😎\n\n*3 Sex-coin* зачисленны на ваш баланс (если вы не превысите лимит)',
                                                    reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                        up_balance_(tg_id, 3)
                    else:
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text='Ничего страшного, можете попробовать ещё раз 😉',
                                                    reply_markup=kl)
        elif callback_query.data == 'poses':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton("Поза дня 📅", callback_data='play_free_game_1_p'))
            kl.add(InlineKeyboardButton("Генератор поз 🎲", callback_data='free_game_3_p'))
            kl.add(InlineKeyboardButton("Мои позы 🧘", callback_data='my_pose'))
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Сыграйте в игру или посмотрите коллекцию своих поз 🔎', reply_markup=kl)
        elif callback_query.data == '_poses':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton("Поза дня 📅", callback_data='play_free_game_1_p'))
            kl.add(InlineKeyboardButton("Генератор поз 🎲", callback_data='free_game_3_p'))
            kl.add(InlineKeyboardButton("Мои позы 🧘", callback_data='my_pose'))
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.send_message(chat_id=tg_id,
                                   text='Сыграйте в игру или посмотрите коллекцию своих поз 🔎', reply_markup=kl)
            await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
        elif callback_query.data == 'pl_1':  # Прав только хозяин
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.player1_id == tg_id).filter(
                For_paid_game_info_1.game_id == 1).filter(For_paid_game_info_1.play == 1).first()
            gam.player1_count = gam.player1_count + 5
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton('Остановиться 🏁', callback_data='pl_end'),
                   InlineKeyboardButton('Продолжить ⏭', callback_data='pl_next'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text=f"*{beatufull_str(user.name)}: {gam.player1_count} очков*\n\n*{beatufull_str(user.partner_name)}: {gam.player2_count} очков*\n\n{excoduc_name(gam.player1_count, gam.player2_count, user.name, user.partner_name)}",
                                        reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
        elif callback_query.data == 'pl_2':  # 2 партнёр
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.player1_id == tg_id).filter(
                For_paid_game_info_1.game_id == 1).filter(For_paid_game_info_1.play == 1).first()
            gam.player2_count = gam.player2_count + 5
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton('Остановиться 🏁', callback_data='pl_end'),
                   InlineKeyboardButton('Продолжить ⏭', callback_data='pl_next'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text=f"*{beatufull_str(user.name)}: {gam.player1_count} очков*\n\n*{beatufull_str(user.partner_name)}: {gam.player2_count} очков*\n\n{excoduc_name(gam.player1_count, gam.player2_count, user.name, user.partner_name)}",
                                        reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
        elif callback_query.data == 'pl_3':  # оба правы
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.player1_id == tg_id).filter(
                For_paid_game_info_1.game_id == 1).filter(For_paid_game_info_1.play == 1).first()
            gam.player2_count = gam.player2_count + 5
            gam.player1_count = gam.player1_count + 5
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton('Остановиться 🏁', callback_data='pl_end'),
                   InlineKeyboardButton('Продолжить ⏭', callback_data='pl_next'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text=f"*{beatufull_str(user.name)}: {gam.player1_count} очков*\n\n*{beatufull_str(user.partner_name)}: {gam.player2_count} очков*\n\n{excoduc_name(gam.player1_count, gam.player2_count, user.name, user.partner_name)}",
                                        reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
        elif callback_query.data == 'pl_4':  # оба ошиблись
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.player1_id == tg_id).filter(
                For_paid_game_info_1.game_id == 1).filter(For_paid_game_info_1.play == 1).first()
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton('Остановиться 🏁', callback_data='pl_end'),
                   InlineKeyboardButton('Продолжить ⏭', callback_data='pl_next'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text=f"*{beatufull_str(user.name)}: {gam.player1_count} очков*\n\n*{beatufull_str(user.partner_name)}: {gam.player2_count} очков*\n\n{excoduc_name(gam.player1_count, gam.player2_count, user.name, user.partner_name)}",
                                        reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
        elif callback_query.data == 'pl_next':
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.player1_id == tg_id).filter(
                For_paid_game_info_1.game_id == 1).filter(For_paid_game_info_1.play == 1).first()
            progress = session.query(Progress).filter(Progress.user_tg_id == int(tg_id)).filter(
                Progress.gam_id == 1).first()
            if progress is None:
                new1 = Progress()
                new1.gam_id = 1
                new1.user_tg_id = int(tg_id)
                new1.lvl = 1
                session.add(new1)
                session.commit()
                ch = 1
            else:
                ch = (progress.lvl) % 50 + 1
                progress.lvl = progress.lvl + 1
            session.add(progress)
            session.commit()
            vop = session.query(Paid_game_info_1).filter(Paid_game_info_1.id == ch).first()
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton(f'Только {user.name}', callback_data='pl_1'),
                   InlineKeyboardButton(f'Только {user.partner_name}', callback_data='pl_2'))
            kl.add(InlineKeyboardButton('Оба правы 😎', callback_data='pl_3'),
                   InlineKeyboardButton("Оба ошиблись  🙊", callback_data='pl_4'))
            await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=tg_id,
                                        text=f"Ответьте друг другу на вопрос и отметьте кто из вас прав ✅\n\n{vop.caption}",
                                        reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
        elif callback_query.data == 'pl_end':
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.player1_id == tg_id).filter(
                For_paid_game_info_1.game_id == 1).filter(For_paid_game_info_1.play == 1).first()
            gam.play = 0

            await bot.edit_message_text(
                text=excoduc_name_end(gam.player1_count, gam.player2_count, user.name, user.partner_name),
                message_id=callback_query.message.message_id, chat_id=tg_id, parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Главное меню 🏡', callback_data='home')))
            await up_balance(tg_id, gam.player1_count)
        elif callback_query.data[0:len('wat_pres_')] == 'wat_pres_':
            pres_id = int(callback_query.data.split('_')[2])
            if pres_id == 1:
                kl = InlineKeyboardMarkup(row_width=2)
                kl.add(InlineKeyboardButton("Назад 🔙", callback_data='present'),
                       InlineKeyboardButton("Открыть подарок 🔓", callback_data=f"open_present_{pres_id}"))
                kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text=f'Это подарок, который даётся за регистрацию!\n'
                                                 f'В этом подарке содержится колода карточек с позами и описанием, всего пять поз: 3 легкие, 1 средняя, 1 тяжелая',
                                            parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
        elif callback_query.data == 'store':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton("Промокоды 💱", callback_data='promo'))
            if user.buy_all == "N":
                kl.add(InlineKeyboardButton("Платные игры 🔒", callback_data='_paid_game'))
                kl.add(InlineKeyboardButton("Паки с позами 🧘‍♀️", callback_data='pak_pose'))
                kl.add(InlineKeyboardButton('Купить все 💳 (990 рублей)', callback_data='buy_alll'))
            kl.add(InlineKeyboardButton('Пополнить баланс 🆙', callback_data='top_up'))
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text=f'Магазин 🏪',
                                        parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
        elif callback_query.data == 'pak_pose':
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton('Обычная колода - 100 sex-coin', callback_data='usual_pak'))
            kl.add(InlineKeyboardButton('Редкая колода - 100 sex-coin', callback_data='rar_pak'))
            kl.add(InlineKeyboardButton('Эпическая колода - 100 sex-coin', callback_data='epic_pak'))
            kl.add(InlineKeyboardButton('Легендарная колода - 500 sex-coin', callback_data='legend_pak'))
            kl.add(InlineKeyboardButton('Назад 🔙', callback_data='store'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Нажмите на интересующую колоду 📌', reply_markup=kl)
        elif callback_query.data == 'legend_pak':
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton('Назад 🔙', callback_data='pak_pose'),
                   InlineKeyboardButton('Купить (500 sex-coin)', callback_data='buy_legend_pak'))
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text="Легендарная колода открывает доступ ко всем позам всех уровней. (100 поз)",
                                        reply_markup=kl)
        elif callback_query.data == 'buy_legend_pak':
            if user.balance < 500:
                await bot.answer_callback_query(text="К сожалению у вас не хватает sex-coin 😔",
                                                callback_query_id=callback_query.id, show_alert=True)
            else:
                user.balance = user.balance - 500
                session.add(user)
                session.commit()
                poses = session.query(Poses).all()
                l = [100, 100, 100, 100]
                for elem in poses:
                    if session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(
                            Open_poses.pos_id == elem.pos_id).first() == None:
                        if l[elem.pos_lvl] != 0:
                            l[elem.pos_lvl] -= 1
                            ne = Open_poses()
                            ne.pos_id = elem.pos_id
                            ne.name = elem.name
                            ne.user_id = tg_id
                            ne.pos_level = elem.pos_lvl
                            ne.see = "False"
                            session.add(ne)
                            session.commit()
                await bot.answer_callback_query(text="Поздравляем! 🥳\nВы можете посмотреть позы в своей коллекции",
                                                callback_query_id=callback_query.id, show_alert=True)
        elif callback_query.data == 'epic_pak':
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton('Назад 🔙', callback_data='pak_pose'),
                   InlineKeyboardButton('Купить (100 sex-coin)', callback_data='buy_epic_pak'))
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text="Эпическая колода состоит из:\n    1 легкие позы\n    1 средняя поза\n    3 тяжелая поза",
                                        reply_markup=kl)
        elif callback_query.data == 'buy_epic_pak':
            if user.balance < 100:
                await bot.answer_callback_query(text="К сожалению у вас не хватает sex-coin 😔",
                                                callback_query_id=callback_query.id, show_alert=True)
            else:
                user.balance = user.balance - 100
                session.add(user)
                session.commit()
                poses = session.query(Poses).all()
                l = [0, 1, 1, 3]
                for elem in poses:
                    if session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(
                            Open_poses.pos_id == elem.pos_id).first() == None:
                        if l[elem.pos_lvl] != 0:
                            l[elem.pos_lvl] -= 1
                            ne = Open_poses()
                            ne.pos_id = elem.pos_id
                            ne.name = elem.name
                            ne.user_id = tg_id
                            ne.pos_level = elem.pos_lvl
                            ne.see = "False"
                            session.add(ne)
                            session.commit()
                await bot.answer_callback_query(text="Поздравляем! 🥳\nВы можете посмотреть позы в своей коллекции",
                                                callback_query_id=callback_query.id, show_alert=True)
        elif callback_query.data == 'rar_pak':
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton('Назад 🔙', callback_data='pak_pose'),
                   InlineKeyboardButton('Купить (100 sex-coin)', callback_data='buy_rar_pak'))
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text="Редкая колода состоит из:\n    1 легкие позы\n    3 средняя поза\n    1 тяжелая поза",
                                        reply_markup=kl)
        elif callback_query.data == 'buy_rar_pak':
            if user.balance < 100:
                await bot.answer_callback_query(text="К сожалению у вас не хватает sex-coin 😔",
                                                callback_query_id=callback_query.id, show_alert=True)
            else:
                user.balance = user.balance - 100
                session.add(user)
                session.commit()
                poses = session.query(Poses).all()
                l = [0, 1, 3, 1]
                for elem in poses:
                    if session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(
                            Open_poses.pos_id == elem.pos_id).first() == None:
                        if l[elem.pos_lvl] != 0:
                            l[elem.pos_lvl] -= 1
                            ne = Open_poses()
                            ne.pos_id = elem.pos_id
                            ne.name = elem.name
                            ne.user_id = tg_id
                            ne.pos_level = elem.pos_lvl
                            ne.see = "False"
                            session.add(ne)
                            session.commit()
                await bot.answer_callback_query(text="Поздравляем! 🥳\nВы можете посмотреть позы в своей коллекции",
                                                callback_query_id=callback_query.id, show_alert=True)
        elif callback_query.data == 'usual_pak':
            kl = InlineKeyboardMarkup(row_width=2)
            kl.add(InlineKeyboardButton('Назад 🔙', callback_data='pak_pose'),
                   InlineKeyboardButton('Купить (100 sex-coin)', callback_data='buy_usual_pak'))
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text="Обычная колода состоит из:\n    3 легкие позы\n    1 средняя поза\n    1 тяжелая поза",
                                        reply_markup=kl)
        elif callback_query.data == 'buy_usual_pak':
            if user.balance < 100:
                await bot.answer_callback_query(text="К сожалению у вас не хватает sex-coin 😔",
                                                callback_query_id=callback_query.id, show_alert=True)
            else:
                user.balance = user.balance - 100
                session.add(user)
                session.commit()
                poses = session.query(Poses).all()
                l = [0, 3, 1, 1]
                for elem in poses:
                    if session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(
                            Open_poses.pos_id == elem.pos_id).first() == None:
                        if l[elem.pos_lvl] != 0:
                            l[elem.pos_lvl] -= 1
                            ne = Open_poses()
                            ne.pos_id = elem.pos_id
                            ne.name = elem.name
                            ne.user_id = tg_id
                            ne.pos_level = elem.pos_lvl
                            ne.see = "False"
                            session.add(ne)
                            session.commit()
                await bot.answer_callback_query(text="Поздравляем! 🥳\nВы можете посмотреть позы в своей коллекции",
                                                callback_query_id=callback_query.id, show_alert=True)
        elif callback_query.data == 'spromo':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton('Купить промокоды 🛒', callback_data='jpromo'))
            kl.add(InlineKeyboardButton("Мои промокоды 💯", callback_data='smy_promo'))
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Посмотри свои промокоды или купи новые 🆕', reply_markup=kl)
        elif callback_query.data == 'promo':
            kl = InlineKeyboardMarkup()
            all_promo = session.query(Promocode).filter(Promocode.user_tg_id == None).all()
            mas = []
            for elem in all_promo:
                if elem.price not in mas:
                    mas.append(elem.price)
            mas = sorted(mas)
            for elem in mas:
                kl.add(InlineKeyboardButton(f'{elem} sex-coin', callback_data=f'buy_promo_{elem}'))
            kl.add(InlineKeyboardButton("Назад 🔙", callback_data='store'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Выберите нужный промокод, курс скидки 1 к 1',
                                        parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
        elif callback_query.data == 'jpromo':
            kl = InlineKeyboardMarkup()
            all_promo = session.query(Promocode).filter(Promocode.user_tg_id == None).all()
            mas = []
            for elem in all_promo:
                if elem.price not in mas:
                    mas.append(elem.price)
            mas = sorted(mas)
            for elem in mas:
                kl.add(InlineKeyboardButton(f'{elem} sex-coin', callback_data=f'buy_promo_{elem}'))
            kl.add(InlineKeyboardButton("Назад 🔙", callback_data='spromo'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Выберите нужный промокод, курс скидки 1 к 1',
                                        parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
        elif callback_query.data[0:len('buy_promo_')] == 'buy_promo_':
            coin = int(callback_query.data.split('_')[2])
            if user.balance < coin:
                await bot.answer_callback_query(text="К сожалению у вас не хватает sex-coin 😔",
                                                callback_query_id=callback_query.id, show_alert=True)
            else:
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text="Смотрим наличие промокодов в базе...")
                texx = buy_promocode(tg_id, coin)
                if texx == 'К сожалению, на данный момент у нас нет активных промокодов!':
                    await bot.send_message(chat_id=tg_id, text=texx, parse_mode=ParseMode.MARKDOWN,
                                           reply_markup=InlineKeyboardMarkup().add(
                                               InlineKeyboardButton('Главное меню 🏡', callback_data='home')))
                else:
                    await bot.send_message(chat_id=tg_id, text=texx, parse_mode=ParseMode.MARKDOWN)
                    await bot.send_message(chat_id=tg_id, text='Желаем вам удачных покупок!',
                                           reply_markup=InlineKeyboardMarkup().add(
                                               InlineKeyboardButton('Главное меню 🏡', callback_data='home')))
        elif callback_query.data[0:len('open_present_')] == 'open_present_':
            pres_id = int(callback_query.data.split('_')[2])
            pres = session.query(Present).filter(Present.user_id == tg_id).filter(Present.present_id == pres_id).first()
            if pres.used == "True":
                await bot.answer_callback_query(text="К сожалению сегодня вы уже открывали этот подарок 😔",
                                                callback_query_id=callback_query.id, show_alert=True)
            else:
                pres.used = "True"
                session.add(pres)
                session.commit()
                if pres_id == 1:
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f'Мы начинаем высалать вам карточки')
                    for __ in range(3):
                        poz = session.query(Poses).filter(Poses.pos_lvl == 1).all()
                        ran = random.randint(1, len(poz))
                        ch = 1
                        for elem in poz:
                            if ch == ran:
                                ot = elem
                                await bot.send_photo(tg_id, photo=poz.file_id,
                                                     caption=f"*{ot.name}*\n\n{ot.caption}",
                                                     parse_mode=ParseMode.MARKDOWN)
                                break
                            ch += 1
                    poz = session.query(Poses).filter(Poses.pos_lvl == 2).all()
                    ran = random.randint(1, len(poz))
                    ch = 1
                    for elem in poz:
                        if ch == ran:
                            ot = elem
                            await bot.send_photo(tg_id, photo=poz.file_id,
                                                 caption=f"*{ot.name}*\n\n{ot.caption}",
                                                 parse_mode=ParseMode.MARKDOWN)
                            break
                        ch += 1
                    poz = session.query(Poses).filter(Poses.pos_lvl == 3).all()
                    ran = random.randint(1, len(poz))
                    ch = 1
                    for elem in poz:
                        if ch == ran:
                            ot = elem
                            await bot.send_photo(tg_id, photo=poz.file_id,
                                                 caption=f"*{ot.name}*\n\n{ot.caption}",
                                                 parse_mode=ParseMode.MARKDOWN)
                            break
                        ch += 1
        elif callback_query.data == 'my_game':
            paid_game_lst = session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).all()
            kl = InlineKeyboardMarkup()
            for elem in paid_game_lst:
                game = session.query(Paid_game).filter(Paid_game.game_id == elem.game_id).first()
                kl.add(InlineKeyboardButton(game.game_name, callback_data=f'spaid_game_{game.game_id}'))
            kl.add(InlineKeyboardButton("Назад 🔙", callback_data='game'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            if len(paid_game_lst) == 0:
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text='К сожалению пока список игр пуст 😔', reply_markup=kl)
            else:
                kl = InlineKeyboardMarkup()
                kl.add(InlineKeyboardButton('Чуства', callback_data='wpaid_game_1_b'))
                kl.add(InlineKeyboardButton('Страсть', callback_data='wpaid_game_2_b'))

                kl.add(InlineKeyboardButton('Все категории', callback_data='wpaid_game_4_b'))
                kl.add(InlineKeyboardButton("Назад 🔙", callback_data='game'),
                       InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text='Список купленных игр:', reply_markup=kl)
        elif callback_query.data == 'smy_game':
            paid_game_lst = session.query(Purchased_game).filter(Purchased_game.user_id == tg_id).all()
            kl = InlineKeyboardMarkup()
            for elem in paid_game_lst:
                game = session.query(Paid_game).filter(Paid_game.game_id == elem.game_id).first()
                kl.add(InlineKeyboardButton(game.game_name, callback_data=f'spaid_game_{game.game_id}'))
            kl.add(InlineKeyboardButton("Назад 🔙", callback_data='my_collection'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            if len(paid_game_lst) == 0:
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text='К сожалению пока список игр пуст 😔', reply_markup=kl)
            else:
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text='Список купленных игр:', reply_markup=kl)
        elif callback_query.data == 'zak_id':
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text=f"Напишите id заказа и мы начислим вам 10% sex-coin от суммы заказа",
                                        reply_markup=InlineKeyboardMarkup().add(
                                            InlineKeyboardButton('Главное меню 🏡', callback_data='home')))
            user.state = 'write_id'
            session.add(user)
            session.commit()
        elif callback_query.data[0:len('free_game_')] == 'free_game_':
            kl = InlineKeyboardMarkup(row_width=2)
            free_game_id = int(callback_query.data.split('_')[2])
            if free_game_id != 3:
                if free_game_id < 100:
                    paid_game = session.query(Free_game).filter(Free_game.game_id == free_game_id).first()
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='free_game'),
                           InlineKeyboardButton('Играть 🚀', callback_data=f'play_free_game_{free_game_id}'))
                    kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f'*{beatufull_str(paid_game.game_name)}*\n\n{paid_game.game_caption}',
                                                parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                else:
                    free_game_id -= 100
                    paid_game = session.query(Paid_game).filter(Paid_game.game_id == free_game_id).first()
                    kl.add(InlineKeyboardButton("Подробнее 🧐", url=paid_game.detail),
                           InlineKeyboardButton('Играть 🚀', callback_data=f'play_free_game_{free_game_id + 100}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='free_game'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f'*{beatufull_str(paid_game.game_name)}*\n\n{paid_game.game_caption}',
                                                parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            else:
                if len(callback_query.data.split('_')) == 4 and callback_query.data.split('_')[3] == 'p':
                    kl.add(InlineKeyboardButton('По уровню сложности', callback_data='play_free_game_4_p'))
                    kl.add(InlineKeyboardButton('Выбор поз партнерами', callback_data='play_free_game_5_p'))
                    kl.add(InlineKeyboardButton('Случайные позы', callback_data='play_free_game_6_p'))
                    kl.add(InlineKeyboardButton('Карточки со скрытой позой', callback_data='play_free_game_7_p'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='poses'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                else:
                    kl.add(InlineKeyboardButton('По уровню сложности', callback_data='play_free_game_4_f'))
                    kl.add(InlineKeyboardButton('Выбор поз партнерами', callback_data='play_free_game_5_f'))
                    kl.add(InlineKeyboardButton('Случайные позы', callback_data='play_free_game_6_f'))
                    kl.add(InlineKeyboardButton('Карточки со скрытой позой', callback_data='play_free_game_7_f'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='free_game'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text='Выберите как сгенерировать позы 🎲', reply_markup=kl)
        elif callback_query.data[0:len('play_free_game_')] == 'play_free_game_':
            free_game_id = int(callback_query.data.split('_')[3])
            if free_game_id == 1:
                kl = InlineKeyboardMarkup()
                if len(callback_query.data.split('_')) == 4:
                    poz = session.query(Poses).filter(Poses.pos_id == day_pose_id).first()
                    f = int(poz.pos_lvl) * '⭐️'
                    if user.take_pose != 'True':
                        kl.add(InlineKeyboardButton('Выполнено ✅', callback_data='play_free_game_1_0_0_0_0'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='play_free_game_1_0'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                    await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                                         caption=f'*{poz.name}*{poz.caption}*Сложность:* {f}', reply_markup=kl,
                                         parse_mode=ParseMode.MARKDOWN)
                    await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                elif len(callback_query.data.split('_')) == 8:

                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='play_free_game_1_0'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                    await bot.edit_message_reply_markup(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                        reply_markup=kl)
                    if user.take_pose != 'True':
                        await up_balance(tg_id, 5)
                    user.take_pose = 'True'
                else:
                    if callback_query.data.split('_')[4] == 'p':
                        poz = session.query(Poses).filter(Poses.pos_id == day_pose_id).first()
                        f = int(poz.pos_lvl) * '⭐️'
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data='_poses'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                        await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                                             caption=f'*{poz.name}*{poz.caption}*Сложность:* {f}', reply_markup=kl,
                                             parse_mode=ParseMode.MARKDOWN)
                        await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                    else:
                        free_game_id = 1
                        paid_game = session.query(Free_game).filter(Free_game.game_id == free_game_id).first()
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data='free_game'),
                               InlineKeyboardButton('Играть 🚀', callback_data=f'play_free_game_{free_game_id}'))
                        kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                        await bot.send_message(chat_id=tg_id,
                                               text=f'*{beatufull_str(paid_game.game_name)}*\n\n{paid_game.game_caption}',
                                               parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                        await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
            elif free_game_id == 2:
                if len(callback_query.data.split('_')) == 8:

                    kl = InlineKeyboardMarkup()
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='free_game_2'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_reply_markup(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                        reply_markup=kl)
                    if user.podpiska != 'True':
                        await up_balance(tg_id, 5)
                    user.podpiska = 'True'
                else:
                    ran = day_task_id
                    woman = session.query(Paid_game_info_5).filter(Paid_game_info_5.id == ran).first()
                    man = session.query(Paid_game_info_5).filter(Paid_game_info_5.id == ran + 5).first()
                    kl = InlineKeyboardMarkup()
                    if user.podpiska != 'True':
                        kl.add(InlineKeyboardButton('Выполнено ✅', callback_data='play_free_game_2_0_0_0_0'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data='free_game_2'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    if user.pol == 'man':
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text=f"*{woman.dop_info.split('_')[0]}*\n\n*{man.dop_info.split('_')[1]}*\n{man.caption}",
                                                    reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text=f"*{woman.dop_info.split('_')[0]}*\n\n*{man.dop_info.split('_')[1]}*\n{man.caption}",
                                                    reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
            elif free_game_id == 3:
                print('Как вы сюда попали...')
            elif free_game_id == 4:
                if len(callback_query.data.split('_')) == 5:
                    b = callback_query.data.split('_')[4]
                    kl = InlineKeyboardMarkup(row_width=2)
                    f = '⭐️'
                    kl.add(InlineKeyboardButton(f'1 уровень {f}', callback_data=f'play_free_game_4_1_{b}'))
                    kl.add(InlineKeyboardButton(f'2 уровень {f * 2}', callback_data=f'play_free_game_4_2_{b}'))
                    kl.add(InlineKeyboardButton(f'3 уровень {f * 3}', callback_data=f'play_free_game_4_3_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game_3_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, text='Выберите уровень сложности 🤟',
                                                message_id=callback_query.message.message_id, reply_markup=kl)
                elif len(callback_query.data.split('_')) == 6:
                    lvl = int(callback_query.data.split('_')[4])
                    b = callback_query.data.split('_')[5]
                    poses = session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter(
                        Open_poses.pos_level == lvl).all()
                    if len(poses) == 0:
                        await bot.answer_callback_query(
                            text="К сожалению у вас нету поз этого уровня 😔\nЗарабатывайте sex-coin и покупайте паки или заходите в бота каждый день, тут дарят позы",
                            callback_query_id=callback_query.id, show_alert=True)
                    else:

                        ch = random.randint(1, len(poses))
                        elem = -1
                        coun = 1
                        for el in poses:
                            if coun == ch:
                                elem = el
                                break
                            coun += 1
                        ran = elem.pos_id
                        poz = session.query(Poses).filter(Poses.pos_id == ran).first()
                        f = int(poz.pos_lvl) * '⭐️'
                        kl = InlineKeyboardMarkup()
                        kl.add(InlineKeyboardButton("Пропустить ❌", callback_data=f'play_free_game_4_{lvl}_{b}'),
                               InlineKeyboardButton("Выполнить ✅", callback_data=f'play_free_game_4_{lvl}_{b}_0_0'))
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'play_free_game_4_0_0_{b}'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                        await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                                             caption=f'*{poz.name}*{poz.caption}*Сложность:* {f}', reply_markup=kl,
                                             parse_mode=ParseMode.MARKDOWN)
                        await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                elif len(callback_query.data.split('_')) == 7:

                    b = callback_query.data.split('_')[6]
                    kl = InlineKeyboardMarkup(row_width=2)
                    f = '⭐️'
                    kl.add(InlineKeyboardButton(f'1 уровень {f}', callback_data=f'play_free_game_4_1_{b}'))
                    kl.add(InlineKeyboardButton(f'2 уровень {f * 2}', callback_data=f'play_free_game_4_2_{b}'))
                    kl.add(InlineKeyboardButton(f'3 уровень {f * 3}', callback_data=f'play_free_game_4_3_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game_3_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.send_message(chat_id=tg_id, text='Выберите уровень сложности 🤟', reply_markup=kl)
                    await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                elif len(callback_query.data.split('_')) == 8:
                    lvl = int(callback_query.data.split('_')[4])
                    b = callback_query.data.split('_')[5]
                    kl = InlineKeyboardMarkup()
                    kl.add(InlineKeyboardButton("Играть дальше ⏭", callback_data=f'play_free_game_4_{lvl}_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'play_free_game_4_0_0_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                    await bot.edit_message_reply_markup(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                        reply_markup=kl)
                    await up_balance(tg_id, 5)
            elif free_game_id == 6:
                kl = InlineKeyboardMarkup(row_width=2)
                if len(callback_query.data.split('_')) == 5:
                    poses = session.query(Open_poses).filter(Open_poses.user_id == tg_id).filter().all()
                    ch = random.randint(1, len(poses))
                    elem = -1
                    coun = 1
                    for el in poses:
                        if coun == ch:
                            elem = el
                            break
                        coun += 1
                    ran = elem.pos_id
                    poz = session.query(Poses).filter(Poses.pos_id == ran).first()
                    f = int(poz.pos_lvl) * '⭐️'
                    b = callback_query.data.split('_')[4]
                    kl.add(
                        InlineKeyboardButton("Пропустить ❌", callback_data=f'play_free_game_6_{b}'),
                        InlineKeyboardButton("Выполнить ✅", callback_data=f'play_free_game_6_{b}_0_0'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'play_free_game_6_0_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                    await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                                         caption=f'*{poz.name}*{poz.caption}*Сложность:* {f}', reply_markup=kl,
                                         parse_mode=ParseMode.MARKDOWN)
                    await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                elif len(callback_query.data.split('_')) == 6:
                    b = callback_query.data.split('_')[5]
                    kl.add(InlineKeyboardButton('По уровню сложности', callback_data=f'play_free_game_4_{b}'))
                    kl.add(InlineKeyboardButton('Выбор поз партнерами', callback_data=f'play_free_game_5_{b}'))
                    kl.add(InlineKeyboardButton('Случайные позы', callback_data=f'play_free_game_6_{b}'))
                    kl.add(InlineKeyboardButton('Карточки со скрытой позой', callback_data=f'play_free_game_7_{b}'))
                    if b == 'f':
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    else:
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'poses'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.send_message(chat_id=tg_id,
                                           text='Выберите как сгенерировать позы 🎲', reply_markup=kl)
                    await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                elif len(callback_query.data.split('_')) == 7:
                    b = callback_query.data.split('_')[4]
                    kl.add(InlineKeyboardButton("Играть дальше ⏭", callback_data=f'play_free_game_6_{b}'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'play_free_game_6_0_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                    await bot.edit_message_reply_markup(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                        reply_markup=kl)
                    await up_balance(tg_id, 5)
            elif free_game_id == 7:
                kl = InlineKeyboardMarkup(row_width=2)
                if len(callback_query.data.split('_')) == 5:
                    b = callback_query.data.split('_')[4]
                    co = 0
                    kl.add(
                        InlineKeyboardButton("Секретная поза 1 🙊",
                                             callback_data=f'play_free_game_7_-1_-1_-1_-1_-1_1_{b}'))
                    kl.add(
                        InlineKeyboardButton("Секретная поза 2 🤫",
                                             callback_data=f'play_free_game_7_-1_-1_-1_-1_-1_2_{b}'))
                    kl.add(
                        InlineKeyboardButton("Секретная поза 3 🤐",
                                             callback_data=f'play_free_game_7_-1_-1_-1_-1_-1_3_{b}'))
                    kl.add(
                        InlineKeyboardButton("Секретная поза 4 🙈",
                                             callback_data=f'play_free_game_7_-1_-1_-1_-1_-1_4_{b}'))
                    kl.add(
                        InlineKeyboardButton("Секретная поза 5 🤭",
                                             callback_data=f'play_free_game_7_-1_-1_-1_-1_-1_5_{b}'))
                    kl.add(InlineKeyboardButton('Всё сделано ✅',
                                                callback_data=f'play_free_game_7_-1_-1_-1_-1_-1_{b}_{co}_-1'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game_3_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text='В данной игре у вас пять карточек, в каждой из них случайная поза, открывайте карточки и смотрите что вам выпало\n\n``` Если вы вышли из игры, то карточки не сохранятся```',
                                                parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                elif len(callback_query.data.split('_')) == 12:
                    b = callback_query.data.split('_')[9]
                    co = int(callback_query.data.split('_')[10])
                    if co == 5:
                        ll = callback_query.data[0:len(callback_query.data) - 7]
                        he = callback_query.data.split('_')
                        kl = InlineKeyboardMarkup()
                        if he[4] == '-1':
                            kl.add(InlineKeyboardButton("Секретная поза 1 🙊", callback_data=ll + f'_1_{b}'))
                        else:
                            kl.add(InlineKeyboardButton(
                                session.query(Poses).filter(Poses.pos_id == int(he[4])).first().name + ' 🗝',
                                callback_data=ll + f'_1_{b}_0_0'))
                        if he[5] == '-1':
                            kl.add(InlineKeyboardButton("Секретная поза 2 🤫", callback_data=ll + f'_2_{b}'))
                        else:
                            kl.add(InlineKeyboardButton(
                                session.query(Poses).filter(Poses.pos_id == int(he[5])).first().name + ' 🔑',
                                callback_data=ll + f'_2_{b}_0_0'))
                        if he[6] == '-1':
                            kl.add(InlineKeyboardButton("Секретная поза 3 🤐", callback_data=ll + f'_3_{b}'))
                        else:
                            kl.add(InlineKeyboardButton(
                                session.query(Poses).filter(Poses.pos_id == int(he[6])).first().name + ' 🔧',
                                callback_data=ll + f'_3_{b}_0_0'))
                        if he[7] == '-1':
                            kl.add(InlineKeyboardButton("Секретная поза 4 🙈", callback_data=ll + f'_4_{b}'))
                        else:
                            kl.add(InlineKeyboardButton(
                                session.query(Poses).filter(Poses.pos_id == int(he[7])).first().name + ' 🔐',
                                callback_data=ll + f'_4_{b}_0_0'))
                        if he[8] == '-1':
                            kl.add(InlineKeyboardButton("Секретная поза 5 🤭", callback_data=ll + f'_5_{b}'))
                        else:
                            kl.add(InlineKeyboardButton(
                                session.query(Poses).filter(Poses.pos_id == int(he[8])).first().name + ' 🛠',
                                callback_data=ll + f'_5_{b}_0_0'))
                        kl.add(InlineKeyboardButton('Поменять набор 🔄', callback_data=f'play_free_game_7_{b}'))
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game_3_{b}'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                        if callback_query.data.split('_')[11] == '-1':
                            await bot.edit_message_reply_markup(chat_id=tg_id,
                                                                message_id=callback_query.message.message_id,
                                                                reply_markup=kl)
                            await up_balance(tg_id, 5)
                        else:
                            await bot.send_message(chat_id=tg_id,
                                                   text='В данной игре у вас пять карточек, в каждой из них случайная поза, открывайте карточки и смотрите что вам выпало\n\n``` Если вы вышли из игры, то карточки не сохранятся```',
                                                   parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                            await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                    elif co < 5:
                        await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                        text=f'Вам нужно открыть ещё {5 - co} карточек 🃏',
                                                        show_alert=True)
                elif len(callback_query.data.split('_')) == 10:
                    he = callback_query.data.split('_')
                    b = he[9]
                    co = 0
                    ll = callback_query.data[0:len(callback_query.data) - 2]
                    if he[4] == '-1':
                        kl.add(InlineKeyboardButton("Секретная поза 1 🙊", callback_data=ll + f'_1_{b}'))
                    else:
                        kl.add(InlineKeyboardButton(
                            session.query(Poses).filter(Poses.pos_id == int(he[4])).first().name + ' 🗝',
                            callback_data=ll + f'_1_{b}'))
                        co += 1
                    if he[5] == '-1':
                        kl.add(InlineKeyboardButton("Секретная поза 2 🤫", callback_data=ll + f'_2_{b}'))
                    else:
                        co += 1
                        kl.add(InlineKeyboardButton(
                            session.query(Poses).filter(Poses.pos_id == int(he[5])).first().name + ' 🔑',
                            callback_data=ll + f'_2_{b}'))
                    if he[6] == '-1':
                        kl.add(InlineKeyboardButton("Секретная поза 3 🤐", callback_data=ll + f'_3_{b}'))
                    else:
                        co += 1
                        kl.add(InlineKeyboardButton(
                            session.query(Poses).filter(Poses.pos_id == int(he[6])).first().name + ' 🔧',
                            callback_data=ll + f'_3_{b}'))
                    if he[7] == '-1':
                        kl.add(InlineKeyboardButton("Секретная поза 4 🙈", callback_data=ll + f'_4_{b}'))
                    else:
                        co += 1
                        kl.add(InlineKeyboardButton(
                            session.query(Poses).filter(Poses.pos_id == int(he[7])).first().name + ' 🔐',
                            callback_data=ll + f'_4_{b}'))
                    if he[8] == '-1':
                        kl.add(InlineKeyboardButton("Секретная поза 5 🤭", callback_data=ll + f'_5_{b}'))
                    else:
                        co += 1
                        kl.add(InlineKeyboardButton(
                            session.query(Poses).filter(Poses.pos_id == int(he[8])).first().name + ' 🛠',
                            callback_data=ll + f'_5_{b}'))
                    kl.add(InlineKeyboardButton('Всё сделано ✅',
                                                callback_data=f'{ll}_{b}_{co}_-1'))
                    kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game_3_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.send_message(chat_id=tg_id,
                                           text='В данной игре у вас пять карточек, в каждой из них случайная поза, открывайте карточки и смотрите что вам выпало\n\n``` Если вы вышли из игры, то карточки не сохранятся```',
                                           parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                    await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                elif len(callback_query.data.split('_')) == 11:
                    he = callback_query.data.split('_')
                    ran = -1
                    tec = int(he[9])
                    b = he[10]
                    if he[tec + 3] == '-1':
                        if random.randint(1, 2) % 2 == 1:
                            poses = session.query(Open_poses).filter(Open_poses.user_id == tg_id).all()
                            ch = random.randint(1, len(poses))
                            elem = -1
                            coun = 1
                            for el in poses:
                                if coun == ch:
                                    elem = el
                                    break
                                coun += 1
                            ran = elem.pos_id
                        else:
                            ran = random.randint(1, 100)
                    else:
                        ran = int(he[tec + 3])
                    he[tec + 3] = str(ran)
                    poz = session.query(Poses).filter(Poses.pos_id == ran).first()
                    f = int(poz.pos_lvl) * '⭐️'
                    kol = ''
                    for __ in range(len(he) - 3):
                        kol += he[__] + '_'
                    kol += he[-3]
                    kl.add(InlineKeyboardButton("Играть дальше ⏭", callback_data=kol + f'_{b}'))
                    kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                    await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                                         caption=f'*{poz.name}*{poz.caption}*Сложность:* {f}', reply_markup=kl,
                                         parse_mode=ParseMode.MARKDOWN)
                    await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                elif len(callback_query.data.split('_')) == 13:
                    he = callback_query.data.split('_')
                    ran = -1
                    tec = int(he[9])
                    b = he[10]
                    if he[tec + 3] == '-1':
                        if random.randint(1, 2) % 2 == 1:
                            poses = session.query(Open_poses).filter(Open_poses.user_id == tg_id).all()
                            ch = random.randint(1, len(poses))
                            elem = -1
                            coun = 1
                            for el in poses:
                                if coun == ch:
                                    elem = el
                                    break
                                coun += 1
                            ran = elem.pos_id
                        else:
                            ran = random.randint(1, 100)
                    else:
                        ran = int(he[tec + 3])
                    he[tec + 3] = str(ran)
                    poz = session.query(Poses).filter(Poses.pos_id == ran).first()
                    f = int(poz.pos_lvl) * '⭐️'
                    kol = ''
                    # print(he)
                    for __ in range(len(he) - 4):
                        kol += he[__] + '_'
                    # kol += he[-3]
                    # print(')
                    # print(kol + f'{b}_5_5')
                    kl.add(InlineKeyboardButton("Играть дальше ⏭", callback_data=kol + f'{b}_5_-5'))
                    kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                    await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                                         caption=f'*{poz.name}*{poz.caption}*Сложность:* {f}', reply_markup=kl,
                                         parse_mode=ParseMode.MARKDOWN)
                    await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
            elif free_game_id == 5:
                kl = InlineKeyboardMarkup()
                pom = callback_query.data.split('_')
                b = pom[-1]
                if len(pom) == 5:
                    sdfaa = 0
                    poses = session.query(Open_poses).filter(Open_poses.user_id == tg_id).all()
                    for elem in poses:
                        sdfaa += 1
                        kl.add(InlineKeyboardButton(elem.name, callback_data=f'play_free_game_5_{elem.pos_id}_{b}'))
                        if sdfaa == 10:
                            break
                    kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text='Выберите 1/2 позу ⏳', reply_markup=kl)
                elif len(pom) == 6:
                    sdfaa = 0
                    poses = session.query(Open_poses).filter(Open_poses.user_id == tg_id).all()
                    for elem in poses:
                        sdfaa += 1
                        kl.add(
                            InlineKeyboardButton(elem.name, callback_data=callback_query.data[0:len(
                                callback_query.data) - 2] + f'_{elem.pos_id}_{b}'))
                        if sdfaa == 10:
                            break
                    kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text='Выберите 2/2 позу ⌛️', reply_markup=kl)
                elif len(pom) == 7:
                    if random.randint(1, 2) == 1:
                        await bot.send_message(chat_id=tg_id, text='Бот выбрал первую позу')
                        poz = session.query(Poses).filter(
                            Poses.pos_id == int(callback_query.data.split('_')[4])).first()
                        f = int(poz.pos_lvl) * '⭐️'
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'play_free_game_5_0_0_0_0_{b}'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                        await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                                             caption=f'*{poz.name}*{poz.caption}*Сложность:* {f}', reply_markup=kl,
                                             parse_mode=ParseMode.MARKDOWN)
                    else:
                        await bot.send_message(chat_id=tg_id, text='Бот выбрал вторую позу')
                        poz = session.query(Poses).filter(
                            Poses.pos_id == int(callback_query.data.split('_')[5])).first()
                        f = int(poz.pos_lvl) * '⭐️'
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'play_free_game_5_0_0_0_0_{b}'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
                        await bot.send_photo(chat_id=tg_id, photo=poz.file_id,
                                             caption=f'*{poz.name}*{poz.caption}*Сложность:* {f}', reply_markup=kl,
                                             parse_mode=ParseMode.MARKDOWN)
                    await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                elif len(pom) == 9:
                    kl.add(InlineKeyboardButton('По уровню сложности', callback_data=f'play_free_game_4_{b}'))
                    kl.add(InlineKeyboardButton('Выбор поз партнерами', callback_data=f'play_free_game_5_{b}'))
                    kl.add(InlineKeyboardButton('Случайные позы', callback_data=f'play_free_game_6_{b}'))
                    kl.add(InlineKeyboardButton('Карточки со скрытой позой', callback_data=f'play_free_game_7_{b}'))
                    if b == 'f':
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data='free_game'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    elif b == 'p':
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data='poses'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                    await bot.send_message(chat_id=tg_id,
                                           text='Выберите как сгенерировать позы 🎲', reply_markup=kl)
                    await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
            else:
                paid_game_id = free_game_id - 100
                if paid_game_id == 1:
                    if len(callback_query.data.split('_')) == 4:
                        # 1 играет 1, 2 играют вдвоём
                        kl = InlineKeyboardMarkup(row_width=2)
                        kl.add(InlineKeyboardButton('С одного 1️⃣', callback_data=f'play_paid_game_{paid_game_id}_1'),
                               InlineKeyboardButton('С двух 2️⃣', callback_data=f'play_paid_game_{paid_game_id}_2'))
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game_{paid_game_id + 100}'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                        await bot.edit_message_text(
                            chat_id=tg_id, message_id=callback_query.message.message_id,
                            text="Выберите как вы хотите играть, с одного телефона или с партнёром с двух 📲",
                            reply_markup=kl)
                    else:
                        count_play = int(callback_query.data.split('_')[4])
                        if count_play == 2:
                            partner_phone_number = user.partner_phone_number
                            partner = session.query(User).filter(User.partner_phone_number == user.phone_number).filter(
                                User.phone_number == partner_phone_number).first()
                            if partner is None:
                                await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                                text="К сожалению мы не можем найти вашего партнёра 😔\nПопробуйте написать в поддержку, мы вам поможем",
                                                                show_alert=True)
                            else:
                                user.state = 'write_wish'
                                partner.state = 'write_wish'
                                al = session.query(For_paid_game_info_1).all()
                                for elem in al:
                                    if elem.player1_id == tg_id or elem.player2_id == tg_id:
                                        elem.play = 0
                                        session.add(elem)
                                        session.commit()
                                new = For_paid_game_info_1()
                                new.game_id = 1
                                new.players = 2
                                new.player1_id = user.user_tg_id
                                new.player2_id = partner.user_tg_id
                                new.player1_count = 0
                                new.player2_count = 0
                                new.play_now = 0
                                new.play = 1
                                session.add(new)
                                session.add(partner)
                                session.add(user)
                                session.commit()
                                await bot.send_message(chat_id=partner.user_tg_id,
                                                       text="Ваш партнёр позвал вас играть в *А ты знаешь, что*\nНапишите своё желание, в случае вашей победы, мы отправим его партнёру",
                                                       parse_mode=ParseMode.MARKDOWN)
                                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                            text="Игра: *А ты знаешь, что* началась\nДля начала напиши своё желание, в случае вашей победы, мы отправим его твоему партнёру",
                                                            parse_mode=ParseMode.MARKDOWN)
                        elif count_play == 1:
                            await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=tg_id,
                                                        text="Напишите свои желания на листочке, после окончания игры проигравшему достанется желание партнёра 📝")
                            al = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.play == 1).all()
                            for elem in al:
                                if elem.player1_id == tg_id or elem.player2_id == tg_id:
                                    elem.play = 0
                                    session.add(elem)
                                    session.commit()
                            new = For_paid_game_info_1()
                            new.game_id = 1
                            new.players = 1
                            new.player1_id = user.user_tg_id
                            new.player1_count = 0
                            new.player2_count = 0
                            new.play = 1
                            progress = session.query(Progress).filter(Progress.user_tg_id == int(tg_id)).filter(
                                Progress.gam_id == 1).first()
                            if progress is None:
                                new1 = Progress()
                                new1.gam_id = 1
                                new1.user_tg_id = int(tg_id)
                                new1.lvl = 1
                                session.add(new1)
                                session.commit()
                                ch = 1
                            else:
                                ch = (progress.lvl) % 50 + 1
                                progress.lvl = progress.lvl + 1
                            session.add(progress)
                            session.add(new)
                            session.commit()
                            vop = session.query(Paid_game_info_1).filter(Paid_game_info_1.id == ch).first()
                            kl = InlineKeyboardMarkup(row_width=2)
                            kl.add(InlineKeyboardButton(f'Только {user.name}', callback_data='pl_1'),
                                   InlineKeyboardButton(f'Только {user.partner_name}', callback_data='pl_2'))
                            kl.add(InlineKeyboardButton('Оба правы 😎', callback_data='pl_3'),
                                   InlineKeyboardButton("Оба ошиблись  🙊", callback_data='pl_4'))
                            await bot.send_message(chat_id=tg_id,
                                                   text=f"Ответьте друг другу на вопрос и отметьте кто из вас прав ✅\n\n{vop.caption}",
                                                   reply_markup=kl)
                elif paid_game_id == 2:
                    f = 0
                    if len(callback_query.data.split('_')) == 4:
                        partner = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                        if partner is None or user.partner_phone_number is None or partner.partner_phone_number != user.phone_number:
                            await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                            text="К сожалению мы не можем найти вашего партнёра 😔\nПопробуйте написать в поддержку, мы вам поможем",
                                                            show_alert=True)
                        else:
                            finish_all_game(tg_id)
                            finish_all_game(partner.user_tg_id)
                            kl = InlineKeyboardMarkup(row_width=2)
                            kl.add(
                                InlineKeyboardButton(f'{beatufull_str(user.name)}', callback_data='play_paid_game_2_1'),
                                InlineKeyboardButton(f'{beatufull_str(user.partner_name)}',
                                                     callback_data='play_paid_game_2_2'))

                            kl.add(InlineKeyboardButton("Назад 🔙", callback_data=f'free_game_102'),
                                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                        text="Выберите кто из вас начнёт игру 🎯", reply_markup=kl)
                    elif len(callback_query.data.split('_')) == 5:
                        partner = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                        if partner is not None:
                            await bot.edit_message_text(text="Игра *Говори или подчиняйся* началась",
                                                        message_id=callback_query.message.message_id, chat_id=tg_id,
                                                        parse_mode=ParseMode.MARKDOWN)
                            n = For_paid_game_info_2()
                            n.play = 1
                            n.player1_id = tg_id
                            n.player2_id = partner.user_tg_id
                            n.game_id = 2
                            n.player1_count = 0
                            n.player2_count = 0
                            c = int(callback_query.data.split('_')[4])
                            n.hwo_last = c
                            session.add(n)
                            session.commit()
                            gam = session.query(For_paid_game_info_2).filter(For_paid_game_info_2.play == 1).filter(
                                For_paid_game_info_2.player1_id == tg_id).filter(
                                For_paid_game_info_2.player2_id == partner.user_tg_id).filter(
                                For_paid_game_info_2.hwo_last == c).first()
                            if c == 1:
                                kl = InlineKeyboardMarkup(row_width=2)
                                kl.add(InlineKeyboardButton("Отвечай 🤓", callback_data='play_paid_game_2_2_1_0'),
                                       InlineKeyboardButton("Выполняй 💪", callback_data='play_paid_game_2_2_2_0'))
                                kl.add(InlineKeyboardButton('Закончить игру ❌', callback_data=f"break_2_{gam.id}"))
                                await bot.send_message(chat_id=tg_id,
                                                       text="Игра *Говори или подчиняйся*\n\nСейчас ваш ход вам нужно выбрать то, что вы будете делать",
                                                       reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                            elif c == 2:
                                kl = InlineKeyboardMarkup(row_width=2)
                                kl.add(InlineKeyboardButton("Отвечай 🤓", callback_data='play_paid_game_2_1_1_0'),
                                       InlineKeyboardButton("Выполняй 💪", callback_data='play_paid_game_2_1_2_0'))
                                kl.add(InlineKeyboardButton('Закончить игру ❌', callback_data=f"break_2_{gam.id}"))
                                await bot.send_message(chat_id=partner.user_tg_id,
                                                       text="Игра *Говори или подчиняйся*\n\nСейчас ваш ход вам нужно выбрать то, что вы будете делать",
                                                       reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
                    elif len(callback_query.data.split('_')) == 7:
                        partner = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                        c = int(callback_query.data.split('_')[4])
                        d = int(callback_query.data.split('_')[5])
                        await bot.edit_message_text(chat_id=tg_id, text='Вашему партнёру пришло задание',
                                                    message_id=callback_query.message.message_id)
                        ch = -1
                        gam = session.query(For_paid_game_info_2).filter(For_paid_game_info_2.play == 1).filter(
                            For_paid_game_info_2.player1_id == tg_id).filter(
                            For_paid_game_info_2.player2_id == partner.user_tg_id).first()
                        if gam is None:
                            gam = session.query(For_paid_game_info_2).filter(For_paid_game_info_2.play == 1).filter(
                                For_paid_game_info_2.player2_id == tg_id).filter(
                                For_paid_game_info_2.player1_id == partner.user_tg_id).first()
                            gam.player2_count += 3
                        else:
                            gam.player1_count += 3
                        if d == 1:
                            progress = session.query(Progress).filter(
                                Progress.user_tg_id == int(partner.user_tg_id)).filter(
                                Progress.gam_id == 2).filter(Progress.dop_info == 'Вопросы').first()
                            if progress is None:
                                ch = 1
                                new = Progress()
                                new.lvl = 1
                                new.gam_id = 2
                                new.user_tg_id = partner.user_tg_id
                                new.dop_info = 'Вопросы'
                                session.add(new)
                                session.commit()
                            else:
                                ch = progress.lvl % 25 + 1
                                progress.lvl = progress.lvl + 1
                                session.add(progress)
                                session.commit()
                        else:
                            progress = session.query(Progress).filter(
                                Progress.user_tg_id == int(partner.user_tg_id)).filter(
                                Progress.gam_id == 2).filter(Progress.dop_info == 'Действия').first()
                            if progress is None:
                                ch = 26
                                new = Progress()
                                new.lvl = 26
                                new.gam_id = 2
                                new.dop_info = 'Действия'
                                new.user_tg_id = partner.user_tg_id
                                session.add(new)
                                session.commit()
                            else:
                                if progress.lvl == 50:
                                    progress.lvl = 25
                                progress.lvl += 1
                                ch = progress.lvl
                                session.add(progress)
                                session.commit()
                        kl = InlineKeyboardMarkup(row_width=2)
                        kl.add(InlineKeyboardButton("Отвечай 🤓", callback_data='play_paid_game_2_2_1_0'),
                               InlineKeyboardButton("Выполняй 💪", callback_data='play_paid_game_2_2_2_0'))
                        kl.add(InlineKeyboardButton('Закончить игру ❌', callback_data=f"break_2_{gam.id}"))
                        game = session.query(Paid_game_info_2).filter(Paid_game_info_2.id == ch).first()
                        await bot.send_message(chat_id=partner.user_tg_id,
                                               text=f'*{game.dop_info}*\n\n{game.caption}\n\nВыберите что будет делать ваш партнёр или закончите игру',
                                               parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                elif paid_game_id == 7:
                    if len(callback_query.data.split('_')) == 4:
                        kl = InlineKeyboardMarkup(row_width=2)
                        kl.add(InlineKeyboardButton("Флирт 😏", callback_data=f'play_free_game_107_1'),
                               InlineKeyboardButton("Cближение 🔗", callback_data=f'play_free_game_107_2'))
                        kl.add(InlineKeyboardButton("Возбуждение 🤩", callback_data=f'play_free_game_107_3'),
                               InlineKeyboardButton("Рандом 🎲", callback_data=f'play_free_game_107_4'))
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game_107'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text="Выбирайте или доверьтесь случайности в любом порядке, выполняйте указанное действие, и это будет не просто вечер, а вечер который вы запомните надолго.",
                                                    reply_markup=kl)
                    elif len(callback_query.data.split('_')) == 5:
                        t = int(callback_query.data.split('_')[4])
                        ch = -1
                        if t <= 3:
                            ch = random.randint(0, 8) * 3 + t
                        else:
                            ch = random.randint(1, 27)
                        elem = session.query(Paid_game_info_7).filter(Paid_game_info_7.id == ch).first()
                        kl = InlineKeyboardMarkup(row_width=2)
                        kl.add(InlineKeyboardButton('Выполнено ✅', callback_data=callback_query.data + '_1'))
                        kl.add(InlineKeyboardButton("Флирт 😏", callback_data=f'play_free_game_107_1'),
                               InlineKeyboardButton("Cближение 🔗", callback_data=f'play_free_game_107_2'))
                        kl.add(InlineKeyboardButton("Возбуждение 🤩", callback_data=f'play_free_game_107_3'),
                               InlineKeyboardButton("Рандом 🎲", callback_data=f'play_free_game_107_4'))
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game_107'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text=f'*{elem.dop_info}*\n\n{elem.caption}', reply_markup=kl,
                                                    parse_mode=ParseMode.MARKDOWN)
                    elif len(callback_query.data.split('_')) == 6:
                        kl = InlineKeyboardMarkup(row_width=2)
                        kl.add(InlineKeyboardButton("Флирт 😏", callback_data=f'play_free_game_107_1'),
                               InlineKeyboardButton("Cближение 🔗", callback_data=f'play_free_game_107_2'))
                        kl.add(InlineKeyboardButton("Возбуждение 🤩", callback_data=f'play_free_game_107_3'),
                               InlineKeyboardButton("Рандом 🎲", callback_data=f'play_free_game_107_4'))
                        kl.add(InlineKeyboardButton('Назад 🔙', callback_data=f'free_game_107'),
                               InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text="Выбирайте или доверьтесь случайности в любом порядке, выполняйте указанное действие, и это будет не просто вечер, а вечер который вы запомните надолго.",
                                                    reply_markup=kl)
                        await up_balance(tg_id, 2)
        elif callback_query.data[0:len('answ')] == 'answ':
            id = int(callback_query.data.split('_')[1])
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.id == id).first()
            gam.play_now = gam.play_now + 1
            answer = callback_query.data.split('_')[2]
            play_1 = True
            if int(gam.player2_id) == int(tg_id):
                play_1 = False
            if answer == 'y':
                if play_1:
                    gam.player2_count = gam.player2_count + 5
                else:
                    gam.player1_count = gam.player1_count + 5
            if gam.play_now == gam.players:
                gam.play_now = 0
                if play_1:
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f'В данной игре у вас: *{gam.player1_count}* очков\n\n'
                                                     f'У вашего партнёра: *{gam.player2_count}* очков\n\n'
                                                     f'Пока {excoduc(gam.player1_count, gam.player2_count)}',
                                                parse_mode=ParseMode.MARKDOWN)
                    await bot.send_message(chat_id=gam.player2_id, text=f'Мы получили ответ от вашего партнёра\n\n'
                                                                        f'В данной игре у вас: *{gam.player2_count}* очков\n\n'
                                                                        f'У вашего партнёра: *{gam.player1_count}* очков\n\n'
                                                                        f'Пока {excoduc(gam.player2_count, gam.player1_count)}',
                                           parse_mode=ParseMode.MARKDOWN)
                else:
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f'В данной игре у вас: *{gam.player2_count}* очков\n\n'
                                                     f'У вашего партнёра: *{gam.player1_count}* очков\n\n'
                                                     f'Пока {excoduc(gam.player2_count, gam.player1_count)}',
                                                parse_mode=ParseMode.MARKDOWN)
                    await bot.send_message(chat_id=gam.player1_id, text=f'Мы получили ответ от вашего партнёра\n\n'
                                                                        f'В данной игре у вас: *{gam.player1_count}* очков\n\n'
                                                                        f'У вашего партнёра: *{gam.player2_count}* очков\n\n'
                                                                        f'Пока {excoduc(gam.player1_count, gam.player2_count)}',
                                           parse_mode=ParseMode.MARKDOWN)
                await bot.send_message(chat_id=gam.player1_id, text='Хотите продолжить игру? 😉',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Остановиться 🏁', callback_data=f'end_ans_{gam.id}'),
                                           InlineKeyboardButton("Продолжить ⏭", callback_data=f'next_ans_{gam.id}')))
            else:
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text=f'Мы всё записали, осталось дождаться вашего партнёра ⌛️')
            session.add(gam)
            session.commit()
        elif callback_query.data[0:len('end_ans_')] == 'end_ans_':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            id = int(callback_query.data.split('_')[2])
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.id == id).first()
            gam.play = 0
            if gam.player1_count == gam.player2_count:
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text=f"У вас ничья 🥳\n\nВы оба увидите загаданные желания\n\n*Желание вашего партнёра:* {gam.wish2}",
                                            parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                await bot.send_message(chat_id=gam.player2_id,
                                       text=f"У вас ничья 🥳\n\nВы оба увидите загаданные желания\n\n*Желание вашего партнёра:* {gam.wish1}",
                                       parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            elif gam.player1_count > gam.player2_count:
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text=f'Вы победили 🎉\n\nМы отправим ваше желание партнёру',
                                            reply_markup=kl)
                await bot.send_message(chat_id=gam.player2_id,
                                       text=f"К сожалению вы проиграли 😔\n\n*Желание вашего партнёра:* {gam.wish1}",
                                       parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            else:
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text=f"К сожалению вы проиграли 😔\n\n*Желание вашего партнёра:* {gam.wish2}",
                                            parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                await bot.send_message(chat_id=gam.player2_id,
                                       text=f'Вы победили 🎉\n\nМы отправим ваше желание партнёру', reply_markup=kl)
            await up_balance(gam.player1_id, gam.player1_count)
            await up_balance(gam.player2_id, gam.player2_count)
            session.add(gam)
            session.commit()
        elif callback_query.data[0:len('next_ans_')] == 'next_ans_':
            id = int(callback_query.data.split('_')[2])
            gam = session.query(For_paid_game_info_1).filter(For_paid_game_info_1.id == id).first()
            user.state = 'answer_vop'
            part = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
            part.state = 'answer_vop'
            progress = session.query(Progress).filter(Progress.user_tg_id == int(gam.player1_id)).filter(
                Progress.gam_id == 1).first()
            if progress is None:
                new = Progress()
                new.gam_id = 1
                new.user_tg_id = int(gam.player1_id)
                new.lvl = 1
                session.add(new)
                session.commit()
                ch = 1
            else:
                ch = (progress.lvl) % 50 + 1
                progress.lvl = progress.lvl + 1
                session.add(progress)
            vop = session.query(Paid_game_info_1).filter(Paid_game_info_1.id == ch).first()
            kl = ReplyKeyboardMarkup(resize_keyboard=True)
            kl.add(KeyboardButton('Ответил в живую 📵'))
            await bot.edit_message_text(chat_id=user.user_tg_id, message_id=callback_query.message.message_id,
                                        text=f'Напишите ответ прямо в бота (нажмите на клавиатуру и напечатайте) или нажмите на кнопку')
            await bot.send_message(chat_id=part.user_tg_id,
                                   text=f'Напишите ответ прямо в бота (нажмите на клавиатуру и напечатайте) или нажмите на кнопку')
            await bot.send_message(chat_id=user.user_tg_id, text=f'*А ты знаешь, что*\n\n{vop.caption}',
                                   reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
            await bot.send_message(chat_id=part.user_tg_id, text=f'*А ты знаешь, что*\n\n{vop.caption}',
                                   reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
            gam.play_now = 0
            gam.game_id_id = ch
            session.add(part)
            session.add(user)
            session.add(gam)
            session.commit()
        elif callback_query.data == 'add_phone':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home_'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Можете вернуться в главное меню', reply_markup=kl)
            kl = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            kl.add(KeyboardButton('Поделиться своим номером ☎️', request_contact=True))
            user.state = 'write_phone'
            await bot.send_message(chat_id=tg_id, text='Поделитесь номером, нажав на кнопку', reply_markup=kl)
        elif callback_query.data == 'my_profile':
            kl = InlineKeyboardMarkup()
            kl.add(InlineKeyboardButton("Поменять имя 🔄", callback_data='change_name'))
            if user.pol == 'man':
                kl.add(InlineKeyboardButton("Мой партнёр 👩", callback_data='partner'))
            else:
                kl.add(InlineKeyboardButton("Мой партнёр 👨", callback_data='partner'))
            if user.buy_all == "N":
                kl.add(InlineKeyboardButton('Купить всё что есть 🤑', callback_data='buy_all'))
            # kl.add(InlineKeyboardButton('Подарки 🎁', callback_data='present'))
            kl.add(InlineKeyboardButton("Мои промокоды 💯", callback_data='my_promo'))
            tex = f"*Ваше имя:* {user.name}\n\n"
            if len(user.phone_number) == 0:
                tex += "*Номер телефона:* не добавлен 🔴"
                kl.add(InlineKeyboardButton("Добавить телефон ☎️", callback_data='add_phone'))
            else:
                tex += "*Номер телефона:* добавлен 🟢"
            if user.partner_name == 'партнёр':
                tex += "\n\n*Партнёр:* не добавлен 🔴"
            else:
                tex += "\n\n*Партнёр:* добавлен 🟢"

            kl.add(InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text=tex,
                                        reply_markup=kl, parse_mode=ParseMode.MARKDOWN)
        elif callback_query.data == 'partner':
            klpar = InlineKeyboardMarkup(row_width=2)
            if user.partner_phone_number == None:
                klpar.add(InlineKeyboardButton('Добавить партнёра 😊', callback_data='add_partner'))
                klpar.add(InlineKeyboardButton('Назад 🔙', callback_data='my_profile'),
                          InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                            text="К сожалению вы пока не добавили партнёра 😔", reply_markup=klpar)
            else:
                klpar.add(InlineKeyboardButton('Обновить партнёра 🔄', callback_data='add_partner'))
                klpar.add(InlineKeyboardButton('Назад 🔙', callback_data='my_profile'),
                          InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                par = session.query(User).filter(User.phone_number == user.partner_phone_number).first()
                if par is None:
                    if user.pol == 'man':
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text=f"Партнёр пока не зарегистрирована 😢",
                                                    reply_markup=klpar)
                    else:
                        await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                    text=f"Партнёр пока не зарегистрирован 😢",
                                                    reply_markup=klpar)
                else:
                    await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                                text=f"Номер телефона: {par.phone_number}\nИмя: {beatufull_str(par.name)}",
                                                reply_markup=klpar)
        elif callback_query.data == 'buy_all':
            kl = InlineKeyboardMarkup(row_width=2)
            if user.buy_all == "N":
                kl.add(InlineKeyboardButton('Купить все 💳 (990 рублей)', callback_data='buy_alll'))
            kl.add(InlineKeyboardButton('Назад 🔙', callback_data='my_profile'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Купите весь функционал бота за 990 рублей', reply_markup=kl)
        elif callback_query.data == 'add_partner':
            user.state = 'add_partner'
            session.add(user)
            session.commit()
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        reply_markup=InlineKeyboardMarkup().add(
                                            InlineKeyboardButton('Главное меню 🏡', callback_data='home')),
                                        text='Напишите номер своего партнёра в одном из форматов:\n+79172665539\n89172665539')
        elif callback_query.data == 'change_name':
            user.state = 'write_name'
            session.add(user)
            session.commit()
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        reply_markup=InlineKeyboardMarkup().add(
                                            InlineKeyboardButton('Главное меню 🏡', callback_data='home')),
                                        text='Напишите своё имя')
        elif callback_query.data == 'free_game':
            fre_games = session.query(Free_game).all()
            kl = InlineKeyboardMarkup()
            for elem in fre_games:
                if elem.game_id > 3:
                    break
                kl.add(InlineKeyboardButton(f"{elem.game_name}", callback_data=f"free_game_{elem.game_id}"))
            for i in [1, 2, 7]:
                elem = session.query(Paid_game).filter(Paid_game.game_id == i).first()
                kl.add(InlineKeyboardButton(f"{elem.game_name}", callback_data=f"free_game_{elem.game_id + 100}"))
            kl.add(InlineKeyboardButton("Назад 🔙", callback_data='game'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Нажмите на понравившуюся игру и посмотрите описание 👀',
                                        reply_markup=kl)
        elif callback_query.data == 'top_up':
            kl = InlineKeyboardMarkup()
            co = 100
            ff = 50
            for i in range(10):
                if i != 0:
                    kl.add(InlineKeyboardButton(f'{co} sex-coin - {ff} рублей',
                                                callback_data=f'tt_{i}'))
                co += 100
                ff += 50
            kl.add(InlineKeyboardButton('Назад 🔙', callback_data='store'),
                   InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text='Выберите нужное количество sex-coin, курс 1 рубль = 2 sex-coin',
                                        reply_markup=kl)
        elif callback_query.data[0:len('tt_')] == 'tt_':
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text="Для того что бы попасть в главное меню, нажмите /start")
            t = int(callback_query.data.split('_')[1])
            await bot.send_invoice(
                tg_id,
                title="Покупка валюты",
                description=f"{(t + 1) * 50 * 2} sex-coin на баланс в AmateurBot",
                provider_token=payment_token,
                currency='rub',
                prices=[prices[t]],
                start_parameter=str(t),
                payload=str(tg_id) + f"_{(t + 1) * 50 * 2}")
        elif callback_query.data == 'buy_alll':
            await bot.edit_message_text(chat_id=tg_id, message_id=callback_query.message.message_id,
                                        text="Для того что бы попасть в главное меню, нажмите /start")
            await bot.send_invoice(
                tg_id,
                title="Покупка всего функционала",
                description=f"Покупка всех игр и поз в AmateurBot",
                provider_token=payment_token,
                currency='rub',
                prices=[PRICE_SUB],
                start_parameter=str(99),
                payload=str(tg_id) + f"_{99}")
        elif callback_query.data == 'my_promo':
            promo = session.query(Promocode).filter(Promocode.user_tg_id == tg_id).all()
            count = 1
            for elem in promo:
                await bot.send_message(chat_id=tg_id,
                                       text=f'{count}. **Промокод** на **{elem.value}**, действует **от {elem.minimum_price} рублей**, действует **до {elem.end_date}**\n```{elem.code}```',
                                       parse_mode=ParseMode.MARKDOWN)
                count += 1
            if count == 1:
                await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                text='К сожалению у вас пока нету промокодов 😔', show_alert=True)
            else:
                await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                kl = InlineKeyboardMarkup(row_width=2)
                kl.add(InlineKeyboardButton('Назад 🔙', callback_data='my_profile'),
                       InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                await bot.send_message(chat_id=tg_id, text='Это список всех ваших промокодов', reply_markup=kl)
        elif callback_query.data == 'smy_promo':
            promo = session.query(Promocode).filter(Promocode.user_tg_id == tg_id).all()
            count = 1
            for elem in promo:
                await bot.send_message(chat_id=tg_id,
                                       text=f'{count}. **Промокод** на **{elem.value}**, действует **от {elem.minimum_price} рублей**, действует **до {elem.end_date}**\n```{elem.code}```',
                                       parse_mode=ParseMode.MARKDOWN)
                count += 1
            if count == 1:
                await bot.answer_callback_query(callback_query_id=callback_query.id,
                                                text='К сожалению у вас пока нету промокодов 😔', show_alert=True)
            else:
                await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
                kl = InlineKeyboardMarkup(row_width=2)
                kl.add(InlineKeyboardButton('Назад 🔙', callback_data='spromo'),
                       InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                await bot.send_message(chat_id=tg_id, text='Это список всех ваших промокодов', reply_markup=kl)
        elif callback_query.data[0:len('__paid_game_9')] == '__paid_game_9':
            callback_query.data = callback_query.data[2:]
            paid_game_id = int(callback_query.data.split('_')[2])
            paid_game = session.query(Paid_game).filter(Paid_game.game_id == paid_game_id).first()
            buy = False
            if session.query(Purchased_game).filter(Purchased_game.game_id == paid_game_id).filter(
                    Purchased_game.user_id == tg_id).first() != None:
                buy = True
            kl = InlineKeyboardMarkup(row_width=2)
            b = callback_query.data.split('_')[3]
            t = callback_query.data.split('_')[4]
            if buy:
                kl.add(InlineKeyboardButton('Подробнее 🧐', url=str(paid_game.detail)),
                       InlineKeyboardButton('Играть 🚀', callback_data=f'play_paid_game_{paid_game_id}_{t}_{b}'))
            else:
                kl.add(InlineKeyboardButton('Подробнее 🧐', url=str(paid_game.detail)),
                       InlineKeyboardButton('Купить (100 sex-coin)',
                                            callback_data=f'buy_paid_game_{paid_game_id}_{t}_{b}'))
            if len(callback_query.data.split('_')) == 5:
                t = callback_query.data.split('_')[3]
                if callback_query.data.split('_')[4] == 'b':
                    kl.add(InlineKeyboardButton('Назад 🔙',
                                                callback_data=f'wpaid_game_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                elif callback_query.data.split('_')[4] == 'w':
                    kl.add(InlineKeyboardButton('Назад 🔙',
                                                callback_data='_paid_game'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
                else:
                    kl.add(InlineKeyboardButton('Назад 🔙',
                                                callback_data=f'wpaid_game_{t}_{b}'),
                           InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            else:
                kl.add(InlineKeyboardButton('Назад 🔙', callback_data='paid_game'),
                       InlineKeyboardButton('Главное меню 🏡', callback_data='home'))
            await bot.send_message(chat_id=tg_id,
                                   text=f'*{beatufull_str(paid_game.game_name)}*\n\n{paid_game.game_caption}',
                                   parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            await bot.delete_message(chat_id=tg_id, message_id=callback_query.message.message_id)
        elif callback_query.data == 'ras_yes':
            users = session.query(User).all()
            for elem in users:
                try:
                    await bot.send_message(chat_id=elem.user_tg_id, text=callback_query.message.text)
                except:
                    pass
    session.commit()
    session.close()


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    pmnt = message.successful_payment.to_python()
    pmnt = pmnt["invoice_payload"].split("_")
    # print(pmnt[0], pmnt[1])
    # pmnt[0] - tg_id pmnt[1] - что именно оплатил
    session = create_session()
    user = session.query(User).filter(User.user_tg_id == int(pmnt[0])).first()
    if int(pmnt[1]) != 99:
        user.balance += int(pmnt[1])
        session.add(user)
        session.commit()
        await bot.send_message(chat_id=message.chat.id,
                               text=f"Оплата прошла успешно!\n*{pmnt[1]} sex-coin* поступили на ваш баланс",
                               parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Главное меню 🏡', callback_data='home')))
    else:
        for i in range(11):
            paid_game_id = i + 1
            if paid_game_id == 6:
                if session.query(Purchased_game).filter(Purchased_game.user_id == user.user_tg_id).filter(
                        Purchased_game.game_id == 6).first() is None:
                    for i in range(20):
                        ne = For_paid_game_info_6()
                        ne.name = session.query(Paid_game_info_6).filter(Paid_game_info_6.id == i + 1).first().dop_info
                        ne.user_tg_id = int(message.chat.id)
                        ne.id_from_game = 6
                        ne.do = "No"
                        ne.id_from_game = 6
                        session.add(ne)
                        session.commit()
            new_paid_game = Purchased_game()
            new_paid_game.game_id = paid_game_id
            new_paid_game.user_id = int(user.user_tg_id)
            session.add(new_paid_game)
            session.commit()
        poses = session.query(Poses).all()
        for elem in poses:
            if session.query(Open_poses).filter(Open_poses.user_id == int(user.user_tg_id)).filter(
                    Open_poses.pos_id == elem.pos_id).first() is None:
                ne = Open_poses()
                ne.pos_id = elem.pos_id
                ne.name = elem.name
                ne.user_id = int(user.user_tg_id)
                ne.pos_level = elem.pos_lvl
                ne.see = "False"
                session.add(ne)
                session.commit()
        user.buy_all = 'Y'
        session.add(user)
        session.commit()
        await bot.send_message(chat_id=int(user.user_tg_id),
                               text='Оплата прошла успешно! Пользуйтесь всем что есть в боте',
                               reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton('Главное меню 🏡', callback_data='home')))
    session.commit()
    session.close()


async def hurryz():
    session = create_session()
    global day_pose_id
    global day_task_id
    day_pose_id = random.randint(1, 100)
    cur = random.randint(1, 3)
    if cur == 1:
        day_task_id = random.randint(1, 5)
    elif cur == 2:
        day_task_id = random.randint(11, 15)
    else:
        day_task_id = random.randint(21, 25)
    users = session.query(User).all()
    for i in users:
        i.zar_today = 0
        i.take_pose = 'False'
        i.podpiska = 'False'
        session.add(i)
        session.commit()
    get_promocodes()
    update_orders()
    session.commit()
    session.close()


async def scheduler():
    aioschedule.every().day.at('00:00').do(hurryz)
    while True:
        await asyncio.sleep(1)
        await aioschedule.run_pending()


async def on_startup(x):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    global_init("db.sqlite")
    # get_promocodes()
    # update_orders()
    start_polling(dp, on_startup=on_startup)
