from configparser import ConfigParser
from telethon import TelegramClient, events
from handlers.auth_handler import register as register_auth_handler
from handlers.cancel_handler import register as register_cancel_handler

config_parser = ConfigParser()
config_parser.read('config.ini')

api_id = config_parser.get('CORE', 'api_id')
api_hash = config_parser.get('CORE', 'api_hash')
bot_token = config_parser.get('CORE', 'bot_token')

client = TelegramClient('tg_gd', api_id, api_hash)

register_auth_handler(client)
register_cancel_handler(client)


@client.on(events.NewMessage)
async def handler(event):
    # TODO: [DEBUG] delete this
    print('[DEBUG] NewMessage:', event)


@client.on(events.MessageDeleted)
async def handler(event):
    # TODO: delete means cancel
    pass


if __name__ == '__main__':
    print('Starting...')
    client.start(bot_token=bot_token)
    print('Started.')
    client.run_until_disconnected()
