from telethon import TelegramClient
from telethon.events.newmessage import NewMessage

from utils.status import clear_status


async def cancel_handler(event: NewMessage.Event):
    print('cancel_handler', event)
    from_user_id = event.message.from_id
    clear_status(from_user_id)
    await event.reply('取消当前操作成功')


def register(client: TelegramClient):
    client.on(NewMessage(pattern='/cancel'))(cancel_handler)
