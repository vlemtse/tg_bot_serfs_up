from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_helper, UserDb


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.session_factory = db_helper.session_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_id = data["event_from_user"].id
        async with self.session_factory() as s:
            user = await s.get(UserDb, user_id)

            data["user"] = user
            data["session"] = s
            data["is_bot_admin"] = user.is_bot_admin if user else None

            return await handler(event, data)
