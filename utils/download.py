import time
import os
from configparser import ConfigParser
from telethon import TelegramClient
from telethon.tl.types import Message

config_parser = ConfigParser()
config_parser.read('config.ini')

download_cache_dir = config_parser.get('DOWNLOAD', 'cache_dir')


async def from_telegram(client: TelegramClient, message: Message, sent_message: Message = None):
    last_call = 0

    async def callback(received_bytes, total):
        nonlocal last_call
        now = time.time()
        if now > last_call + 2 or received_bytes == total:
            last_call = now
            await sent_message.edit('文件正在从 Telegram 服务器下载\n\n' +
                                    f'{round(received_bytes / 1024 / 1024, 2)}M / {round(total / 1024 / 1024, 2)}M '
                                    f'({round(received_bytes / total * 100, 2)}%)')

    download_to_dir = os.path.join(download_cache_dir, str(message.from_id), str(int(time.time())))

    if sent_message:
        downloaded_media = await client.download_media(message, download_to_dir, progress_callback=callback)
    else:
        downloaded_media = await client.download_media(message, download_to_dir)

    return downloaded_media
