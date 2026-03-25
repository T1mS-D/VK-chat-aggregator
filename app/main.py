import asyncio
from pyrogram import Client

from app.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN
from app.db.database import init_db
from app.handlers.user_handlers import register_handlers
from app.services.telegram_listener import user_client

bot_client = Client(
    "bot_session",
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
    bot_token=TELEGRAM_BOT_TOKEN,
)


async def main():
    await init_db()
    print("[DB] Tables ready.")

    register_handlers(bot_client)

    async with bot_client, user_client:
        print("[BOT] Bot started.")
        print("[USER] User client started. Listening to chats...")
        await asyncio.gather(
            bot_client.idle(),
            user_client.idle(),
        )


if __name__ == "__main__":
    asyncio.run(main())