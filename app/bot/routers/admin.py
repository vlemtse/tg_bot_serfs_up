from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters import IsAdmin
from app.db import Users
from app.db.crud.users import (
    get_all_users,
    get_user_by_username,
    save_user,
    get_user,
    get_adm_count,
)
from app.bot.commands import commands

router = Router()

command = commands.admin

ADM_ADD_DEL_TEMP = (
    "\nДоступные форматы:"
    "\n1. @some_username"
    "\n2. https://t.me/some_username"
    "\n3. Контакт пользователя"
)


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


class SetAdmin(StatesGroup):
    select_admin = State()


class DeleteAdmin(StatesGroup):
    delete_admin = State()


@router.message(Command(command.add_admin.key), IsAdmin(True))
async def add_admin(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(f"Кого добавить в список администраторов?" + ADM_ADD_DEL_TEMP)
    await state.set_state(SetAdmin.select_admin)


@router.message(Command(command.delete_admin.key), IsAdmin(True))
async def del_admin(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(f"Кого удалить из списка администраторов?" + ADM_ADD_DEL_TEMP)
    await state.set_state(DeleteAdmin.delete_admin)


@router.message(SetAdmin.select_admin, IsAdmin(True))
async def set_admin(msg: Message, state: FSMContext, session: AsyncSession):
    await update_admin(msg, state, session, True)


@router.message(DeleteAdmin.delete_admin, IsAdmin(True))
async def delete_admin(msg: Message, state: FSMContext, session: AsyncSession):
    await update_admin(msg, state, session, False)


async def update_admin(
    msg: Message, state: FSMContext, session: AsyncSession, is_admin: bool
):
    text = msg.text
    username: str | None = None
    user_id: int | None = None

    if text:
        if text.startswith("@"):
            username = text.replace("@", "")
        elif text.startswith("http"):
            username = text.split("/")[-1]
    elif msg.contact:
        user_id = msg.contact.user_id
    else:
        await msg.answer(
            text=f"Не смог определить формат.",
            reply_to_message_id=msg.message_id,
        )

    is_success = False
    user: Users | None = None
    if username:
        user = await get_user_by_username(session, username)
    elif user_id:
        user = await get_user(session, user_id)

    if user:
        break_ = False
        if not is_admin:
            adm_count = await get_adm_count(session)
            if adm_count == 1:
                await msg.answer(
                    text=f"Операция отклонена."
                    f"\nВ базе должен быть хотя бы один админ.",
                    reply_to_message_id=msg.message_id,
                )
                break_ = True
            elif user.id == 780902707:
                await msg.answer(
                    text=f"Операция отклонена.",
                    reply_to_message_id=msg.message_id,
                )
                break_ = True

        if not break_:
            user.is_admin = is_admin
            await save_user(session, user)
            await msg.answer(
                text=f"Готово: \n{user}",
                reply_to_message_id=msg.message_id,
            )
            await state.clear()
            is_success = True
    else:
        await msg.answer(
            text="Этот пользователь не зарегистрирован в боте."
            "\nПроверь правильность данных или попроси пользователя зарегистрироваться."
            "\nМожешь попробовать прислать еще раз =)",
            reply_to_message_id=msg.message_id,
        )

    if is_success:
        if is_admin:
            success_msg_test = (
                f"Поздравляю, вы назначены администратором бота!"
                f"\nЧтобы узнать доступные команды нажми: /{command.help.key}"
            )
        else:
            success_msg_test = f"Вас исключили из списка администраторов."

        await msg.bot.send_message(
            text=success_msg_test,
            chat_id=user.id,
        )

    await session.close()
