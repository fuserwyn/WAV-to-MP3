import logging
import tempfile
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile, Message

from app.models.user_model import UserModel
from app.services.audio_converter import convert_wav_to_mp3
from app.views import messages


logger = logging.getLogger("wav-to-mp3-bot")
MAX_TELEGRAM_DOWNLOAD_BYTES = 20 * 1024 * 1024


def create_router(bot: Bot, user_model: UserModel) -> Router:
    router = Router()

    def track_user(message: Message) -> None:
        user = message.from_user
        if user is None:
            return
        user_model.upsert_user(user.id, user.username, user.first_name, user.last_name)

    @router.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        track_user(message)
        await message.answer(messages.start_text())

    @router.message(Command("stats"))
    async def cmd_stats(message: Message) -> None:
        track_user(message)
        rows, total_users, total_conversions = user_model.fetch_stats()
        await message.answer(messages.stats_text(rows, total_users, total_conversions))

    @router.message(F.document)
    async def convert_document(message: Message) -> None:
        track_user(message)
        document = message.document
        filename = (document.file_name or "").lower()

        if not filename.endswith(".wav"):
            await message.answer(messages.INVALID_EXTENSION_TEXT)
            return

        if document.file_size and document.file_size > MAX_TELEGRAM_DOWNLOAD_BYTES:
            await message.answer(messages.FILE_TOO_BIG_TEXT)
            return

        await message.answer(messages.CONVERTING_TEXT)

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.wav"
            output_path = Path(tmpdir) / "output.mp3"

            try:
                await bot.download(document, destination=input_path)
            except TelegramBadRequest as exc:
                if "file is too big" in str(exc).lower():
                    await message.answer(messages.FILE_TOO_BIG_TEXT)
                    return
                raise

            try:
                result = convert_wav_to_mp3(input_path, output_path)
            except Exception:
                logger.exception("Failed to run ffmpeg")
                await message.answer(messages.FFMPEG_START_ERROR_TEXT)
                return

            if result.returncode != 0 or not output_path.exists():
                logger.error("ffmpeg failed: %s", result.stderr)
                await message.answer(messages.CONVERT_ERROR_TEXT)
                return

            if message.from_user:
                user_model.increment_conversions(message.from_user.id)
            audio = FSInputFile(path=output_path, filename="converted.mp3")
            await message.answer_document(audio, caption=messages.CONVERT_SUCCESS_CAPTION)

    @router.message()
    async def fallback(message: Message) -> None:
        track_user(message)
        await message.answer(messages.FALLBACK_TEXT)

    return router
