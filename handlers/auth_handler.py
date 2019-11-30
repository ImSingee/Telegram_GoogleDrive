from telethon import TelegramClient
from telethon.events.newmessage import NewMessage
from pydrive.auth import GoogleAuth

from utils.status import set_status, clear_status, check_status
from utils.authenticate import is_authenticated, save_credential

gauth = GoogleAuth()
auth_url = gauth.GetAuthUrl()


def auth_init_filter(event: NewMessage.Event):
    if event.message.message.startswith('/authenticate'):
        return True

    if event.message.message.startswith('/cancel'):
        return False

    if check_status(event.message.from_id, 'authenticating'):
        event.status_match = 'authenticating'
        return True

    return False


async def auth_init_handler(event: NewMessage.Event):
    print('auth_init_handler', event)

    from_user_id = event.message.from_id

    if not event.message.message.startswith('/authenticate'):
        # 授权码
        code = event.message.message.strip()
        try:
            gauth.Auth(code)
        except Exception as e:
            await event.reply(
                '授权码无效：' + str(e) + '\n\n如需取消当前操作请发送 /cancel'
            )
            return

        save_credential(from_user_id, gauth.credentials.to_json())
        await event.reply(
            '授权成功！'  # TODO：使用指引
        )

        clear_status(from_user_id)

    else:
        # 要求授权
        if is_authenticated(from_user_id):
            await event.reply(
                '您已经授权，如需重新授权'
                '请点击以下链接并登录以再次授权，授权完成后发送生成的授权码\n\n' + auth_url
            )
        else:
            await event.reply(
                '请点击以下链接并登录授权，授权完成后发送生成的授权码\n\n' + auth_url
            )

        set_status(from_user_id, 'authenticating')


def register(client: TelegramClient):
    client.on(NewMessage(func=auth_init_filter))(auth_init_handler)
