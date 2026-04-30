import asyncio
import logging
import os
import subprocess
import tempfile
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message


BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN is required")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("wav-to-mp3-bot")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Отправь мне WAV-файл как документ, и я верну его в MP3."
    )


@dp.message(F.document)
async def convert_document(message: Message) -> None:
    document = message.document
    filename = (document.file_name or "").lower()

    if not filename.endswith(".wav"):
        await message.answer("Нужен файл с расширением .wav")
        return

    await message.answer("Получил файл, конвертирую...")

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.wav"
        output_path = Path(tmpdir) / "output.mp3"

        await bot.download(document, destination=input_path)

        # ffmpeg converts WAV to MP3 using libmp3lame codec.
        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_path),
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(output_path),
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception:
            logger.exception("Failed to run ffmpeg")
            await message.answer("Не удалось запустить ffmpeg.")
            return

        if result.returncode != 0 or not output_path.exists():
            logger.error("ffmpeg failed: %s", result.stderr)
            await message.answer("Ошибка конвертации. Проверь, что это валидный WAV.")
            return

        audio = FSInputFile(path=output_path, filename="converted.mp3")
        await message.answer_document(audio, caption="Готово: WAV -> MP3")


@dp.message()
async def fallback(message: Message) -> None:
    await message.answer("Отправь WAV-файл как документ.")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
