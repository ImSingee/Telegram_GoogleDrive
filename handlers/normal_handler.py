from telethon import TelegramClient
from telethon.events.newmessage import NewMessage

from utils.status import set_status, clear_status, check_status
from utils.authenticate import is_authenticated, get_drive
from utils.download import from_telegram as download_from_telegram
from utils.folders import get_default_folders


def filter(event: NewMessage.Event):
    if event.message.message.startswith('/'):
        return False

    if check_status(event.message.from_id):
        return True

    return False


async def handler(event: NewMessage.Event):
    print('normal_handler', event)

    from_user_id = event.message.from_id
    media = event.message.media

    if not is_authenticated(from_user_id):
        await event.reply(
            '请发送 /authenticate 授权 Google Drive 后重试'
        )
        return

    if media:
        sent_message = await event.reply(
            '文件已收到，已经加入处理队列，请耐心等待。'
        )

        downloaded_media = await download_from_telegram(event.client, event.message, sent_message)
        await sent_message.edit('下载完成，即将上传至 Google Drive')
        print(downloaded_media)
        drive = get_drive(from_user_id)
        file = drive.CreateFile()
        file['title'] = downloaded_media.split('/')[-1]
        folders = get_default_folders(from_user_id)
        if folders:
            file['parents'] = [{'id': x} for x in folders]
        file.SetContentFile(downloaded_media)
        await sent_message.edit('正在上传至 Google Drive。通常情况下 1GB 文件需要 1min 左右，如果在超出预估时间 5 倍后您依然未收到成功或失败的提醒请联系管理员。')
        try:
            file.Upload()
        except Exception as e:
            # TODO: 允许重试
            await sent_message.edit('上传失败。\n\n' + str(e))
            return

        if folders:
            await sent_message.edit(f"上传完成，文件已经存储至您设置的默认文件夹。\n\n[点此查看此文件]({file['alternateLink']})")
        else:
            await sent_message.edit(f"上传完成，文件已经存储至您网盘的根目录。\n\n[点此查看此文件]({file['alternateLink']})")
        # TODO: 删除上传完成后的文件
        # TODO: 重命名
    else:
        await event.reply(
            '纯文本信息不会被保存至 Google Drive'
        )
        return


def register(client: TelegramClient):
    client.on(NewMessage(func=filter))(handler)
