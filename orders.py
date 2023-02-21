from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from db import create_session, Order, User

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = 'id'
SAMPLE_RANGE_NAME = 'name'


def get_orders_from_spreadsheet():
    key = "AIzaSyAzJcL89h9b6YQJVxFDvDQa5vFiJdD_UjU"
    try:
        service = build('sheets', 'v4', developerKey=key)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
            return
        orders = []
        for row in values:
            status = row[0]
            order_id = int(row[3])
            coins = int(row[7].split(",")[0].replace("\xa0", ""))
            coins = coins // 10 + (1 if coins % 10 != 0 else 0)
            orders.append([order_id, status, coins])
        return orders
    except HttpError as err:
        print(err)


def update_orders():
    loaded_orders = get_orders_from_spreadsheet()
    session = create_session()
    for loaded_order in loaded_orders:
        if not session.query(Order).filter(Order.order_id == loaded_order[0]).first() and loaded_order[1] == "К выводу":
            new_order = Order(order_id=loaded_order[0], coins=loaded_order[2])
            session.add(new_order)
    session.commit()
    session.close()


def get_coins_from_order(order_id, user_tg_id):
    session = create_session()
    order = session.query(Order).filter(Order.order_id == order_id).first()
    if order is None:
        return "Мы не нашли такой номер заказа. Проверьте, правильно ли вы ввели номер."
    elif order.user_tg_id == user_tg_id:
        return "Вы уже получили коины за этот заказ!"
    elif order.user_tg_id is not None:
        return "Коины за этот заказ получил другой пользователь. Проверьте, правильно ли вы ввели номер. Если вы уверены, что " \
               "это ваш заказ, то обратитесь в поддержку."
    else:
        user = session.query(User).filter(User.user_tg_id == user_tg_id).first()
        order.user_tg_id = user.user_tg_id
        user.balance += order.coins
        coins = order.coins
        session.commit()
        session.close()
        return f"Вам было начислено {coins} коинов!"