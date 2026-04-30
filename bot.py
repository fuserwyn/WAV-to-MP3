import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN, DATABASE_URL
from app.controllers.bot_controller import create_router
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository

if not BOT_TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN is required")
if not DATABASE_URL:
    raise RuntimeError("Environment variable DATABASE_URL is required")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("wav-to-mp3-bot")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    user_repository = UserRepository(DATABASE_URL)
    user_model = UserModel(user_repository)
    user_model.init_db()
    dp.include_router(create_router(bot, user_model))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
