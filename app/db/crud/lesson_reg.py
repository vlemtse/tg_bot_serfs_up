__all__ = ("UserLessonRegistrationCrud",)

from sqlalchemy import select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserLessonRegistrationDb


class UserLessonRegistrationCrud:
    @classmethod
    async def save(cls, session: AsyncSession, obj: UserLessonRegistrationDb) -> None:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[UserLessonRegistrationDb]:
        stmt = select(UserLessonRegistrationDb).order_by(
            UserLessonRegistrationDb.date.desc()
        )
        result: Result = await session.execute(stmt)
        users_lessons_registrations = result.scalars().all()
        return list(users_lessons_registrations)

    @classmethod
    async def get_by_date(
        cls, session: AsyncSession, date: str
    ) -> list[UserLessonRegistrationDb]:
        stmt = (
            select(UserLessonRegistrationDb)
            .where(UserLessonRegistrationDb.date == date)
            .order_by(UserLessonRegistrationDb.date.desc())
        )
        result: Result = await session.execute(stmt)
        users_lessons_registrations = result.scalars().all()
        return list(users_lessons_registrations)
