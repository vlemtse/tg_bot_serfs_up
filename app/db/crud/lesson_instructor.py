__all__ = ("LessonInstructorCrud",)

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import LessonInstructorDb


class LessonInstructorCrud:
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[LessonInstructorDb] | None:
        stmt = select(LessonInstructorDb).order_by(LessonInstructorDb.name)
        result: Result = await session.execute(stmt)
        types = result.scalars().all()
        return list(types)
