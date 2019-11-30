from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.events.newmessage import NewMessage
from pydrive.auth import GoogleAuth

from utils.authenticate import save_credential

gauth = GoogleAuth()
auth_url = gauth.GetAuthUrl()


def auth_init_filter(message: str):
    return message.startswith('/authenticate')


async def auth_init_handler(event: NewMessage.Event):
    print('auth_init_handler', event)

    message = event.message
    from_user_id = message.from_id

    groups = message.message.split()
    if len(groups) >= 2:
        # 授权码
        code = groups[1]
        try:
            gauth.Auth(code)
        except Exception as e:
            await message.reply(
                '授权码无效：' + str(e)
            )
            return

        save_credential(from_user_id, gauth.credentials.to_json())
        await message.reply(
            '授权成功！'  # TODO：使用指引
        )

    else:
        # 要求授权
        await message.reply(
            '请点击以下链接并登陆授权，授权完成后发送 `/authenticate ` 后接生成的授权码\n\n' + auth_url
        )


def register(client: TelegramClient):
    client.on(NewMessage(pattern=auth_init_filter))(auth_init_handler)
