__all__ = ("UserCrud",)

from sqlalchemy import select, Result, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserDb

from logging import getLogger

logger = getLogger(__name__)


class UserCrud:
    @classmethod
    async def save_user(cls, session: AsyncSession, user: UserDb) -> None:
        session.add(user)
        await session.commit()

    @classmethod
    async def get_user(cls, session: AsyncSession, user_id: int) -> UserDb | None:
        return await session.get(UserDb, user_id)

    @classmethod
    async def get_all_users(cls, session: AsyncSession) -> list[UserDb] | None:
        stmt = select(UserDb).order_by(UserDb.connected_at)
        result: Result = await session.execute(stmt)
        users = result.scalars().all()
        return list(users)

    @classmethod
    async def get_user_by_username(
        cls, session: AsyncSession, username: str
    ) -> UserDb | None:
        stmt = select(UserDb).where(UserDb.username == username)
        result: Result = await session.execute(stmt)
        users = result.scalars().one_or_none()
        return users

    @classmethod
    async def get_bot_adm_count(cls, session: AsyncSession) -> UserDb | None:
        stmt = (
            select(func.count())
            .select_from(UserDb)
            .where(UserDb.is_bot_admin.is_(True))
        )
        result: Result = await session.execute(stmt)
        adm_count = result.scalars().one_or_none()
        return adm_count

    @classmethod
    async def get_reg_adm_count(cls, session: AsyncSession) -> UserDb | None:
        stmt = (
            select(func.count())
            .select_from(UserDb)
            .where(UserDb.is_reg_admin.is_(True))
        )
        result: Result = await session.execute(stmt)
        adm_count = result.scalars().one_or_none()
        return adm_count

    @classmethod
    async def get_reg_admins(cls, session: AsyncSession) -> list[UserDb] | None:
        stmt = select(UserDb).where(UserDb.is_reg_admin.is_(True))
        result: Result = await session.execute(stmt)
        users = result.scalars().all()
        return list(users)
