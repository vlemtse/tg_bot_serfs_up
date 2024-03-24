__all__ = ("UserLessonRegistrationCrud",)

from sqlalchemy import select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import UserLessonRegistrationDb


class UserLessonRegistrationCrud:
    @classmethod
    async def save(cls, session: AsyncSession, obj: UserLessonRegistrationDb) -> None:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[UserLessonRegistrationDb]:
        stmt = (
            select(UserLessonRegistrationDb)
            .order_by(UserLessonRegistrationDb.date.desc())
            .options(selectinload(UserLessonRegistrationDb.user))
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
            .options(selectinload(UserLessonRegistrationDb.user))
        )
        result: Result = await session.execute(stmt)
        users_lessons_registrations = result.scalars().all()
        return list(users_lessons_registrations)

    @classmethod
    async def get_by_user_and_date(
        cls, session: AsyncSession, date: str, user_id: int
    ) -> UserLessonRegistrationDb | None:
        stmt = select(UserLessonRegistrationDb).where(
            and_(
                UserLessonRegistrationDb.date == date,
                UserLessonRegistrationDb.user_id == user_id,
            )
        )
        result: Result = await session.execute(stmt)
        users_lessons_registrations = result.scalars().one_or_none()
        return users_lessons_registrations
