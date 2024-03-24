from datetime import datetime
from enum import Enum

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.routers.login import command_start_handler
from app.bot.schemas import LessonRegProcess
from app.configs import config
from app.db import (
    UserDb,
    UserLessonRegistrationDb,
    UserLessonRegistrationCrud,
    UserLessonRegistrationProcessDb,
    ULRP,
    UserCrud,
)
from app.bot.keyboards import LessonRegProcessKeyboards
from app.funcs import prepare_data, get_datetime_shri

router = Router()


class RegState(Enum):
    select_lesson_type = "select_lesson_type"
    select_lesson_date = "select_lesson_date"
    select_lesson_number = "select_lesson_number"
    select_place = "select_place"
    select_theory = "select_theory"
    select_preferred_start_time = "select_preferred_start_time"
    select_preferred_instructor = "select_preferred_instructor"
    accept_or_change_registration = "accept_or_change_registration"
    registration_done = "registration_done"


@router.message(Command("registration_for_a_lesson"))
async def command_registration_for_a_lesson(
    msg: Message, state: FSMContext, session: AsyncSession, user: UserDb | None
):
    if not user:
        return await command_start_handler(msg=msg, state=state, user=user)

    # todo проверка на наличие записи

    msg_s = await msg.answer(
        text=f"На какой вид занятия Вы хотите записаться?",
        reply_markup=await LessonRegProcessKeyboards.select_lesson_type(session),
    )

    str_state = LessonRegProcess().model_dump_json()
    ulrp = UserLessonRegistrationProcessDb(
        user_id=msg.from_user.id,
        chat_id=msg.chat.id,
        message_id=msg_s.message_id,
        status=RegState.select_lesson_type.value,
        state=str_state,
    )
    await ULRP.save(session=session, obj=ulrp)


@router.callback_query(F.data.startswith(LessonRegProcessKeyboards.day_prefix))
async def set_select_lesson_day(
    callback_query: CallbackQuery, session: AsyncSession, user: UserDb
):

    state = await update_data(
        prefix=LessonRegProcessKeyboards.day_prefix,
        data=callback_query.data,
        user_id=user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        status=RegState.select_lesson_number.value,
        session=session,
    )

    await callback_answer(
        callback_query=callback_query,
        text=f"Выберите номер занятия из пакета:",
        state=state,
        keyboard=await LessonRegProcessKeyboards.select_lesson_number(),
    )


@router.callback_query(F.data.startswith(LessonRegProcessKeyboards.type_prefix))
async def set_select_lesson_type(
    callback_query: CallbackQuery, session: AsyncSession, user: UserDb
):
    data = await prepare_data(
        prefix=LessonRegProcessKeyboards.type_prefix, data=callback_query.data
    )
    if data == "Индивидуальное":
        text = "Для записи на индивидуальное занятие напиши в личку"
        return await go_to_reg_admin(
            callback_query=callback_query, text=text, session=session, user=user
        )

    date: datetime = await get_datetime_shri()
    conf_timelimit = config.tg_bot.registration.timelimit
    timelimit = int(f"{conf_timelimit.hours}{conf_timelimit.minutes}")
    if int(date.time().strftime("%H%M")) > timelimit:
        text = (
            f"Запись на {data} занятие выполняется до {conf_timelimit.hours}:{conf_timelimit.minutes}\n"
            f"За дополнительной информацией обратитесь к администратору"
        )
        return await go_to_reg_admin(
            callback_query=callback_query, text=text, session=session, user=user
        )

    state = await update_data(
        prefix=LessonRegProcessKeyboards.type_prefix,
        data=callback_query.data,
        user_id=user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        status=RegState.select_lesson_date.value,
        session=session,
    )

    await callback_answer(
        callback_query=callback_query,
        text=f"На какой день вы хотите записаться?",
        state=state,
        keyboard=await LessonRegProcessKeyboards.select_day(),
    )


