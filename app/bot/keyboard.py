from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, BotCommand

from datetime import datetime, timedelta

side_menu = [
    BotCommand(command='registration_for_a_lesson', description='Запись на занятие'),
    BotCommand(command='update_name', description='Обновить имя')
]

set_user_name = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='set_user_name_yes'),
        ],
        [
            InlineKeyboardButton(text='Установить другое', callback_data='set_user_name_new'),
        ],
    ]
)

select_lesson_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Групповое', callback_data='Групповое'),
        ],
        [
            InlineKeyboardButton(text='Индивидуальное', callback_data='Индивидуальное'),
        ],
    ],
)

now = datetime.today().date()
today = now.strftime('%d.%m.%Y')
tomorrow = (now + timedelta(1)).strftime('%d.%m.%Y')
select_day = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'{today}\n(Сегодня)', callback_data='today_lesson'),
        ],
        [
            InlineKeyboardButton(text=f'{tomorrow}\n(Завтра)', callback_data='tomorrow_lesson'),
        ]
    ]
)

select_lesson_number = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'1', callback_data='1'),
            InlineKeyboardButton(text=f'2', callback_data='2'),
            InlineKeyboardButton(text=f'3', callback_data='3'),
            InlineKeyboardButton(text=f'4', callback_data='4'),
            InlineKeyboardButton(text=f'5', callback_data='5'),
        ],
        [
            InlineKeyboardButton(text=f'6', callback_data='6'),
            InlineKeyboardButton(text=f'7', callback_data='7'),
            InlineKeyboardButton(text=f'8', callback_data='8'),
            InlineKeyboardButton(text=f'9', callback_data='9'),
            InlineKeyboardButton(text=f'10', callback_data='10'),
        ]
    ]
)

select_place = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'Пена', callback_data='Пена'),
            InlineKeyboardButton(text=f'Лайн-ап', callback_data='Лайн-ап'),
            InlineKeyboardButton(text=f'Риф', callback_data='Риф'),
        ]
    ]
)

select_yes_or_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'Да', callback_data='yes'),
            InlineKeyboardButton(text=f'Нет', callback_data='no'),
        ]
    ]
)

select_preferred_start_time = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'6:00', callback_data='6:00'),
            InlineKeyboardButton(text=f'7:00', callback_data='7:00'),
            InlineKeyboardButton(text=f'8:00', callback_data='8:00'),
        ],
        [
            InlineKeyboardButton(text=f'9:00', callback_data='9:00'),
            InlineKeyboardButton(text=f'10:00', callback_data='10:00'),
            InlineKeyboardButton(text=f'16:00', callback_data='16:00'),
        ],
        [
            InlineKeyboardButton(text=f'Не имеет значения', callback_data='Неважно'),
        ]
    ]
)

select_preferred_instructor = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'Аня', callback_data='Аня'),
            InlineKeyboardButton(text=f'Андрей', callback_data='Андрей'),

        ],
        [
            InlineKeyboardButton(text=f'Рома', callback_data='Рома'),
            InlineKeyboardButton(text=f'Макс', callback_data='Макс'),

        ],
        [
            InlineKeyboardButton(text=f'Не имеет значения', callback_data='Неважно'),
        ]
    ]
)

accept_or_change_registration = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'Подтвердить', callback_data='accept_registration'),
            InlineKeyboardButton(text=f'Изменить', callback_data='change_registration'),
        ]
    ]
)
