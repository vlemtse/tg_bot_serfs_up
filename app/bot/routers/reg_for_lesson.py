from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from app.bot.keyboards import select_lesson_type


router = Router()


class RegForALesson(StatesGroup):
    select_lesson_type = State()


@router.message(Command('registration_for_a_lesson'))
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    await msg.answer(f'На какой вид занятия Вы хотите записаться?',
                     reply_markup=select_lesson_type)

    await state.set_state(RegForALesson.select_lesson_type)


@router.callback_query(
    RegForALesson.select_lesson_type
)
async def select_lesson_type(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_type=callback_query.data)

    await callback_query.bot.edit_message_text(
        text=f'На какой день вы хотите записаться?',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=
    )





