from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, BotCommand


side_menu = [
    BotCommand(command='registration_for_a_lesson', description='Запись на занятие')
]

set_user_name = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='set_user_name_yes'),
            InlineKeyboardButton(text='Установить другое', callback_data='set_user_name_new'),
        ]
    ]
)

select_lesson_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Индивидуальное', callback_data='indiv_lesson'),
            InlineKeyboardButton(text='Групповое', callback_data='group_lesson'),
        ]
    ]
)

select_day = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Сегодня', callback_data='today_lesson'),
            InlineKeyboardButton(text='Завтра', callback_data='group_lesson'),
        ]
    ]
)
