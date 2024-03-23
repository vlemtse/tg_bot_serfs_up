__all__ = ("AdminsKeyboards",)

from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.funcs import get_datetime_shri

from logging import getLogger

logger = getLogger(__name__)


class AdminsKeyboards:
    upload_users_registration_date_prefix = "upload_users_registration_date_"

    @classmethod
    async def upload_users_registration(cls):
        inline_keyboard = []
        now = await get_datetime_shri()
        today = now.strftime("%d.%m.%Y")
        tomorrow = (now + timedelta(1)).strftime("%d.%m.%Y")

        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Сегодня - {today}",
                    callback_data=cls.upload_users_registration_date_prefix + today,
                ),
            ]
        )
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Завтра - {tomorrow}",
                    callback_data=cls.upload_users_registration_date_prefix + tomorrow,
                ),
            ]
        )
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"За все время",
                    callback_data=cls.upload_users_registration_date_prefix
                    + "all_the_time",
                ),
            ]
        )
        upload_users_registration_date = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard
        )

        return upload_users_registration_date
