from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, ErrorEvent

from app.bot.commands import commands
from app.bot.middlewares import DbSessionMiddleware
from app.bot.routers import login, lesson_reg_process, admin
from app.configs import config
from app.db import db_helper, UserDb

from logging import getLogger

logger = getLogger(__name__)

command = commands.user

dp = Dispatcher(storage=MemoryStorage())


async def bot_start():
    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)

    # storage=MemoryStorage() - временное хранение, постоянное - в бд

    dp.update.middleware(DbSessionMiddleware())

    # Добавлять роутеры тут:
    dp.include_router(admin.router)
    dp.include_router(login.router)
    dp.include_router(lesson_reg_process.router)

    # Устанавливаем команды в кнопке меню
    await bot.set_my_commands(
        commands=[command.update_name, command.registration_for_a_lesson]
    )

    # Удаляет/игнорирует все сообщения, которые были написаны пока бот не работал
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск бота
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


@dp.errors(F.update.message.as_("msg"))
async def error_handler(exception, msg: Message):
    logger.error(exception)
    js = msg.model_dump_json(
        exclude_defaults=True, exclude_none=True, exclude_unset=True, indent=2
    )
    text = (
        f"Ошибка при обработке сообщения "
        f"\n{exception.exception}"
        f"\n\nUser message:"
        f"\n```json\n{js}\n```"
    )

    await send_error(msg.bot, text)


@dp.errors(F.update.callback_query.as_("callback_query"))
async def error_handler(exception: ErrorEvent, callback_query: CallbackQuery):
    logger.error(exception)
    js = callback_query.model_dump_json(
        exclude_defaults=True, exclude_none=True, exclude_unset=True, indent=2
    )

    text = (
        f"Ошибка при обработке сообщения "
        f"\n{exception.exception}"
        f"\n\nUser message:"
        f"\n```json\n{js}\n```"
    )
    await send_error(callback_query.bot, text)


async def send_error(bot: Bot, text: str):
    async with db_helper.session_factory() as s:
        user = await s.get(UserDb, 780902707)

    await bot.send_message(text=text, chat_id=user.id, parse_mode=ParseMode.MARKDOWN_V2)
