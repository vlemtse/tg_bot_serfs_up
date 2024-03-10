__all__ = ("commands",)

from pydantic import BaseModel


class Base(BaseModel):
    key: str
    description: str


class Admin(BaseModel):
    help: Base = Base(key="adm_help", description="Команды админа")
    all_users: Base = Base(key="all_users", description="Все пользователи")
    add_admin: Base = Base(key="add_admin", description="Добавить нового админа")
    delete_admin: Base = Base(key="delete_admin", description="Удалить админа")


class User(BaseModel):
    update_name: Base = Base(key="update_name", description="Обновить имя")


class Commands(BaseModel):
    admin: Admin = Admin()
    user: User = User()


commands = Commands()
