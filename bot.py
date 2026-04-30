import logging
import tempfile
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import Message

from app.config import API_HASH, API_ID, BOT_TOKEN, DATABASE_URL, MAX_INPUT_MB
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.services.audio_converter import convert_wav_to_mp3
from app.views import messages

if not BOT_TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN is required")
if not DATABASE_URL:
    raise RuntimeError("Environment variable DATABASE_URL is required")
if not API_ID:
    raise RuntimeError("Environment variable API_ID is required")
if not API_HASH:
    raise RuntimeError("Environment variable API_HASH is required")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("wav-to-mp3-bot")

user_repository = UserRepository(DATABASE_URL)
user_model = UserModel(user_repository)
user_model.init_db()

app = Client(
    "wav_to_mp3_bot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
)
max_input_bytes = MAX_INPUT_MB * 1024 * 1024


def track_user(message: Message) -> None:
    user = message.from_user
    if user is None:
        return
    user_model.upsert_user(user.id, user.username, user.first_name, user.last_name)


@app.on_message(filters.command("start"))
async def cmd_start(_: Client, message: Message) -> None:
    track_user(message)
    await message.reply_text(messages.start_text())


@app.on_message(filters.command("stats"))
async def cmd_stats(_: Client, message: Message) -> None:
    track_user(message)
    rows, total_users, total_conversions = user_model.fetch_stats()
    await message.reply_text(messages.stats_text(rows, total_users, total_conversions))


@app.on_message(filters.document)
async def handle_document(client: Client, message: Message) -> None:
    track_user(message)
    document = message.document
    if document is None:
        await message.reply_text(messages.FALLBACK_TEXT)
        return

    filename = (document.file_name or "").lower()
    if not filename.endswith(".wav"):
        await message.reply_text(messages.INVALID_EXTENSION_TEXT)
        return
    original_name = document.file_name or "audio.wav"
    output_filename = f"{Path(original_name).stem}.mp3"

    if document.file_size and document.file_size > max_input_bytes:
        await message.reply_text(messages.file_too_big_text(MAX_INPUT_MB))
        return

    await message.reply_text(messages.CONVERTING_TEXT)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.wav"
        output_path = Path(tmpdir) / "output.mp3"

        await client.download_media(message, file_name=str(input_path))

        try:
            result = convert_wav_to_mp3(input_path, output_path)
        except Exception:
            logger.exception("Failed to run ffmpeg")
            await message.reply_text(messages.FFMPEG_START_ERROR_TEXT)
            return

        if result.returncode != 0 or not output_path.exists():
            logger.error("ffmpeg failed: %s", result.stderr)
            await message.reply_text(messages.CONVERT_ERROR_TEXT)
            return

        if message.from_user:
            user_model.increment_conversions(message.from_user.id)
        await message.reply_document(
            document=str(output_path),
            file_name=output_filename,
            caption=messages.CONVERT_SUCCESS_CAPTION,
        )


@app.on_message(filters.all)
async def fallback(_: Client, message: Message) -> None:
    track_user(message)
    await message.reply_text(messages.FALLBACK_TEXT)


if __name__ == "__main__":
    app.run()
