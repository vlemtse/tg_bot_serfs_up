import csv
import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters import IsBotAdmin
from app.bot.keyboards import AdminsKeyboards
from app.bot.schemas import LessonReg
from app.configs.constants import PROJECT_ROOT_PATH
from app.db import UserDb, UserLessonRegistrationDb, UserLessonRegistrationCrud
from app.db.crud import UserCrud
from app.bot.commands import commands
from app.funcs import prepare_data, str_datetime_file

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
file_name = "lessons_reg_to_{}_from_{}.csv"


@router.message(Command(command.help.command), IsBotAdmin(True))
async def admin_help(msg: Message):
    text = "Доступные команды:\n"
    for i in command:
        obj = i[1]
        text += f"\n/{obj.command} - {obj.description}\n"
    await msg.answer(text)


@router.message(Command(command.all_users.command), IsBotAdmin(True))
async def all_users(msg: Message, session: AsyncSession):
    users = await UserCrud.get_all_users(session)
    await msg.answer(f"{users}")


class UpdateAdmin(StatesGroup):
    select_bot_admin = State()
    delete_bot_admin = State()
    select_reg_admin = State()
    delete_reg_admin = State()


@router.message(Command(command.add_bot_admin.command), IsBotAdmin(True))
async def add_bot_admin(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(f"Кого добавить в список администраторов бота?" + ADM_ADD_DEL_TEMP)
    await state.set_state(UpdateAdmin.select_bot_admin)


@router.message(Command(command.delete_bot_admin.command), IsBotAdmin(True))
async def del_bot_admin(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(f"Кого удалить из списка администраторов бота?" + ADM_ADD_DEL_TEMP)
    await state.set_state(UpdateAdmin.delete_bot_admin)


@router.message(UpdateAdmin.select_bot_admin, IsBotAdmin(True))
async def set_bot_admin(msg: Message, state: FSMContext, session: AsyncSession):
    await update_bot_admin(msg, session, True)
    await state.clear()


@router.message(UpdateAdmin.delete_bot_admin, IsBotAdmin(True))
async def delete_bot_admin(msg: Message, state: FSMContext, session: AsyncSession):
    await update_bot_admin(msg, session, False)
    await state.clear()


@router.message(Command(command.add_registration_admin.command), IsBotAdmin(True))
async def add_reg_admin(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        f"Кого добавить в список администраторов регистрации?" + ADM_ADD_DEL_TEMP
    )
    await state.set_state(UpdateAdmin.select_reg_admin)


@router.message(Command(command.delete_registration_admin.command), IsBotAdmin(True))
async def del_reg_admin(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        f"Кого удалить из списка администраторов регистрации?" + ADM_ADD_DEL_TEMP
    )
    await state.set_state(UpdateAdmin.delete_reg_admin)


@router.message(UpdateAdmin.select_reg_admin, IsBotAdmin(True))
async def set_reg_admin(msg: Message, state: FSMContext, session: AsyncSession):
    await update_reg_admin(msg, session, True)
    await state.clear()


@router.message(UpdateAdmin.delete_reg_admin, IsBotAdmin(True))
async def delete_reg_admin(msg: Message, state: FSMContext, session: AsyncSession):
    await update_reg_admin(msg, session, False)
    await state.clear()


async def update_bot_admin(msg: Message, session: AsyncSession, is_bot_admin: bool):
    username, user_id, check_data = await get_link_data(msg)

    if not check_data:
        return await msg.answer(
            text=f"Не смог определить формат.",
            reply_to_message_id=msg.message_id,
        )

    user: UserDb | None = await get_user(session, user_id, username)

    if user:
        if not is_bot_admin:
            # Перед удалением флага админа проверяем чтобы остался хотя бы один админ
            adm_count = await UserCrud.get_bot_adm_count(session)

            reply = True
            if adm_count == 1:
                text = (
                    f"Операция отклонена. \nВ базе должен быть хотя бы один админ бота."
                )
            elif user.id == 780902707:
                text = f"Операция отклонена."
            else:
                reply = False

            if reply:
                return await msg.answer(
                    text=text,
                    reply_to_message_id=msg.message_id,
                )
            success_msg_text = f"Вас исключили из списка администраторов."

        else:
            success_msg_text = (
                f"Поздравляю, вы назначены администратором бота!"
                f"\nЧтобы узнать доступные команды нажми: /{command.help.command}"
            )

        user.is_bot_admin = is_bot_admin
        await UserCrud.save_user(session, user)
        await msg.answer(
            text=f"Готово: \n{user}",
            reply_to_message_id=msg.message_id,
        )
    else:
        return await msg.answer(
            text="Этот пользователь не зарегистрирован в боте."
            "\nПроверь правильность данных или попроси пользователя зарегистрироваться.",
            reply_to_message_id=msg.message_id,
        )

    await msg.bot.send_message(
        text=success_msg_text,
        chat_id=user.id,
    )


async def update_reg_admin(msg: Message, session: AsyncSession, is_reg_admin: bool):
    username, user_id, check_data = await get_link_data(msg)

    if not check_data:
        return await msg.answer(
            text=f"Не смог определить формат.",
            reply_to_message_id=msg.message_id,
        )

    user: UserDb | None = await get_user(session, user_id, username)

    if user:
        if not is_reg_admin:
            # Перед удалением флага админа проверяем чтобы остался хотя бы один админ
            adm_count = await UserCrud.get_reg_adm_count(session)

            if adm_count == 1:
                text = f"Операция отклонена. \nВ базе должен быть хотя бы один админ регистрации на уроки."
                return await msg.answer(
                    text=text,
                    reply_to_message_id=msg.message_id,
                )
            success_msg_text = (
                f"Вас исключили из списка администраторов регистрации на уроки."
            )

        else:
            success_msg_text = (
                f"Вы назначены администратором регистрации на уроки."
                f"\nВаш контакт будет отображаться пользователям для регистрации на Индивидуальные уроки, "
                f"а также при попытке регистрации на Групповые уроки после окончания регистрации."
            )

        user.is_reg_admin = is_reg_admin
        await UserCrud.save_user(session, user)
        await msg.answer(
            text=f"Готово: \n{user}",
            reply_to_message_id=msg.message_id,
        )
    else:
        return await msg.answer(
            text="Этот пользователь не зарегистрирован в боте."
            "\nПроверь правильность данных или попроси пользователя зарегистрироваться.",
            reply_to_message_id=msg.message_id,
        )

    await msg.bot.send_message(
        text=success_msg_text,
        chat_id=user.id,
    )


async def get_link_data(msg: Message) -> (str | None, int | None, bool):
    text = msg.text
    username: str | None = None
    user_id: int | None = None

    check_data = True
    if text:
        if text.startswith("@"):
            username = text.replace("@", "")
        elif text.startswith("http"):
            username = text.split("/")[-1]
        else:
            check_data = False
    elif msg.contact:
        user_id = msg.contact.user_id
    else:
        check_data = False

    return username, user_id, check_data


async def get_user(session: AsyncSession, user_id: int, username: str) -> UserDb | None:
    user: UserDb | None = None
    if user_id:
        user = await UserCrud.get_user(session, user_id)
    elif username:
        user = await UserCrud.get_user_by_username(session, username)
    return user


@router.message(
    Command(command.upload_users_registration.command),
    IsBotAdmin(True),
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
    IsBotAdmin(True),
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
                need_theory="Да" if i.need_theory else "",
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

    file = path / file_name.format(data, await str_datetime_file())
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
