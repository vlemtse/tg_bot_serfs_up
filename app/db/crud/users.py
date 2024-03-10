from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Users


async def create_user(session: AsyncSession, user: Users) -> None:
    session.add(user)
    await session.commit()


async def get_user(session: AsyncSession, user_id: int) -> Users | None:
    return await session.get(Users, user_id)


async def get_all_users(session: AsyncSession) -> list[Users] | None:
    stmt = select(Users).order_by(Users.connected_at)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)
