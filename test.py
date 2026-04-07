import asyncio
from telethon import TelegramClient
import socks

proxy = (
    socks.SOCKS5,
    "127.0.0.1",
    9050
)

client = TelegramClient(
    "userbot",
    31364388,
    '6e7c15d00a1c02806d509d0b619e3d8f',
    proxy=proxy,
    use_ipv6=False
)

async def main():
    await client.start()
    me = await client.get_me()
    print("Connected as:", me.first_name)

asyncio.run(main())