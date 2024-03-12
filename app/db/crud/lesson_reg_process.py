__all__ = ("ULRP",)

from sqlalchemy import select, Result, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserLessonRegistrationProcess


class ULRP:
    @classmethod
    async def save(
        cls, session: AsyncSession, obj: UserLessonRegistrationProcess
    ) -> None:
        session.add(obj)
        await session.commit()

    @classmethod
    async def get_by_params(
        cls, session: AsyncSession, message_id: int, chat_id: int, user_id: int
    ) -> UserLessonRegistrationProcess | None:
        stmt = select(UserLessonRegistrationProcess).where(
            and_(
                UserLessonRegistrationProcess.message_id == message_id,
                UserLessonRegistrationProcess.chat_id == chat_id,
                UserLessonRegistrationProcess.user_id == user_id,
            )
        )
        result: Result = await session.execute(stmt)
        ulrp = result.scalars().one_or_none()
        return ulrp

    @classmethod
    async def delete(
        cls, session: AsyncSession, obj: UserLessonRegistrationProcess
    ) -> None:
        await session.delete(obj)
