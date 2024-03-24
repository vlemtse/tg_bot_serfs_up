__all__ = ("LoginKeyboards",)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from logging import getLogger

logger = getLogger(__name__)


class LoginKeyboards:
    user_name_prefix = "set_user_name_"

    @classmethod
    async def set_user_name(cls, only_new: bool = False):
        row = []
        inline_keyboard = [row]
        row.append(
            InlineKeyboardButton(
                text=f"Установить другое",
                callback_data=cls.user_name_prefix + "False",
            )
        )
        if not only_new:
            row.insert(
                0,
                InlineKeyboardButton(
                    text=f"Да", callback_data=cls.user_name_prefix + "True"
                ),
            )

        set_user_name = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        return set_user_name
