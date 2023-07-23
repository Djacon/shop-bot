import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('token.json', SCOPES)

FILE_URL = 'https://drive.google.com/file/d/'
service = build('drive', 'v3', credentials=creds)

request_body = {
    'role': 'reader',
    'type': 'anyone'
}


def upload_photo(src):
    file_metadata = {
        'name': src,
        'parents': ['1d160L6ZDKAP3H5NCRk2jQwZYbgTQZvAG']
    }
    media = MediaFileUpload(f'photos/{src}')
    file_id = service.files().create(body=file_metadata,
                                     media_body=media,
                                     fields='id').execute()['id']

    service.permissions().create(
        fileId=file_id,
        body=request_body
    ).execute()

    public_url = service.files().get(
        fileId=file_id,
        fields='webViewLink'
    ).execute()

    return public_url


try:
    upload_photo(src)
except HttpError as e:
    print(f'Error: {e}')
