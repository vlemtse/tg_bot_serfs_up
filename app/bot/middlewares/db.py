from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_helper


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.db_helper = db_helper

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["session"]: AsyncSession = await anext(self.db_helper.session_dependency())
        return await handler(event, data)
