from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, Subscription, Message

async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)

async def get_or_create_user(session: AsyncSession, user_id: int, username: str | None) -> User:
    user = await get_user(session, user_id)
    if not user:
        user = User(id=user_id, username=username)
        session.add(user)
        await session.flush()
    return user


async def create_subscription(session: AsyncSession, user_id: int, prompt: str) -> Subscription:
    sub = Subscription(user_id=user_id, prompt=prompt)
    session.add(sub)
    await session.flush()
    await session.refresh(sub)
    return sub

async def get_subscriptions_by_user(session: AsyncSession, user_id: int) -> list[Subscription]:
    result = await session.execute(
        select(Subscription).where(Subscription.user_id == user_id)
    )
    return result.scalars().all()

async def get_subscription(session: AsyncSession, sub_id: int, user_id: int) -> Subscription | None:
    result = await session.execute(
        select(Subscription).where(
            Subscription.id == sub_id,
            Subscription.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()

async def delete_subscription(session: AsyncSession, sub_id: int) -> None:
    await session.execute(delete(Subscription).where(Subscription.id == sub_id))

async def get_all_subscriptions(session: AsyncSession) -> list[Subscription]:
    result = await session.execute(select(Subscription))
    return result.scalars().all()


async def create_message(
    session: AsyncSession,
    chat_id: int,
    chat_title: str | None,
    message_id: int,
    sender_id: int | None,
    text: str,
    date,
    link: str | None,
) -> Message:
    msg = Message(
        chat_id=chat_id,
        chat_title=chat_title,
        message_id=message_id,
        sender_id=sender_id,
        text=text,
        date=date,
        link=link,
    )
    session.add(msg)
    await session.flush()
    return msg