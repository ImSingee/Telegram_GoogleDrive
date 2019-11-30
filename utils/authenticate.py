import db


def is_authenticated(user_id):
    # 未授权：返回 False
    # 已授权：返回 credentials
    return db.get('gauth-credentials', user_id, default=False)


def save_credential(user_id, credential):
    db.set('gauth-credentials', user_id, credential)
