import csv
import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters import IsAdmin
from app.bot.keyboards import AdminsKeyboards
from app.bot.schemas import LessonReg
from app.configs.constants import PROJECT_ROOT_PATH
from app.db import UserDb, UserLessonRegistrationDb, UserLessonRegistrationCrud
from app.db.crud.users import (
    get_all_users,
    get_user_by_username,
    save_user,
    get_user,
    get_adm_count,
)
from app.bot.commands import commands
from app.funcs import prepare_data, str_datetime, str_datetime_file

from logging import getLogger

logger = getLogger(__name__)

router = Router()

command = commands.admin

ADM_ADD_DEL_TEMP = (
    "\nДоступные форматы:"
    "\n1. @some_username"
    "\n2. https://t.me/some_username"
    "\n3. Контакт пользователя"
)
path = PROJECT_ROOT_PATH / "tmp"
file_name = "users_lessons_reg_{}.csv"


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


class UpdateAdmin(StatesGroup):
    select_admin = State()
    delete_admin = State()


@router.message(Command(command.add_admin.key), IsAdmin(True))
async def add_admin(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(f"Кого добавить в список администраторов?" + ADM_ADD_DEL_TEMP)
    await state.set_state(UpdateAdmin.select_admin)


@router.message(Command(command.delete_admin.key), IsAdmin(True))
async def del_admin(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(f"Кого удалить из списка администраторов?" + ADM_ADD_DEL_TEMP)
    await state.set_state(UpdateAdmin.delete_admin)


@router.message(UpdateAdmin.select_admin, IsAdmin(True))
async def set_admin(msg: Message, state: FSMContext, session: AsyncSession):
    await update_admin(msg, state, session, True)
    await state.clear()


@router.message(UpdateAdmin.delete_admin, IsAdmin(True))
async def delete_admin(msg: Message, state: FSMContext, session: AsyncSession):
    await update_admin(msg, state, session, False)
    await state.clear()


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
    user: UserDb | None = None
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


@router.message(
    Command(command.upload_users_registration.key),
    IsAdmin(True),
)
async def upload_users_registration(
    msg: Message,
):
    await msg.answer(
        f"За какой период выгрузить регистрацию на уроки?",
        reply_markup=await AdminsKeyboards.upload_users_registration(),
    )


@router.callback_query(
    F.data.startswith(AdminsKeyboards.upload_users_registration_date_prefix),
    IsAdmin(True),
)
async def upload_users_registration(
    callback_query: CallbackQuery, session: AsyncSession
):
    data = await prepare_data(
        AdminsKeyboards.upload_users_registration_date_prefix, callback_query.data
    )
    regs: list[UserLessonRegistrationDb]
    all_time = False
    if data == "all the time":
        regs = await UserLessonRegistrationCrud.get_all(session)
        all_time = True
    else:
        regs = await UserLessonRegistrationCrud.get_by_date(session, data)

    reg_upload: list[dict] = []
    for i in regs:
        reg_upload.append(
            LessonReg(
                date=i.date,
                username="@" + i.user.username,
                registration_name=i.user.registration_name,
                type=i.type,
                number=i.number,
                place=i.place,
                need_theory=i.need_theory,
                start_time=i.start_time,
                instructor=i.instructor,
                comment=i.comment,
            ).model_dump(by_alias=True)
        )

    if not reg_upload:
        await callback_query.bot.edit_message_text(
            text="В базе нет записей.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
        )
        return

    file = path / file_name.format(str_datetime_file(False))
    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=reg_upload[0].keys(),
            delimiter=";",
        )
        writer.writeheader()
        for i in reg_upload:
            writer.writerow(i)

    await callback_query.message.answer_document(
        text="Данные успешно загружены.",
        reply_to_message_id=callback_query.message.message_id,
        document=FSInputFile(path=file),
    )

    text = "Выгрузка данных за {}."
    if all_time:
        text = text.format("все время")
    else:
        text = text.format(f"'{data}'")

    await callback_query.bot.edit_message_text(
        text=text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )

    if os.path.exists(file):
        os.remove(file)
        logger.debug("The file deleted")
    else:
        logger.error("The file does not exist")
