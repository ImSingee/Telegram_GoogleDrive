import db
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import Credentials


def is_authenticated(user_id):
    # 未授权：返回 False
    # 已授权：返回 credentials
    return db.get('gauth-credentials', user_id, default=False)


def save_credential(user_id, credential):
    db.set('gauth-credentials', user_id, credential)


def get_gauth(user_id):
    credentials = is_authenticated(user_id)
    if not credentials:
        return None
    gauth = GoogleAuth()
    gauth.credentials = Credentials.new_from_json(credentials)

    return gauth


def get_drive(user_id):
    gauth = get_gauth(user_id)
    if not gauth:
        return None
    drive = GoogleDrive(gauth)
    return drive
