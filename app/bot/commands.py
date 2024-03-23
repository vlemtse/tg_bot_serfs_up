__all__ = ("commands",)

from aiogram.types import BotCommand
from pydantic import BaseModel


class Base(BaseModel):
    command: str
    description: str


class Admin(BaseModel):
    help: BotCommand = BotCommand(command="adm_help", description="Команды админа")
    all_users: BotCommand = BotCommand(
        command="all_users", description="Все пользователи"
    )
    add_bot_admin: BotCommand = BotCommand(
        command="add_bot_admin", description="Добавить нового админа бота"
    )
    delete_bot_admin: BotCommand = BotCommand(
        command="delete_bot_admin", description="Удалить админа бота"
    )
    add_registration_admin: BotCommand = BotCommand(
        command="add_registration_admin",
        description="Добавить нового админа регистрации",
    )
    delete_registration_admin: BotCommand = BotCommand(
        command="delete_registration_admin", description="Удалить админа регистрации"
    )
    upload_users_registration: BotCommand = BotCommand(
        command="upload_users_registration",
        description="Выгрузить регистрацию на уроки",
    )


class User(BaseModel):
    update_name: BotCommand = BotCommand(
        command="update_name",
        description="Обновить имя",
    )
    registration_for_a_lesson: BotCommand = BotCommand(
        command="registration_for_a_lesson", description="Запись на занятие"
    )


class Commands(BaseModel):
    admin: Admin = Admin()
    user: User = User()


commands = Commands()
