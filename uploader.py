from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from keyboards import ITEM_TYPE


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_authorized_user_file('token.json', SCOPES)

SHEET_ID = '1FLOEheaUXY1TUPc8_J4DBuTxeD_8ZSIqfnuuaWset-I'

service = build('sheets', 'v4', credentials=creds)

sheets = service.spreadsheets()


def get_orders_user_count_info():
    header = sheets.values().get(spreadsheetId=SHEET_ID,
                                 range="Sheet1!A3:T3").execute()['values'][0]
    return 3 + int(header[0]), 3 + int(header[12])


def get_order_query(username, order):
    deliv, cost, src, size = (order['deliv'], str(order['cost']), order['src'],
                              str(order['size']))
    type = ITEM_TYPE[order['type']]
    photo = f"=HYPERLINK(\"{order['photo']}\", \"Ссылка на фото\")"

    query = ['Принят']
    query.extend([username, type, deliv, cost, src, size, photo])
    return query


def upload_orders(username, orders, row):
    values = [get_order_query(username, order) for order in orders]
    row_end = row + len(values) - 1
    sheets.values().update(spreadsheetId=SHEET_ID,
                           range=f'Sheet1!C{row}:J{row_end}',
                           valueInputOption='USER_ENTERED',
                           body={'values': values}).execute()


def upload_user(userinfo, row):
    query = ['Принят']
    query.extend(list(map(str, userinfo)))
    sheets.values().update(spreadsheetId=SHEET_ID,
                           range=f'Sheet1!O{row}:S{row}',
                           valueInputOption='USER_ENTERED',
                           body={'values': [query]}).execute()
