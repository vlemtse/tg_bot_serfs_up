__all__ = ("LessonTypeCrud",)

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import LessonTypeDb


class LessonTypeCrud:
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[LessonTypeDb] | None:
        stmt = select(LessonTypeDb).order_by(LessonTypeDb.object_id)
        result: Result = await session.execute(stmt)
        types = result.scalars().all()
        return list(types)
