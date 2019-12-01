import os
import db
from telethon import TelegramClient
from telethon.events.newmessage import NewMessage
from utils.authenticate import get_drive


async def rename_handler(event: NewMessage.Event):
    print('rename_handler', event)
    reply_to_msg_id = event.message.reply_to_msg_id

    if not reply_to_msg_id:
        # TODO - 引导选择文件
        await event.reply('请【回复】相应消息以重命名文件')
        return

    file_id = db.get('message-info-google-drive-file-id', f'{event.chat.id}.{reply_to_msg_id}')
    print(f'{event.chat.id}.{reply_to_msg_id}')
    if not file_id:
        await event.reply('请回复正确的消息以重命名文件')
        return

    from_user_id = event.message.from_id
    new_name_groups = event.message.message.strip().split(maxsplit=1)
    if len(new_name_groups) <= 1:
        await event.reply('请输入新名称')
        return

    new_name = new_name_groups[1].strip()

    drive = get_drive(from_user_id)
    file = drive.CreateFile({'id': file_id})
    try:
        file.FetchMetadata(fields='title')

        if new_name[-1] == '.':
            file['title'] = new_name[:-1]
        elif new_name.find('.') == -1:
            file['title'] = new_name + os.path.splitext(file['title'])[-1]
        else:
            file['title'] = new_name
        file.Upload()
    except:
        await event.reply('文件不存在或您无权操作')
        return

    await event.reply(f"重命名成功，新文件名为 [{file['title']}]({file['alternateLink']})")


def register(client: TelegramClient):
    client.on(NewMessage(pattern='/rename'))(rename_handler)
