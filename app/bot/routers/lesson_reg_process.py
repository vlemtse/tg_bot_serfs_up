from enum import Enum

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.schemas import LessonRegProcess
from app.db.models import UserLessonRegistrationProcess
from app.db.crud import ULRP
from app.bot.keyboard import (
    select_lesson_type,
    select_day,
    today,
    tomorrow,
    select_lesson_number,
    select_place,
    select_yes_or_no,
    select_preferred_start_time,
    select_preferred_instructor,
    accept_or_change_registration
)
from app.bot.keyboards import LessonRegProcessKeyboards

router = Router()


class RegForALesson(StatesGroup):
    select_lesson_type = State()
    select_lesson_date = State()
    select_lesson_number = State()
    select_place = State()
    select_theory = State()
    select_preferred_start_time = State()
    select_preferred_instructor = State()
    accept_or_change_registration = State()
    registration_done = State()


class RegState(Enum):
    select_lesson_type = 'select_lesson_type'
    select_lesson_date = 'select_lesson_date'
    select_lesson_number = 'select_lesson_number'
    select_place = 'select_place'
    select_theory = 'select_theory'
    select_preferred_start_time = 'select_preferred_start_time'
    select_preferred_instructor = 'select_preferred_instructor'
    accept_or_change_registration = 'accept_or_change_registration'
    registration_done = 'registration_done'


@router.message(Command('registration_for_a_lesson'))
async def command_registration_for_a_lesson(msg: Message, state: FSMContext, session: AsyncSession) -> None:
    msg_s = await msg.answer(
        text=f'На какой вид занятия Вы хотите записаться?',
        reply_markup=await LessonRegProcessKeyboards.select_lesson_type(session)
    )

    str_state = LessonRegProcess().model_dump_json()
    await update_state(
        session=session,
        user_id=msg.from_user.id,
        chat_id=msg.chat.id,
        message_id=msg_s.message_id,
        status=RegState.select_lesson_type.value,
        state=str_state
    )


@router.callback_query(
    F.data.startswith(LessonRegProcessKeyboards.select_lesson_type_prefix)
)
async def set_select_lesson_type(callback_query: CallbackQuery, session: AsyncSession):
    data = callback_query.data.replace(LessonRegProcessKeyboards.select_lesson_type_prefix, '')
    data = data.replace('_', ' ')

    ulrp = await ULRP.get_by_params(
        session=session,
        user_id=callback_query.from_user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )
    state = LessonRegProcess.model_validate_json(ulrp.state)
    state.type = data
    str_state = state.model_dump_json()

    await update_state(
        session=session,
        user_id=callback_query.from_user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        state=str_state,
        status=RegState.select_lesson_date.value,
    )

    await callback_query.bot.edit_message_text(
        text=f'На какой день вы хотите записаться?',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=await LessonRegProcessKeyboards.select_day()
    )


@router.callback_query(
    F.data.startswith(LessonRegProcessKeyboards.select_day_prefix)
)
async def set_select_lesson_day(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    # todo Доделать
    ulrp = await ULRP.get_by_params(
        session=session,
        user_id=callback_query.from_user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )
    if ulrp:
        state = LessonRegProcess.model_validate_json(ulrp.state)

    if callback_query.data == 'today_lesson':
        date = today
    else:
        date = tomorrow

    await state.update_data(lesson_date=date)

    await callback_query.bot.edit_message_text(
        text=f'Выберите номер занятия из пакета:',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=select_lesson_number
    )

    await state.set_state(RegForALesson.select_lesson_number)


@router.callback_query(
    RegForALesson.select_lesson_number
)
async def set_select_lesson_date(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_number=callback_query.data)

    await callback_query.bot.edit_message_text(
        text=f'Выберите место урока:',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=select_place
    )

    await state.set_state(RegForALesson.select_place)


@router.callback_query(
    RegForALesson.select_place
)
async def set_select_lesson_place(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_place=callback_query.data)

    await callback_query.bot.edit_message_text(
        text='У тебя уже была теория?',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=select_yes_or_no
    )

    await state.set_state(RegForALesson.select_theory)


@router.callback_query(
    RegForALesson.select_theory
)
async def set_select_theory(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'no':
        user_data = await state.get_data()
        await state.update_data(lesson_place=f'{user_data.get('lesson_place')} + теория')

    await callback_query.bot.edit_message_text(
        text='Выбери предпочтительное время.\n'
             'Но к сожалению не всегда получается подстроить под него расписание 😔',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=select_preferred_start_time
    )

    await state.set_state(RegForALesson.select_preferred_start_time)


@router.callback_query(
    RegForALesson.select_preferred_start_time
)
async def set_select_preferred_start_time(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_start_time=callback_query.data)

    await callback_query.bot.edit_message_text(
        text='Выбери какому инструктору хотелось бы попасть.\n'
             'К сожалению и под него не всегда получается подстроить расписание 😔',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=select_preferred_instructor
    )

    await state.set_state(RegForALesson.select_preferred_instructor)


@router.callback_query(
    RegForALesson.select_preferred_instructor
)
async def set_select_preferred_instructor(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_instructor=callback_query.data)

    user_data = await state.get_data()
    text = (f'Подтвердите свою запись:\n'
            f'Вид - {hbold(user_data.get('lesson_type'))}\n'
            f'День - {hbold(user_data.get('lesson_date'))}\n'
            f'Номер - {hbold(user_data.get('lesson_number'))}\n'
            f'Место - {hbold(user_data.get('lesson_place'))}\n'
            f'Время - {hbold(user_data.get('lesson_start_time'))}\n'
            f'Инструктор - {hbold(user_data.get('lesson_instructor'))}\n'
            )

    await callback_query.bot.edit_message_text(
        text=text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=accept_or_change_registration
    )

    await state.set_state(RegForALesson.accept_or_change_registration)


@router.callback_query(
    RegForALesson.accept_or_change_registration,
    F.data == 'accept_registration'
)
async def set_accept_registration(callback_query: CallbackQuery, state: FSMContext):
    # TODO save to db
    user_data = await state.get_data()
    text = (f'Поздравляю! Вы записаны на занятие:\n'
            f'Вид - {hbold(user_data.get('lesson_type'))}\n'
            f'День - {hbold(user_data.get('lesson_date'))}\n'
            f'Номер - {hbold(user_data.get('lesson_number'))}\n'
            f'Место - {hbold(user_data.get('lesson_place'))}\n'
            f'Время - {hbold(user_data.get('lesson_start_time'))}\n'
            f'Инструктор - {hbold(user_data.get('lesson_instructor'))}\n'
            )

    await callback_query.bot.edit_message_text(
        text=text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    await state.set_state(RegForALesson.registration_done)


@router.callback_query(
    RegForALesson.accept_or_change_registration,
    F.data == 'change_registration'
)
async def set_change_registration(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback_query.bot.edit_message_text(
        text=f'На какой вид занятия Вы хотите записаться?',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=select_lesson_type
    )

    await state.set_state(RegForALesson.select_lesson_type)


async def update_state(
        session: AsyncSession,
        user_id: int,
        chat_id: int,
        message_id: int,
        status: str,
        state: str = None
):
    ulrp = UserLessonRegistrationProcess(
        user_id=user_id,
        chat_id=chat_id,
        message_id=message_id,
        status=status,
        state=state
    )
    await ULRP.save(session=session, obj=ulrp)
