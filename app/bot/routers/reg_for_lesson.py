from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from app.bot.keyboards import (
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


@router.message(Command('registration_for_a_lesson'))
async def command_registration_for_a_lesson(msg: Message, state: FSMContext) -> None:
    await state.clear()

    await msg.answer(f'На какой вид занятия Вы хотите записаться?',
                     reply_markup=select_lesson_type)

    await state.set_state(RegForALesson.select_lesson_type)


@router.callback_query(
    RegForALesson.select_lesson_type
)
async def set_select_lesson_type(callback_query: CallbackQuery, state: FSMContext):

    await state.update_data(lesson_type=callback_query.data)

    await callback_query.bot.edit_message_text(
        text=f'На какой день вы хотите записаться?',
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=select_day
    )

    await state.set_state(RegForALesson.select_lesson_date)


@router.callback_query(
    RegForALesson.select_lesson_date
)
async def set_select_lesson_date(callback_query: CallbackQuery, state: FSMContext):
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
