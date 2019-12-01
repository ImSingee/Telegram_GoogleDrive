from telethon import TelegramClient
from telethon.events.newmessage import NewMessage

import db
from utils.status import set_status, clear_status, get_status, check_status
from utils.folders import set_folder_alias, get_folder_id, delete_folder_alias


def set_filter(event: NewMessage.Event):
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


def unset_filter(event: NewMessage.Event):
    if event.message.message.startswith('/unset_folder_alias'):
        return True

    if event.message.message.startswith('/cancel'):
        return False

    if check_status(event.message.from_id, 'unsetting-folder-alias'):
        event.status_match = 'unsetting-folder-alias'
        return True

    return False


def query_filter(event: NewMessage.Event):
    if event.message.message.startswith('/query_folder_alias'):
        return True

    if event.message.message.startswith('/cancel'):
        return False

    if check_status(event.message.from_id, 'querying-folder-alias'):
        event.status_match = 'querying-folder-alias'
        return True

    return False


async def set_handler(event: NewMessage.Event):
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


async def unset_handler(event: NewMessage.Event):
    print('unset_default_folder_handler', event)

    from_user_id = event.message.from_id

    if event.message.message.startswith('/unset_folder_alias'):
        set_status(from_user_id, 'unsetting-folder-alias')
        # TODO - 一键取消全部
        await event.respond(
            '请输入要取消设定的文件夹别名，取消当前操作请输入 /cancel'
        )
    elif event.status_match == 'unsetting-folder-alias':
        key = event.message.message.strip()
        delete_folder_alias(from_user_id, key)
        clear_status(from_user_id)
        await event.respond(
            '删除别名完成。'
        )


async def query_handler(event: NewMessage.Event):
    print('query_default_folder_handler', event)

    from_user_id = event.message.from_id

    if event.message.message.startswith('/query_folder_alias'):
        set_status(from_user_id, 'querying-folder-alias')
        # TODO - 查询全部
        await event.respond(
            '请输入要查询的文件夹别名，取消当前操作请输入 /cancel'
        )
    elif event.status_match == 'querying-folder-alias':
        key = event.message.message.strip()
        value = get_folder_id(from_user_id, key)

        clear_status(from_user_id)
        if value == key:
            await event.reply(
                '未设定该别名。'
            )
        else:
            await event.respond(
                f'别名`{key}`对应的文件夹 ID 为`{value}`'
            )


def register(client: TelegramClient):
    client.on(NewMessage(func=set_filter))(set_handler)
    client.on(NewMessage(func=unset_filter))(unset_handler)
    client.on(NewMessage(func=query_filter))(query_handler)
