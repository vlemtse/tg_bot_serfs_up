__all__ = ("LessonPlaceCrud",)

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import LessonPlaceDb


class LessonPlaceCrud:
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[LessonPlaceDb] | None:
        stmt = select(LessonPlaceDb).order_by(LessonPlaceDb.object_id)
        result: Result = await session.execute(stmt)
        types = result.scalars().all()
        return list(types)
