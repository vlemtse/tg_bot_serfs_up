__all__ = ("LoginKeyboards",)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from logging import getLogger

logger = getLogger(__name__)


class LoginKeyboards:
    user_name_prefix = "set_user_name_"

    @classmethod
    async def set_user_name(cls):
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text=f"Да", callback_data=cls.user_name_prefix + "True"
                ),
                InlineKeyboardButton(
                    text=f"Установить другое",
                    callback_data=cls.user_name_prefix + "False",
                ),
            ]
        ]

        set_user_name = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        return set_user_name
