__all__ = (
    "save_user",
    "get_user",
    "get_all_users",
    "get_user_by_username",
    "get_adm_count",
)

from sqlalchemy import select, Result, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserDb


async def save_user(session: AsyncSession, user: UserDb) -> None:
    session.add(user)
    await session.commit()


async def get_user(session: AsyncSession, user_id: int) -> UserDb | None:
    return await session.get(UserDb, user_id)


async def get_all_users(session: AsyncSession) -> list[UserDb] | None:
    stmt = select(UserDb).order_by(UserDb.connected_at)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_username(session: AsyncSession, username: str) -> UserDb | None:
    stmt = select(UserDb).where(UserDb.username == username)
    result: Result = await session.execute(stmt)
    users = result.scalars().one_or_none()
    return users


async def get_adm_count(session: AsyncSession) -> UserDb | None:
    stmt = select(func.count()).select_from(UserDb).where(UserDb.is_admin.is_(True))
    result: Result = await session.execute(stmt)
    adm_count = result.scalars().one_or_none()
    return adm_count
