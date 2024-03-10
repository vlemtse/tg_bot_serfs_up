from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.users import get_all_users, get_user

router = Router()


@router.message(Command("all_users"))
async def update_user_name(msg: Message, session: AsyncSession):
    if not await check_is_admin(msg, session):
        return None

    users = await get_all_users(session)
    await msg.answer(f"{users}")


async def check_is_admin(msg: Message, session: AsyncSession):
    user = await get_user(session, msg.from_user.id)
    if user and user.is_admin:
        return True
    else:
        await msg.answer(f"Access denied 😈")
        return False