async def go_to_reg_admin(
    callback_query: CallbackQuery, session: AsyncSession, text: str, user: UserDb
):
    ulrp = await ULRP.get_by_params(
        session=session,
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        user_id=user.id,
    )
    # Удаляем процесс после успешной регистрации
    await ULRP.delete(session=session, obj=ulrp)

    reg_adm_users: list[UserDb] = await UserCrud.get_reg_admins(session)
    usernames = [f"@{user.username}" for user in reg_adm_users]
    str_telegram_users = ", ".join(usernames)

    return await callback_query.bot.edit_message_text(
        text=f"{text} - {str_telegram_users}",
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )


@router.callback_query(F.data.startswith(LessonRegProcessKeyboards.number_prefix))
async def set_select_lesson_number(
    callback_query: CallbackQuery, session: AsyncSession, user: UserDb
):
    state = await update_data(
        prefix=LessonRegProcessKeyboards.number_prefix,
        data=callback_query.data,
        user_id=user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        status=RegState.select_place.value,
        session=session,
    )

    await callback_answer(
        callback_query=callback_query,
        text=f"Выберите место урока:",
        state=state,
        keyboard=await LessonRegProcessKeyboards.select_place(session),
    )


@router.callback_query(F.data.startswith(LessonRegProcessKeyboards.place_prefix))
async def set_select_lesson_place(
    callback_query: CallbackQuery, session: AsyncSession, user: UserDb
):
    state = await update_data(
        prefix=LessonRegProcessKeyboards.place_prefix,
        data=callback_query.data,
        user_id=user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        status=RegState.select_theory.value,
        session=session,
    )

    await callback_answer(
        callback_query=callback_query,
        text=f'Нужна теория для "{state.place}"?',
        state=state,
        keyboard=await LessonRegProcessKeyboards.select_theory(),
    )


@router.callback_query(F.data.startswith(LessonRegProcessKeyboards.theory_prefix))
async def set_select_theory(
    callback_query: CallbackQuery, session: AsyncSession, user: UserDb
):
    state = await update_data(
        prefix=LessonRegProcessKeyboards.theory_prefix,
        data=callback_query.data,
        user_id=user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        status=RegState.select_preferred_start_time.value,
        session=session,
    )

    await callback_answer(
        callback_query=callback_query,
        text="Выбери предпочтительное время.\n"
        "Но к сожалению не всегда получается подстроить под него расписание 😔",
        state=state,
        keyboard=await LessonRegProcessKeyboards.select_preferred_start_time(),
    )


@router.callback_query(
    F.data.startswith(LessonRegProcessKeyboards.preferred_start_time_prefix)
)
async def set_select_preferred_start_time(
    callback_query: CallbackQuery, session: AsyncSession, user: UserDb
):
    state = await update_data(
        prefix=LessonRegProcessKeyboards.preferred_start_time_prefix,
        data=callback_query.data,
        user_id=user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        status=RegState.select_preferred_instructor.value,
        session=session,
    )

    await callback_answer(
        callback_query=callback_query,
        text="Выбери какому инструктору хотелось бы попасть.\n"
        "К сожалению и под него не всегда получается подстроить расписание 😔",
        state=state,
        keyboard=await LessonRegProcessKeyboards.select_preferred_instructor(session),
    )


@router.callback_query(
    F.data.startswith(LessonRegProcessKeyboards.preferred_instructor_prefix)
)
async def set_select_preferred_instructor(
    callback_query: CallbackQuery, session: AsyncSession, user: UserDb
):
    state = await update_data(
        prefix=LessonRegProcessKeyboards.preferred_instructor_prefix,
        data=callback_query.data,
        user_id=user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        status=RegState.accept_or_change_registration.value,
        session=session,
    )

    text = await prepare_end_text(text=f"Подтвердите свою запись:\n", state=state)

    await callback_answer(
        callback_query=callback_query,
        text=text,
        state=state,
        keyboard=await LessonRegProcessKeyboards.accept_or_change_registration(),
    )


