from telethon import TelegramClient
from telethon.events.newmessage import NewMessage

import db
from utils.status import set_status, clear_status, get_status
from utils.folders import set_folder_alias, get_folder_id


def filter(event: NewMessage.Event):
    if event.message.message.startswith('/set_folder_alias'):
        return True

    if event.message.message.startswith('/cancel'):
        return False

    status = get_status(event.message.from_id)
    if status == 'setting-folder-alias-key':
        event.status_match = 'setting-folder-alias-key'
        return True
    elif status == 'setting-folder-alias-value':
        event.status_match = 'setting-folder-alias-value'
        return True

    return False


async def handler(event: NewMessage.Event):
    print('set_default_folder_handler', event)

    from_user_id = event.message.from_id

    if event.message.message.startswith('/set_folder_alias'):
        set_status(from_user_id, 'setting-folder-alias-key')
        await event.respond(
            '请输入要设定的文件夹别名，取消当前操作请输入 /cancel'
        )
    elif event.status_match == 'setting-folder-alias-key':
        key = event.message.message.strip()
        if len(key.split()) != 1:
            await event.respond(
                '文件夹别名不能含有空格，请重新输入；取消当前操作请输入 /cancel'
            )
            return

        set_status(from_user_id, 'setting-folder-alias-value')
        db.set('folder-alias-setting-key', from_user_id, key)
        await event.respond(
            f'请输入别名`{key}`对应的文件夹 ID（也可以是其他别名），取消当前操作请输入 /cancel'
        )
    elif event.status_match == 'setting-folder-alias-value':
        key = db.get('folder-alias-setting-key', from_user_id)
        if not key:
            clear_status(from_user_id)
            await event.respond(
                '超时，请重试。'
            )
            return

        value = get_folder_id(from_user_id, event.message.message.strip())
        set_folder_alias(from_user_id, key, value)
        clear_status(from_user_id)
        await event.respond(
            '设定完成。'
        )


def register(client: TelegramClient):
    client.on(NewMessage(func=filter))(handler)
