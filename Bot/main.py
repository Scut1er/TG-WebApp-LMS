import asyncio
import logging

from aiogram import Bot, Dispatcher
import config
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from Bot.email_service import email_router
from Bot.ticket_service import ticket_router
from bot_service import main_router
from aiogram.client.bot import DefaultBotProperties


async def main():
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(main_router, email_router, ticket_router)  # Включение роутеров в диспетчер
    await bot.delete_webhook(drop_pending_updates=True)  # Обработка запросов только во время работы
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
