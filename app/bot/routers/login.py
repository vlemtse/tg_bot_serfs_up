from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from app.bot.keyboards import set_user_name


router = Router()


class SetName(StatesGroup):
    accept_name_or_set_new = State()
    set_user_name_new = State()
    set_name_done = State()


@router.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    await msg.answer(f"Привет, {hbold(msg.from_user.full_name)}!"
                     f"\nДля регистрации на урок необходимо указать Имя и первую букву Фамилии")

    await msg.answer(f'{hbold(msg.from_user.first_name)} {hbold(msg.from_user.last_name[0].upper())} '
                     f'- имя соответствует?',
                     reply_markup=set_user_name)
    await state.set_state(SetName.accept_name_or_set_new)


@router.message(Command('update_name'))
async def update_user_name(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get('name')
    if not name:
        name = f'{msg.from_user.first_name} {msg.from_user.last_name[0].upper()}'

    await msg.answer(f'{hbold(name)}'
                     f'- имя соответствует?',
                     reply_markup=set_user_name)

    await state.update_data(name=name)

    await state.set_state(SetName.accept_name_or_set_new)


@router.callback_query(
    SetName.accept_name_or_set_new,
    F.data == 'set_user_name_yes'
)
async def set_user_name_yes(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get('name')
    if not name:
        name = f'{callback_query.from_user.first_name} {callback_query.from_user.last_name[0].upper()}'

    # TODO Сохранить в бд
    await state.update_data(name=name)

    await callback_query.bot.edit_message_text(
        text=f'Задано имя - {hbold(name)}',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    await state.set_state(SetName.set_name_done)


@router.callback_query(
    SetName.accept_name_or_set_new,
    F.data == 'set_user_name_new'
)
async def msg_set_user_name_new(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.bot.edit_message_text(
        text=f'Введите Имя и первую букву Фамилии. Например:\n'
             f'{hbold('Иванов И')}',
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




