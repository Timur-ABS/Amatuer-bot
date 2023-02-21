from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from db import create_session, Order, User, Promocode

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = 'id'
SAMPLE_RANGE_NAME = ['Промокод (100 руб)!A3:F1000', 'Промокод (200 руб)!A3:F1000', 'Промокод (300 руб)!A3:F1000',
                     'Промокод (400 руб)!A3:F1000', 'Промокод (500 руб)!A3:F1000', 'Промокод (600 руб)!A3:F1000',
                     'Промокод (700 руб)!A3:F1000']


def get_promocodes():
    key = "AIzaSyAzJcL89h9b6YQJVxFDvDQa5vFiJdD_UjU"
    try:
        for i in range(7):
            service = build('sheets', 'v4', developerKey=key)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME[i]).execute()
            values = result.get('values', [])
            if not values:
                print('No data found.')
                return
            for row in values:
                if len(row[0]) == 0:
                    continue
                code = row[0]
                value = (i + 1) * 100
                minimum_price = int(row[2])
                until = row[4]
                status = 1 if row[5] == '1' else 0
                if status:
                    add_to_db(code, value, minimum_price, until)
    except HttpError as err:
        print(err)


def add_to_db(code, value, minimum_price, until):
    session = create_session()
    promocode = session.query(Promocode).filter(Promocode.code == code).first()
    if not promocode:
        new_promocode = Promocode(code=code, value=value, price=value, minimum_price=minimum_price, end_date=until)
        session.add(new_promocode)
        session.commit()
    session.close()


def buy_promocode(user_id, price):
    session = create_session()
    user = session.query(User).filter(user_id == User.user_tg_id).first()
    if user.balance < price:
        return "У вас не хватает sex-коинов!"
    promocodes = session.query(Promocode).filter(Promocode.price == price).filter(Promocode.user_tg_id == None).all()
    sp = []
    for elem in promocodes:
        # if datetime.datetime.strptime(elem.end_date, '%d.%m.%Y').date() > datetime.datetime.now().date():
        sp.append(elem)
    if len(sp) >= 1:
        promocode = sp[0]
    else:
        promocode = None
    if not promocode:
        return "К сожалению, на данный момент у нас нет активных промокодов!"
    user.balance -= price
    promocode.user_tg_id = user.user_tg_id
    message = f"Держите промокод на скидку *{promocode.value}* при покупке от {promocode.minimum_price}!\nОн действует до *{promocode.end_date}*.\n```{promocode.code}```"
    session.add(user)
    session.add(promocode)
    session.commit()
    session.close()
    return message
