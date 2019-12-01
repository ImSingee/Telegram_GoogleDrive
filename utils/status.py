import db


def get_status(user_id):
    return db.get('user-status', user_id)


def set_status(user_id, status):
    db.set('user-status', user_id, status)


def clear_status(user_id):
    db.delete('user-status', user_id)


def check_status(user_id, status=None):
    return db.get('user-status', user_id) == status
