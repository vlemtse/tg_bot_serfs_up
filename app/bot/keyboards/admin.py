__all__ = ("AdminsKeyboards",)

from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AdminsKeyboards:
    upload_users_registration_date_prefix = "upload_users_registration_date_"

    @classmethod
    async def upload_users_registration(cls):
        inline_keyboard = []
        now = datetime.today().date()
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
                    + "all the time",
                ),
            ]
        )
        upload_users_registration_date = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard
        )

        return upload_users_registration_date
