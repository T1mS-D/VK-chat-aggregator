from pyrogram import Client, filters
from pyrogram.types import Message as PyroMessage

from app.config import TELEGRAM_API_ID, TELEGRAM_API_HASH
from app.db.database import AsyncSessionLocal
from app.db.crud import create_message, get_all_subscriptions
from app.services.ai_search import is_relevant

user_client = Client(
    "user_session",
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
)


def _build_link(chat_id: int, chat_username: str | None, message_id: int) -> str:
    if chat_username:
        return f"https://t.me/{chat_username}/{message_id}"
    internal_id = str(chat_id).replace("-100", "")
    return f"https://t.me/c/{internal_id}/{message_id}"


@user_client.on_message(filters.group | filters.channel & filters.text)
async def on_new_message(client: Client, message: PyroMessage):
    if not message.text:
        return

    chat = message.chat
    link = _build_link(chat.id, chat.username, message.id)

    async with AsyncSessionLocal() as session:
        await create_message(
            session,
            chat_id=chat.id,
            chat_title=chat.title,
            message_id=message.id,
            sender_id=message.from_user.id if message.from_user else None,
            text=message.text,
            date=message.date,
            link=link,
        )

        subscriptions = await get_all_subscriptions(session)
        await session.commit()

    for sub in subscriptions:
        try:
            matched = await is_relevant(message.text, sub.prompt)
        except Exception as e:
            print(f"[AI] Error checking sub {sub.id}: {e}")
            continue

        if matched:
            from app.main import bot_client
            try:
                await bot_client.send_message(
                    sub.user_id,
                    f"🔔 *Новое совпадение по вашему запросу:*\n"
                    f"_{sub.prompt}_\n\n"
                    f"💬 Чат: *{chat.title or chat.id}*\n"
                    f"📝 {message.text[:300]}\n\n"
                    f"🔗 [Открыть сообщение]({link})",
                    parse_mode="markdown",
                )
            except Exception as e:
                print(f"[BOT] Failed to notify user {sub.user_id}: {e}")