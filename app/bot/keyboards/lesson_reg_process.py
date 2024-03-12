__all__ = ("LessonRegProcessKeyboards",)

from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import LessonTypeCrud, LessonTypeDb


class LessonRegProcessKeyboards:
    select_lesson_type_prefix = "select_lesson_type_"
    select_day_prefix = "select_day_"

    @classmethod
    async def select_lesson_type(cls, session: AsyncSession):
        types_: list[LessonTypeDb] | None = await LessonTypeCrud.get_all(session)
        inline_keyboard = []
        for type_ in types_:
            callback_data = type_.name.replace(" ", "_")
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=type_.name,
                        callback_data=cls.select_lesson_type_prefix + callback_data,
                    )
                ]
            )

        select_lesson_type = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard,
        )

        return select_lesson_type

    @classmethod
    async def select_day(cls):
        inline_keyboard = []
        now = datetime.today().date()
        today = now.strftime("%d.%m.%Y")
        tomorrow = (now + timedelta(1)).strftime("%d.%m.%Y")

        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{today}\n(Сегодня)",
                    callback_data=cls.select_day_prefix + today,
                ),
            ]
        )
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{tomorrow}\n(Завтра)",
                    callback_data=cls.select_day_prefix + tomorrow,
                ),
            ]
        )
        select_day = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        return select_day
