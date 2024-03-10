from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters import IsAdmin
from app.db.crud.users import get_all_users, get_user
from app.bot.commands import commands

router = Router()

command = commands.admin


@router.message(Command(command.help.key), IsAdmin(True))
async def admin_help(msg: Message):
    text = "Доступные команды:\n"
    for i in command:
        obj = i[1]
        text += f"\n/{obj.key} - {obj.description}\n"
    await msg.answer(text)


@router.message(Command(command.all_users.key), IsAdmin(True))
async def all_users(msg: Message, session: AsyncSession):
    users = await get_all_users(session)
    await msg.answer(f"{users}")


@router.message(Command(command.add_admin.key), IsAdmin(True))
async def set_admin(msg: Message, session: AsyncSession):
    pass


@router.message(Command(command.delete_admin.key), IsAdmin(True))
async def set_admin(msg: Message, session: AsyncSession):
    pass
