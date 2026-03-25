from pyrogram import Client, filters
from pyrogram.types import Message

from app.db.database import AsyncSessionLocal
from app.db.crud import (
    get_or_create_user,
    create_subscription,
    get_subscriptions_by_user,
    get_subscription,
    delete_subscription,
)


def register_handlers(bot: Client):

    @bot.on_message(filters.command("start") & filters.private)
    async def cmd_start(client: Client, message: Message):
        async with AsyncSessionLocal() as session:
            await get_or_create_user(session, message.from_user.id, message.from_user.username)
            await session.commit()

        await message.reply(
            "Привет! Я агрегатор Telegram-сообщений.\n\n"
            "Команды:\n"
            "/subscribe <запрос> — подписаться на тему\n"
            "/list — показать мои подписки\n"
            "/delete <id> — удалить подписку"
        )

    @bot.on_message(filters.command("subscribe") & filters.private)
    async def cmd_subscribe(client: Client, message: Message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Укажи запрос. Пример:\n/subscribe упоминание дедлайнов")
            return

        prompt = args[1].strip()
        async with AsyncSessionLocal() as session:
            await get_or_create_user(session, message.from_user.id, message.from_user.username)
            sub = await create_subscription(session, message.from_user.id, prompt)
            await session.commit()

        await message.reply(f"Подписка #{sub.id} создана:\n_{prompt}_", parse_mode="markdown")

    @bot.on_message(filters.command("list") & filters.private)
    async def cmd_list(client: Client, message: Message):
        async with AsyncSessionLocal() as session:
            subs = await get_subscriptions_by_user(session, message.from_user.id)

        if not subs:
            await message.reply("У тебя пока нет подписок. Используй /subscribe <запрос>")
            return

        lines = [f"#{s.id}: _{s.prompt}_" for s in subs]
        await message.reply("Твои подписки:\n" + "\n".join(lines), parse_mode="markdown")

    @bot.on_message(filters.command("delete") & filters.private)
    async def cmd_delete(client: Client, message: Message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2 or not args[1].isdigit():
            await message.reply("Укажи ID подписки. Пример:\n/delete 3")
            return

        sub_id = int(args[1])
        async with AsyncSessionLocal() as session:
            sub = await get_subscription(session, sub_id, message.from_user.id)
            if not sub:
                await message.reply("Подписка не найдена.")
                return
            await delete_subscription(session, sub_id)
            await session.commit()

        await message.reply(f"Подписка #{sub_id} удалена.")