import logging
import tempfile
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import Message

from app.config import API_HASH, API_ID, BOT_TOKEN, DATABASE_URL, MAX_INPUT_MB
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.services.audio_converter import convert_audio
from app.services.image_processor import resize_to_square
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

MP3_MIME_TYPES = {"audio/mpeg", "audio/mp3"}
WAV_MIME_TYPES = {"audio/wav", "audio/x-wav", "audio/wave", "audio/vnd.wave"}
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")


def track_user(message: Message) -> None:
    user = message.from_user
    if user is None:
        return
    user_model.upsert_user(user.id, user.username, user.first_name, user.last_name)


def detect_formats(
    file_name: str | None,
    mime_type: str | None = None,
) -> tuple[str, str] | None:
    name = (file_name or "").lower()
    if name.endswith(".wav"):
        return ".wav", ".mp3"
    if name.endswith(".mp3"):
        return ".mp3", ".wav"

    mime = (mime_type or "").lower()
    if mime in MP3_MIME_TYPES:
        return ".mp3", ".wav"
    if mime in WAV_MIME_TYPES:
        return ".wav", ".mp3"
    return None


def is_image_document(message: Message) -> bool:
    document = message.document
    if document is None:
        return False
    mime_type = (document.mime_type or "").lower()
    if mime_type.startswith("image/"):
        return True
    file_name = (document.file_name or "").lower()
    return any(file_name.endswith(ext) for ext in IMAGE_EXTENSIONS)


def get_media_file_size(message: Message) -> int | None:
    if message.photo:
        photo = message.photo
        if isinstance(photo, list):
            return photo[-1].file_size if photo else None
        return photo.file_size
    if message.document:
        return message.document.file_size
    if message.audio:
        return message.audio.file_size
    return None


async def resize_and_reply(client: Client, message: Message) -> None:
    file_size = get_media_file_size(message)
    if file_size and file_size > max_input_bytes:
        await message.reply_text(messages.file_too_big_text(MAX_INPUT_MB))
        return

    await message.reply_text(messages.RESIZING_TEXT)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.jpg"
        output_path = Path(tmpdir) / "output.jpg"

        await client.download_media(message, file_name=str(input_path))

        try:
            resize_to_square(input_path, output_path)
        except Exception:
            logger.exception("Failed to resize image")
            await message.reply_text(messages.IMAGE_ERROR_TEXT)
            return

        if message.from_user:
            user_model.increment_conversions(message.from_user.id)

        await message.reply_photo(
            photo=str(output_path),
            caption=messages.IMAGE_SUCCESS_CAPTION,
        )


async def convert_and_reply(client: Client, message: Message) -> None:
    if message.document:
        file_name = message.document.file_name
        mime_type = message.document.mime_type
        file_size = message.document.file_size
    elif message.audio:
        file_name = message.audio.file_name
        mime_type = message.audio.mime_type
        file_size = message.audio.file_size
    else:
        await message.reply_text(messages.FALLBACK_TEXT)
        return

    formats = detect_formats(file_name, mime_type)
    if formats is None:
        await message.reply_text(messages.INVALID_EXTENSION_TEXT)
        return

    input_extension, output_extension = formats
    original_name = file_name or (
        "audio.mp3" if input_extension == ".mp3" else "audio.wav"
    )
    output_filename = f"{Path(original_name).stem}{output_extension}"

    if file_size and file_size > max_input_bytes:
        await message.reply_text(messages.file_too_big_text(MAX_INPUT_MB))
        return

    await message.reply_text(messages.CONVERTING_TEXT)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / f"input{input_extension}"
        output_path = Path(tmpdir) / f"output{output_extension}"

        await client.download_media(message, file_name=str(input_path))

        try:
            result = convert_audio(input_path, output_path)
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

        caption = messages.convert_success_caption(output_extension)
        if output_extension == ".mp3":
            await message.reply_audio(
                audio=str(output_path),
                file_name=output_filename,
                title=Path(output_filename).stem,
                caption=caption,
            )
        else:
            await message.reply_document(
                document=str(output_path),
                file_name=output_filename,
                caption=caption,
            )


@app.on_message(filters.command("start"))
async def cmd_start(_: Client, message: Message) -> None:
    track_user(message)
    await message.reply_text(messages.start_text())


@app.on_message(filters.command("stats"))
async def cmd_stats(_: Client, message: Message) -> None:
    track_user(message)
    rows, total_users, total_conversions = user_model.fetch_stats()
    await message.reply_text(messages.stats_text(rows, total_users, total_conversions))


@app.on_message(filters.photo)
async def handle_photo(client: Client, message: Message) -> None:
    track_user(message)
    await resize_and_reply(client, message)


@app.on_message(filters.document | filters.audio)
async def handle_media(client: Client, message: Message) -> None:
    track_user(message)
    if is_image_document(message):
        await resize_and_reply(client, message)
        return
    await convert_and_reply(client, message)


@app.on_message(filters.all)
async def fallback(_: Client, message: Message) -> None:
    track_user(message)
    await message.reply_text(messages.FALLBACK_TEXT)


if __name__ == "__main__":
    app.run()
