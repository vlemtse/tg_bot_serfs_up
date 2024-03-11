from sqlalchemy import select, Result, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Users


async def save_user(session: AsyncSession, user: Users) -> None:
    session.add(user)
    await session.commit()


async def get_user(session: AsyncSession, user_id: int) -> Users | None:
    return await session.get(Users, user_id)


async def get_all_users(session: AsyncSession) -> list[Users] | None:
    stmt = select(Users).order_by(Users.connected_at)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_username(session: AsyncSession, username: str) -> Users | None:
    stmt = select(Users).where(Users.username == username)
    result: Result = await session.execute(stmt)
    users = result.scalars().one_or_none()
    return users


async def get_adm_count(session: AsyncSession) -> Users | None:
    stmt = select(func.count()).select_from(Users).where(Users.is_admin.is_(True))
    result: Result = await session.execute(stmt)
    adm_count = result.scalars().one_or_none()
    return adm_count
