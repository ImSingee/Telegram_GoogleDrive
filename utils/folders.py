import db


def get_default_folders(user_id):
    default_folders = db.get('default-folders', user_id)
    if default_folders:
        return default_folders.split()
    else:
        return []


def set_default_folders(user_id, folders):
    db.set('default-folders', user_id, ' '.join(folders))
