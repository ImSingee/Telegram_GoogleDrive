import db


def get_default_folders(user_id):
    default_folders = db.get('default-folders', user_id)
    if default_folders:
        return default_folders.split()
    else:
        return []


def clear_default_folders(user_id):
    db.delete('default-folders', user_id)


def set_default_folders(user_id, folders):
    db.set('default-folders', user_id, ' '.join(folders))


def get_folder_id(user_id, folder_alias):
    return db.get('folder-alias', f'{user_id}.{folder_alias.lower()}', default=folder_alias)


def set_folder_alias(user_id, folder_alias, folder_id):
    folder_alias = str(folder_alias).lower()
    db.set('folder-alias', f'{user_id}.{folder_alias}', folder_id)


def delete_folder_alias(user_id, folder_alias):
    folder_alias = str(folder_alias).lower()
    db.delete('folder-alias', f'{user_id}.{folder_alias}')
