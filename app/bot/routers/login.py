from datetime import datetime, UTC

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards import set_user_name
from app.db import Users
from app.db.crud.users import save_user
from app.bot.commands import commands

router = Router()

command = commands.user


class SetName(StatesGroup):
    accept_name_or_set_new = State()
    set_user_name_new = State()
    set_name_done = State()


@router.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext, user: Users) -> None:
    """
    This handler receives messages with `/start` command
    """
    await msg.answer(f"Привет, {hbold(msg.from_user.full_name)}!"
                     f"\nДля регистрации на урок необходимо указать Имя и первую букву Фамилии")

    await user_check_name(msg, state, user)


@router.message(Command(command.update_name.key))
async def update_user_name(msg: Message, state: FSMContext, user: Users):
    await user_check_name(msg, state, user)


async def user_check_name(msg: Message, state: FSMContext, user: Users):
    if user:
        name = user.registration_name
    else:
        name = f'{msg.from_user.first_name} {msg.from_user.last_name[0].upper()}'

    await msg.answer(f'{hbold(name)}'
                     f' - имя соответствует?',
                     reply_markup=set_user_name)

    await state.update_data(name=name)

    await state.set_state(SetName.accept_name_or_set_new)


@router.callback_query(
    SetName.accept_name_or_set_new,
    F.data == 'set_user_name_yes'
)
async def set_user_name_yes(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession, user: Users):
    user_data = await state.get_data()
    name = user_data.get('name')

    if not name:
        name = f'{callback_query.from_user.first_name} {callback_query.from_user.last_name[0].upper()}'

    user_id = callback_query.from_user.id

    if user:
        user.registration_name = name
        user.updated_at = str(datetime.now(UTC))
        user.chat_id = callback_query.message.chat.id
    else:
        user = Users(
            id=user_id,
            username=callback_query.from_user.username,
            first_name=callback_query.from_user.first_name,
            last_name=callback_query.from_user.last_name,
            registration_name=name,
            chat_id=callback_query.message.chat.id,
            updated_at=str(datetime.now(UTC))
        )

    await save_user(session, user)

    await callback_query.bot.edit_message_text(
        text=f'Задано имя - {hbold(user.registration_name)}',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    await state.clear()


@router.callback_query(
    SetName.accept_name_or_set_new,
    F.data == 'set_user_name_new'
)
async def msg_set_user_name_new(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.bot.edit_message_text(
        text=f'Введите Имя и первую букву Фамилии. Например:\n'
             f'{hbold('Иван В')}',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )
    await state.set_state(SetName.set_user_name_new)


@router.message(
    SetName.set_user_name_new
)
async def set_user_name_new(msg: Message, state: FSMContext):
    name = msg.text
    await state.update_data(name=name)
    await msg.answer(f'{hbold(name)} '
                     f'- имя соответствует?',
                     reply_markup=set_user_name)

    await state.set_state(SetName.accept_name_or_set_new)
