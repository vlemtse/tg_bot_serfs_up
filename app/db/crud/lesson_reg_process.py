__all__ = ("ULRP",)

from sqlalchemy import select, Result, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserLessonRegistrationProcessDb


class ULRP:
    @classmethod
    async def save(
        cls, session: AsyncSession, obj: UserLessonRegistrationProcessDb
    ) -> None:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)

    @classmethod
    async def get_by_params(
        cls, session: AsyncSession, message_id: int, chat_id: int, user_id: int
    ) -> UserLessonRegistrationProcessDb | None:
        stmt = select(UserLessonRegistrationProcessDb).where(
            and_(
                UserLessonRegistrationProcessDb.message_id == message_id,
                UserLessonRegistrationProcessDb.chat_id == chat_id,
                UserLessonRegistrationProcessDb.user_id == user_id,
            )
        )
        result: Result = await session.execute(stmt)
        ulrp = result.scalars().one_or_none()
        return ulrp

    @classmethod
    async def delete(
        cls, session: AsyncSession, obj: UserLessonRegistrationProcessDb
    ) -> None:
        await session.delete(obj)
        await session.commit()
