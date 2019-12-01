from telethon import TelegramClient
from telethon.events.newmessage import NewMessage

from utils.status import set_status, clear_status, check_status
from utils.authenticate import is_authenticated, get_drive
from utils.folders import set_default_folders, get_folder_id


def filter(event: NewMessage.Event):
    if event.message.message.startswith('/set_default_folder'):
        return True

    if event.message.message.startswith('/cancel'):
        return False

    if check_status(event.message.from_id, 'setting-default-folder'):
        event.status_match = 'setting-default-folder'
        return True

    return False


async def handler(event: NewMessage.Event):
    print('set_default_folder_handler', event)

    from_user_id = event.message.from_id

    if not event.message.message.startswith('/set_default_folder'):
        # 提供新文件夹名
        folder_ids = event.message.message.strip().split()
        folder_infos = []

        if len(folder_ids) > 5:
            await event.reply(
                '最多可以设定 5 个默认文件夹，请重试'
            )
            return

        drive = get_drive(from_user_id)
        if not drive:
            await event.reply(
                '授权过期或被取消，请发送 /authenticate 授权 Google Drive 后重试'
            )
            clear_status(from_user_id)
            return

        folder_ids = [get_folder_id(from_user_id, folder_id) for folder_id in folder_ids]
        for folder_id in folder_ids:
            try:
                folder = drive.CreateFile({'id': folder_id})
            except:
                await event.reply(
                    '授权过期或被取消，请发送 /authenticate 授权 Google Drive 后重试'
                )
                clear_status(from_user_id)
                return

            try:
                folder_infos.append({'id': folder_id, 'title': folder['title'], 'url': folder['alternateLink']})
            except:
                await event.reply(
                    '文件夹' + folder_id + '不存在，请重试\n\n' + '如需取消当前操作请发送 /cancel'
                )
                return

        await event.reply(
            '设定默认文件夹成功！\n\n' + '\n'.join([f"[{x['title']}]({x['url']})" for x in folder_infos])
        )

        set_default_folders(from_user_id, folder_ids)
        clear_status(from_user_id)

    else:
        # 设定新文件夹
        if is_authenticated(from_user_id):
            await event.reply(
                '请输入文件夹 ID，多个文件夹请用空格分隔'
            )

            set_status(from_user_id, 'setting-default-folder')
        else:
            await event.reply(
                '请发送 /authenticate 授权 Google Drive 后重试'
            )


def register(client: TelegramClient):
    client.on(NewMessage(func=filter))(handler)
