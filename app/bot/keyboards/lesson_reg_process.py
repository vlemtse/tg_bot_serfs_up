__all__ = ("LessonRegProcessKeyboards",)

from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import (
    LessonTypeCrud,
    LessonTypeDb,
    LessonPlaceCrud,
    LessonPlaceDb,
    LessonInstructorCrud,
    LessonInstructorDb,
)


class LessonRegProcessKeyboards:
    type_prefix = "select_lesson_type_"
    day_prefix = "select_day_"
    number_prefix = "select_lesson_number_"
    place_prefix = "select_place_"
    theory_prefix = "select_theory_"
    preferred_start_time_prefix = "select_preferred_start_time_"
    preferred_instructor_prefix = "select_preferred_instructor_"
    accept_or_change_registration_prefix = "accept_or_change_registration_"

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
                        callback_data=cls.type_prefix + callback_data,
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
                    text=f"Сегодня - {today}",
                    callback_data=cls.day_prefix + today,
                ),
            ]
        )
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Завтра - {tomorrow}",
                    callback_data=cls.day_prefix + tomorrow,
                ),
            ]
        )
        select_day = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        return select_day

    @classmethod
    async def select_lesson_number(cls):
        line1 = []
        line2 = []
        for i in range(1, 11):
            elem = InlineKeyboardButton(
                text=f"{i}", callback_data=cls.number_prefix + str(i)
            )
            if i <= 5:
                line1.append(elem)
            else:
                line2.append(elem)

        inline_keyboard = [line1, line2]

        lesson_numbers = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        return lesson_numbers

    @classmethod
    async def select_place(cls, session: AsyncSession):
        elems: list[LessonPlaceDb] | None = await LessonPlaceCrud.get_all(session)
        inline_keyboard = []
        for elem in elems:
            name = elem.name
            callback_data = name.replace(" ", "_")

            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=name,
                        callback_data=cls.place_prefix + callback_data,
                    )
                ]
            )

        select_place = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard,
        )

        return select_place

    @classmethod
    async def select_theory(cls):
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text=f"Да", callback_data=cls.theory_prefix + "True"
                ),
                InlineKeyboardButton(
                    text=f"Нет", callback_data=cls.theory_prefix + "False"
                ),
            ]
        ]

        select_theory = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        return select_theory

    @classmethod
    async def select_preferred_start_time(cls):
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text=f"6:00", callback_data=cls.preferred_start_time_prefix + "6:00"
                ),
                InlineKeyboardButton(
                    text=f"7:00", callback_data=cls.preferred_start_time_prefix + "7:00"
                ),
                InlineKeyboardButton(
                    text=f"8:00", callback_data=cls.preferred_start_time_prefix + "8:00"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"9:00", callback_data=cls.preferred_start_time_prefix + "9:00"
                ),
                InlineKeyboardButton(
                    text=f"10:00",
                    callback_data=cls.preferred_start_time_prefix + "10:00",
                ),
                InlineKeyboardButton(
                    text=f"16:00",
                    callback_data=cls.preferred_start_time_prefix + "16:00",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"Не имеет значения",
                    callback_data=cls.preferred_start_time_prefix + "Неважно",
                ),
            ],
        ]

        preferred_start_time = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

        return preferred_start_time

    @classmethod
    async def select_preferred_instructor(cls, session: AsyncSession):
        elems: list[LessonInstructorDb] | None = await LessonInstructorCrud.get_all(
            session
        )
        inline_keyboard = []
        for elem in elems:
            name = elem.name
            callback_data = name.replace(" ", "_")

            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=name,
                        callback_data=cls.preferred_instructor_prefix + callback_data,
                    )
                ]
            )
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Не имеет значения",
                    callback_data=cls.preferred_instructor_prefix + "Неважно",
                )
            ]
        )

        select_instructor = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard,
        )

        return select_instructor

    @classmethod
    async def accept_or_change_registration(cls):
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text=f"Подтвердить",
                    callback_data=cls.accept_or_change_registration_prefix + "True",
                ),
                InlineKeyboardButton(
                    text=f"Изменить",
                    callback_data=cls.accept_or_change_registration_prefix + "False",
                ),
            ]
        ]

        accept_or_change_registration = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard
        )

        return accept_or_change_registration
