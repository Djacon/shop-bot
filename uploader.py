from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# from google_auth_oauthlib.flow import InstalledAppFlow

from keyboards import ITEM_TYPE


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# flow = InstalledAppFlow.from_client_secrets_file('secret.json', SCOPES)
# creds = flow.run_local_server(port=0)

# with open('token.json', 'w') as token:
#     token.write(creds.to_json())

SHEET_ID = '1FLOEheaUXY1TUPc8_J4DBuTxeD_8ZSIqfnuuaWset-I'

service = build('sheets', 'v4', credentials=creds)

sheets = service.spreadsheets()


def get_orders_user_count_info():
    header = sheets.values().get(spreadsheetId=SHEET_ID,
                                 range="Sheet1!A3:T3").execute()['values'][0]
    return 3 + int(header[0]), 3 + int(header[12])


def get_unnecessary_users_id():
    status_id = sheets.values().get(spreadsheetId=SHEET_ID,
                                    range=f"Sheet1!O3:P"
                                    ).execute()['values']
    return [i for i, s in status_id if s == 'Отправлено']


def clear_unnecessary_orders_and_get_row_id():
    users = sheets.values().get(spreadsheetId=SHEET_ID,
                                range=f"Sheet1!O3:U",
                                valueRenderOption="FORMULA",
                                ).execute().get('values', [])
    sent_ids = []
    p = 0
    for i in range(len(users)):
        if users[i][1] != 'Отправлено':
            users[p] = users[i]
            p += 1
        else:
            sent_ids.append(users[i][0])

    if not len(users):
        return 1
    elif p == len(users):
        return users[-1][0] + 1

    if not p:
        row_id = 1
    else:
        row_id = users[p-1][0] + 1

    nan = [''] * 7
    for i in range(p, len(users)):
        users[i] = nan

    sheets.values().update(spreadsheetId=SHEET_ID,
                           range=f'Sheet1!O3:U',
                           valueInputOption='USER_ENTERED',
                           body={'values': users}).execute()

    orders = sheets.values().get(spreadsheetId=SHEET_ID,
                                 range=f"Sheet1!C3:K",
                                 valueRenderOption="FORMULA",
                                 ).execute().get('values', [])
    p = 0
    for i in range(len(orders)):
        if orders[i][0] not in sent_ids:
            orders[p] = orders[i]
            p += 1

    nan = [''] * 9
    for i in range(p, len(orders)):
        orders[i] = nan

    sheets.values().update(spreadsheetId=SHEET_ID,
                           range=f'Sheet1!C3:K',
                           valueInputOption='USER_ENTERED',
                           body={'values': orders}).execute()
    return row_id


def get_order_query(orderid, username, order):
    deliv, cost, src, size = (order['deliv'], str(order['cost']), order['src'],
                              str(order['size']))
    type = ITEM_TYPE[order['type']]
    photo = f"=HYPERLINK(\"{order['photo']}\", \"Ссылка на фото\")"

    query = [orderid, 'Принят']
    query.extend([username, type, deliv, cost, src, size, photo])
    return query


def upload_orders(orderid, username, orders, row):
    values = [get_order_query(orderid, username, order) for order in orders]
    row_end = row + len(values) - 1
    sheets.values().update(spreadsheetId=SHEET_ID,
                           range=f'Sheet1!C{row}:K{row_end}',
                           valueInputOption='USER_ENTERED',
                           body={'values': values}).execute()


def upload_user(row_id, userinfo, row):
    query = [row_id, 'Принят']
    query.extend(list(map(str, userinfo)))
    query[-1] = f"=HYPERLINK(\"{query[-1]}\", \"Ссылка на чек\")"
    sheets.values().update(spreadsheetId=SHEET_ID,
                           range=f'Sheet1!O{row}:U{row}',
                           valueInputOption='USER_ENTERED',
                           body={'values': [query]}).execute()
