from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot import keyboard
from app.bot.middlewares import DbSessionMiddleware
from app.bot.routers import login, lesson_reg_process, admin
from app.configs import config


async def bot_start():
    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)

    # storage=MemoryStorage() - временное хранение, постоянное - в бд
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(DbSessionMiddleware())

    # Добавлять роутеры тут:
    dp.include_router(admin.router)
    dp.include_router(login.router)
    dp.include_router(lesson_reg_process.router)

    # Устанавливаем команды в кнопке меню
    await bot.set_my_commands(commands=keyboard.side_menu)

    # Удаляет/игнорирует все сообщения, которые были написаны пока бот не работал
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск бота
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
