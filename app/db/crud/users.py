from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Users
from app.db.schemas import UserCreate


async def create_user(session: AsyncSession, user: UserCreate):
    pass