@router.callback_query(
    F.data.startswith(LessonRegProcessKeyboards.accept_or_change_registration_prefix),
    F.data.endswith("True"),
)
async def set_accept_registration(
    callback_query: CallbackQuery, session: AsyncSession, user: UserDb
):
    ulrp = await ULRP.get_by_params(
        session=session,
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        user_id=user.id,
    )
    if not ulrp:
        print("Запись не найдена")
        return None

    state: LessonRegProcess = LessonRegProcess.model_validate_json(ulrp.state)
    await UserLessonRegistrationCrud.save(
        session=session,
        obj=UserLessonRegistrationDb(
            user_id=user.id,
            type=state.type,
            date=state.date,
            number=state.number,
            place=state.place,
            need_theory=state.need_theory,
            start_time="" if state.start_time == "Неважно" else state.start_time,
            instructor="" if state.instructor == "Неважно" else state.instructor,
        ),
    )
    # Удаляем процесс после успешной регистрации
    await ULRP.delete(session=session, obj=ulrp)

    text = await prepare_end_text(
        text=f"Поздравляю! Вы записаны на занятие:\n", state=state
    )

    await callback_query.bot.edit_message_text(
        text=text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )


@router.callback_query(
    F.data.startswith(LessonRegProcessKeyboards.accept_or_change_registration_prefix),
    F.data.endswith("False"),
)
async def set_change_registration(
    callback_query: CallbackQuery, session: AsyncSession, user: UserDb
):
    state = await update_data(
        prefix=LessonRegProcessKeyboards.accept_or_change_registration_prefix,
        data=callback_query.data,
        user_id=user.id,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        status=RegState.select_lesson_date.value,
        session=session,
    )

    await callback_answer(
        callback_query=callback_query,
        text=f"На какой день вы хотите записаться?",
        state=state,
        keyboard=await LessonRegProcessKeyboards.select_day(),
    )


async def prepare_end_text(text: str, state: LessonRegProcess):
    theory = " + теория" if state.need_theory else ""
    return (
        f"{text}\n"
        f"День - {hbold(state.date)}\n"
        f"Вид - {hbold(state.type)}\n"
        f"Номер - {hbold(state.number)}\n"
        f"Место - {hbold(state.place + theory)}\n"
        f"Время - {hbold(state.start_time)}\n"
        f"Инструктор - {hbold(state.instructor)}\n"
    )


async def update_data(
    prefix: str,
    session: AsyncSession,
    user_id: int,
    chat_id: int,
    message_id: int,
    data: str,
    status: str,
) -> LessonRegProcess | None:
    try:
        data = await prepare_data(prefix, data)

        ulrp = await ULRP.get_by_params(
            session=session,
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
        )
        if not ulrp:
            print("Запись не найдена")
            return None

        state: LessonRegProcess = LessonRegProcess.model_validate_json(ulrp.state)

        match prefix:
            case LessonRegProcessKeyboards.type_prefix:
                state.type = data
            case LessonRegProcessKeyboards.day_prefix:
                state.date = data
            case LessonRegProcessKeyboards.number_prefix:
                state.number = data
            case LessonRegProcessKeyboards.place_prefix:
                state.place = data
            case LessonRegProcessKeyboards.theory_prefix:
                state.need_theory = True if data == "True" else False
            case LessonRegProcessKeyboards.preferred_start_time_prefix:
                state.start_time = data
            case LessonRegProcessKeyboards.preferred_instructor_prefix:
                state.instructor = data
            case LessonRegProcessKeyboards.accept_or_change_registration_prefix:
                state = LessonRegProcess()

        ulrp.state = state.model_dump_json()
        ulrp.status = status

        await ULRP.save(session=session, obj=ulrp)
        return state
    except Exception as e:
        print(e)
        return None


async def callback_answer(
    callback_query: CallbackQuery,
    text: str,
    state: LessonRegProcess | bool | None,
    keyboard: InlineKeyboardMarkup | None,
):
    if state:
        await callback_query.bot.edit_message_text(
            text=text,
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard,
        )
    else:
        await callback_query.bot.edit_message_text(
            text=f"Ошибка, попробуйте позже, пожалуйста.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
        )
