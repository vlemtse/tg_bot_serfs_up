from aiogram.filters import Filter
from aiogram.types import Message


class IsBotAdmin(Filter):
    def __init__(self, is_bot_admin: bool) -> None:
        self.is_bot_admin = is_bot_admin

    async def __call__(self, message: Message, is_bot_admin: bool) -> bool:
        return is_bot_admin == self.is_bot_admin
