from telethon import TelegramClient
from telethon.events.newmessage import NewMessage
from utils.status import check_status
from utils.authenticate import is_authenticated
from utils.download import from_telegram as download_from_telegram
from utils.upload import to_google_drive as upload_to_google_drive


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
        await upload_to_google_drive(from_user_id, downloaded_media, sent_message)
    else:
        await event.reply(
            '纯文本信息不会被保存至 Google Drive'
        )
        return


def register(client: TelegramClient):
    client.on(NewMessage(func=filter))(handler)
