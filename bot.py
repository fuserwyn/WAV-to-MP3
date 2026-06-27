import asyncio
import logging
import shutil
import tempfile
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message

from app.config import (
    API_HASH,
    API_ID,
    BOT_TOKEN,
    DATABASE_URL,
    MAX_INPUT_MB,
    OPENROUTER_MODEL,
    OPEN_ROUTER_KEY,
    POYO_API_KEY,
)
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.services.audio_converter import convert_audio
from app.services.image_processor import resize_to_square
from app.services.nano_banana import edit_nano_banana_image, generate_nano_banana_image
from app.services.press_release import edit_press_release, generate_press_release
from app.services.ringtone_cutter import cut_ringtone, parse_ringtone_input
from app.views import keyboards, messages

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
AUDIO_EXTENSIONS = (".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac")


TELEGRAM_MESSAGE_LIMIT = 4096

MODE_COVER = "cover"
MODE_COVER_GEN = "cover_gen"
MODE_COVER_GEN_EDIT = "cover_gen_edit"
MODE_PRESS = "press"
MODE_PRESS_IMPORT = "press_import"
MODE_PRESS_EDIT = "press_edit"
MODE_CONVERTER = "converter"
MODE_RINGTONE = "ringtone"

user_modes: dict[int, str] = {}
ringtone_pending: dict[int, dict] = {}
cover_gen_pending: dict[int, dict] = {}
press_pending: dict[int, dict] = {}


def track_user(message: Message) -> None:
    user = message.from_user
    if user is None:
        return
    user_model.upsert_user(user.id, user.username, user.first_name, user.last_name)


def get_user_id(message: Message) -> int | None:
    return message.from_user.id if message.from_user else None


def get_mode(message: Message) -> str | None:
    user_id = get_user_id(message)
    if user_id is None:
        return None
    return user_modes.get(user_id)


def set_mode(message: Message, mode: str | None) -> None:
    user_id = get_user_id(message)
    if user_id is None:
        return
    if mode is None:
        user_modes.pop(user_id, None)
    else:
        user_modes[user_id] = mode
    if mode != MODE_RINGTONE:
        clear_ringtone_pending(user_id)
    if mode not in {MODE_COVER_GEN, MODE_COVER_GEN_EDIT}:
        clear_cover_gen_pending(user_id)
    if mode not in {MODE_PRESS, MODE_PRESS_IMPORT, MODE_PRESS_EDIT}:
        clear_press_pending(user_id)


def clear_press_pending(user_id: int | None) -> None:
    if user_id is None:
        return
    press_pending.pop(user_id, None)


def clear_cover_gen_pending(user_id: int | None) -> None:
    if user_id is None:
        return
    cover_gen_pending.pop(user_id, None)


def clear_ringtone_pending(user_id: int | None) -> None:
    if user_id is None:
        return
    pending = ringtone_pending.pop(user_id, None)
    if pending and pending.get("tmpdir"):
        shutil.rmtree(pending["tmpdir"], ignore_errors=True)


def is_audio_media(message: Message) -> bool:
    if message.audio:
        return True
    document = message.document
    if document is None:
        return False
    mime_type = (document.mime_type or "").lower()
    if mime_type.startswith("audio/"):
        return True
    file_name = (document.file_name or "").lower()
    return any(file_name.endswith(ext) for ext in AUDIO_EXTENSIONS)


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


async def reply_long_text(
    message: Message,
    text: str,
    reply_markup=None,
) -> None:
    chunk_size = TELEGRAM_MESSAGE_LIMIT - 100
    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
    if not chunks:
        chunks = [""]
    for index, chunk in enumerate(chunks):
        is_last = index == len(chunks) - 1
        await message.reply_text(
            chunk,
            reply_markup=reply_markup if is_last else None,
        )


def get_output_image_filename(message: Message) -> str:
    if message.document and message.document.file_name:
        return f"{Path(message.document.file_name).stem}_3000.jpg"
    return "image_3000.jpg"


async def resize_and_reply(client: Client, message: Message) -> None:
    file_size = get_media_file_size(message)
    if file_size and file_size > max_input_bytes:
        await message.reply_text(messages.file_too_big_text(MAX_INPUT_MB))
        return

    await message.reply_text(messages.RESIZING_TEXT)

    output_filename = get_output_image_filename(message)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.jpg"
        output_path = Path(tmpdir) / output_filename

        await client.download_media(message, file_name=str(input_path))

        try:
            resize_to_square(input_path, output_path)
        except Exception:
            logger.exception("Failed to resize image")
            await message.reply_text(messages.IMAGE_ERROR_TEXT)
            return

        if message.from_user:
            user_model.increment_conversions(message.from_user.id)

        await message.reply_document(
            document=str(output_path),
            file_name=output_filename,
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
        output_path = Path(tmpdir) / output_filename

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
                title=Path(output_filename).stem,
                caption=caption,
            )
        else:
            await message.reply_document(
                document=str(output_path),
                file_name=output_filename,
                caption=caption,
            )


async def ask_ringtone_format(
    message: Message,
    pending: dict,
    start_sec: float,
    duration_sec: int,
) -> None:
    pending["start_sec"] = start_sec
    pending["duration_sec"] = duration_sec
    await message.reply_text(
        messages.RINGTONE_PICK_FORMAT_TEXT,
        reply_markup=keyboards.ringtone_format_keyboard(),
    )


async def process_ringtone(
    message: Message,
    user_id: int,
    start_sec: float,
    duration_sec: int,
    output_format: str,
) -> None:
    pending = ringtone_pending.get(user_id)
    if not pending:
        await message.reply_text(
            messages.RINGTONE_NO_AUDIO_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    await message.reply_text(messages.RINGTONE_CUTTING_TEXT)

    extension = "wav" if output_format == "wav" else "mp3"
    output_filename = f"{pending['stem']}_ringtone_{duration_sec}s.{extension}"
    output_path = Path(pending["tmpdir"]) / output_filename

    try:
        result = cut_ringtone(
            Path(pending["input_path"]),
            output_path,
            start_sec,
            duration_sec,
            output_format=extension,
        )
    except Exception:
        logger.exception("Failed to run ffmpeg for ringtone")
        await message.reply_text(
            messages.RINGTONE_ERROR_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    if result.returncode != 0 or not output_path.exists():
        logger.error("Ringtone ffmpeg failed: %s", result.stderr)
        await message.reply_text(
            messages.RINGTONE_ERROR_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    if message.from_user:
        user_model.increment_conversions(message.from_user.id)

    await message.reply_document(
        document=str(output_path),
        file_name=output_filename,
        caption=messages.ringtone_success_caption(
            start_sec, duration_sec, extension
        ),
    )
    clear_ringtone_pending(user_id)


async def save_ringtone_audio(client: Client, message: Message) -> bool:
    user_id = get_user_id(message)
    if user_id is None:
        return False

    file_size = get_media_file_size(message)
    if file_size and file_size > max_input_bytes:
        await message.reply_text(messages.file_too_big_text(MAX_INPUT_MB))
        return True

    clear_ringtone_pending(user_id)
    tmpdir = tempfile.mkdtemp()

    try:
        await message.reply_text(messages.RINGTONE_DOWNLOADING_TEXT)

        input_path = Path(tmpdir) / "input.audio"
        await asyncio.wait_for(
            client.download_media(message, file_name=str(input_path)),
            timeout=300,
        )

        if not input_path.exists() or input_path.stat().st_size == 0:
            raise ValueError("Downloaded audio file is empty")

        stem = "audio"
        if message.audio and message.audio.file_name:
            stem = Path(message.audio.file_name).stem
        elif message.document and message.document.file_name:
            stem = Path(message.document.file_name).stem

        ringtone_pending[user_id] = {
            "tmpdir": tmpdir,
            "input_path": str(input_path),
            "stem": stem,
            "start_sec": None,
        }

        await message.reply_text(
            messages.RINGTONE_AUDIO_SAVED_TEXT,
            reply_markup=keyboards.ringtone_duration_keyboard(),
        )
        return True
    except asyncio.TimeoutError:
        logger.exception("Ringtone audio download timed out for user %s", user_id)
        shutil.rmtree(tmpdir, ignore_errors=True)
        await message.reply_text(
            messages.RINGTONE_DOWNLOAD_ERROR_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return True
    except Exception:
        logger.exception("Failed to download ringtone audio for user %s", user_id)
        shutil.rmtree(tmpdir, ignore_errors=True)
        await message.reply_text(
            messages.RINGTONE_DOWNLOAD_ERROR_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return True


async def handle_ringtone_text(message: Message, text: str) -> None:
    user_id = get_user_id(message)
    if user_id is None:
        return

    try:
        start_sec, duration_sec = parse_ringtone_input(text)
    except ValueError:
        await message.reply_text(
            messages.RINGTONE_INVALID_INPUT_TEXT,
            reply_markup=keyboards.ringtone_duration_keyboard(),
        )
        return

    pending = ringtone_pending.get(user_id)
    if not pending:
        await message.reply_text(
            messages.RINGTONE_NO_AUDIO_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    if duration_sec is None:
        pending["start_sec"] = start_sec
        await message.reply_text(
            messages.RINGTONE_PICK_DURATION_TEXT,
            reply_markup=keyboards.ringtone_duration_keyboard(),
        )
        return

    await ask_ringtone_format(message, pending, start_sec, duration_sec)


async def deliver_press_result(message: Message, text: str) -> None:
    user_id = get_user_id(message)
    if user_id is not None:
        press_pending[user_id] = {"text": text}
        user_modes[user_id] = MODE_PRESS_EDIT

    await reply_long_text(
        message,
        text,
        reply_markup=keyboards.press_result_keyboard(),
    )


async def run_press(message: Message, prompt: str) -> None:
    clear_press_pending(get_user_id(message))

    if not OPEN_ROUTER_KEY:
        await message.reply_text(
            messages.PRESS_NO_KEY_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    await message.reply_text(messages.PRESS_GENERATING_TEXT)

    try:
        press_release = await generate_press_release(
            prompt=prompt,
            api_key=OPEN_ROUTER_KEY,
            model=OPENROUTER_MODEL,
        )
    except Exception:
        logger.exception("Failed to generate press release")
        await message.reply_text(
            messages.PRESS_ERROR_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    await deliver_press_result(message, press_release)


async def run_press_edit(message: Message, instructions: str) -> None:
    user_id = get_user_id(message)
    if user_id is None:
        return

    pending = press_pending.get(user_id)
    if not pending or not pending.get("text"):
        await message.reply_text(
            messages.PRESS_NO_TEXT_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    if not OPEN_ROUTER_KEY:
        await message.reply_text(
            messages.PRESS_NO_KEY_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    await message.reply_text(messages.PRESS_EDITING_TEXT)

    try:
        press_release = await edit_press_release(
            current_text=pending["text"],
            edit_instructions=instructions,
            api_key=OPEN_ROUTER_KEY,
            model=OPENROUTER_MODEL,
        )
    except Exception:
        logger.exception("Failed to edit press release")
        await message.reply_text(
            messages.PRESS_EDIT_ERROR_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    await deliver_press_result(message, press_release)


async def accept_user_press_text(message: Message, text: str) -> None:
    draft = text.strip()
    if not draft:
        await message.reply_text(
            messages.PRESS_IMPORT_EMPTY_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    await message.reply_text(
        messages.PRESS_SAVED_TEXT,
        reply_markup=keyboards.main_menu_keyboard(),
    )
    await deliver_press_result(message, draft)


async def deliver_cover_result(
    message: Message,
    output_path: Path,
    image_url: str,
    caption: str,
) -> None:
    user_id = get_user_id(message)
    if user_id is not None:
        cover_gen_pending[user_id] = {"image_url": image_url}
        user_modes[user_id] = MODE_COVER_GEN_EDIT

    await message.reply_document(
        document=str(output_path),
        caption=caption,
        reply_markup=keyboards.cover_gen_result_keyboard(),
    )


async def run_cover_gen(message: Message, prompt: str) -> None:
    clear_cover_gen_pending(get_user_id(message))

    if not POYO_API_KEY:
        await message.reply_text(
            messages.COVER_GEN_NO_KEY_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    await message.reply_text(messages.COVER_GEN_GENERATING_TEXT)

    with tempfile.TemporaryDirectory() as tmpdir:
        raw_path = Path(tmpdir) / "generated_raw.jpg"
        output_path = Path(tmpdir) / "cover_3000.jpg"
        try:
            image_url = await generate_nano_banana_image(
                prompt, POYO_API_KEY, raw_path
            )
            resize_to_square(raw_path, output_path)
        except Exception:
            logger.exception("Failed to generate cover via Nano Banana")
            await message.reply_text(
                messages.COVER_GEN_ERROR_TEXT,
                reply_markup=keyboards.main_menu_keyboard(),
            )
            return

        await deliver_cover_result(
            message,
            output_path,
            image_url,
            messages.COVER_GEN_SUCCESS_CAPTION,
        )


async def run_cover_edit(message: Message, prompt: str) -> None:
    user_id = get_user_id(message)
    if user_id is None:
        return

    pending = cover_gen_pending.get(user_id)
    if not pending or not pending.get("image_url"):
        await message.reply_text(
            messages.COVER_GEN_NO_IMAGE_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    if not POYO_API_KEY:
        await message.reply_text(
            messages.COVER_GEN_NO_KEY_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    await message.reply_text(messages.COVER_GEN_EDITING_TEXT)

    with tempfile.TemporaryDirectory() as tmpdir:
        raw_path = Path(tmpdir) / "edited_raw.jpg"
        output_path = Path(tmpdir) / "cover_3000.jpg"
        try:
            image_url = await edit_nano_banana_image(
                prompt,
                [pending["image_url"]],
                POYO_API_KEY,
                raw_path,
            )
            resize_to_square(raw_path, output_path)
        except Exception:
            logger.exception("Failed to edit cover via Nano Banana")
            await message.reply_text(
                messages.COVER_GEN_EDIT_ERROR_TEXT,
                reply_markup=keyboards.main_menu_keyboard(),
            )
            return

        await deliver_cover_result(
            message,
            output_path,
            image_url,
            messages.COVER_GEN_EDIT_SUCCESS_CAPTION,
        )


@app.on_message(filters.command("start"))
async def cmd_start(_: Client, message: Message) -> None:
    track_user(message)
    set_mode(message, None)
    await message.reply_text(
        messages.start_text(),
        reply_markup=keyboards.main_menu_keyboard(),
    )


@app.on_message(filters.command("stats"))
async def cmd_stats(_: Client, message: Message) -> None:
    track_user(message)
    rows, total_users, total_conversions = user_model.fetch_stats()
    await message.reply_text(messages.stats_text(rows, total_users, total_conversions))


@app.on_message(filters.command("press"))
async def cmd_press(_: Client, message: Message) -> None:
    track_user(message)
    set_mode(message, MODE_PRESS)

    prompt = ""
    if message.text:
        parts = message.text.split(maxsplit=1)
        if len(parts) > 1:
            prompt = parts[1].strip()

    if not prompt:
        await message.reply_text(
            messages.PRESS_MODE_TEXT,
            reply_markup=keyboards.press_mode_keyboard(),
        )
        return

    await run_press(message, prompt)


@app.on_message(filters.command("gen"))
async def cmd_gen(_: Client, message: Message) -> None:
    track_user(message)
    set_mode(message, MODE_COVER_GEN)

    prompt = ""
    if message.text:
        parts = message.text.split(maxsplit=1)
        if len(parts) > 1:
            prompt = parts[1].strip()

    if not prompt:
        await message.reply_text(
            messages.COVER_GEN_MODE_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    await run_cover_gen(message, prompt)


@app.on_message(filters.text & ~filters.command(["start", "stats", "press", "gen"]))
async def handle_text(_: Client, message: Message) -> None:
    track_user(message)
    text = (message.text or "").strip()

    if text == keyboards.BTN_COVER:
        set_mode(message, MODE_COVER)
        await message.reply_text(
            messages.COVER_MODE_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    if text == keyboards.BTN_COVER_GEN:
        clear_cover_gen_pending(get_user_id(message))
        set_mode(message, MODE_COVER_GEN)
        await message.reply_text(
            messages.COVER_GEN_MODE_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    if text == keyboards.BTN_PRESS:
        clear_press_pending(get_user_id(message))
        set_mode(message, None)
        await message.reply_text(
            messages.PRESS_MODE_TEXT,
            reply_markup=keyboards.press_mode_keyboard(),
        )
        return

    if text == keyboards.BTN_CONVERTER:
        set_mode(message, MODE_CONVERTER)
        await message.reply_text(
            messages.CONVERTER_MODE_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    if text == keyboards.BTN_RINGTONE:
        set_mode(message, MODE_RINGTONE)
        await message.reply_text(
            messages.RINGTONE_MODE_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    if text == keyboards.BTN_MENU:
        set_mode(message, None)
        await message.reply_text(
            messages.MENU_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    if get_mode(message) == MODE_PRESS:
        await run_press(message, text)
        return

    if get_mode(message) == MODE_PRESS_IMPORT:
        await accept_user_press_text(message, text)
        return

    if get_mode(message) == MODE_PRESS_EDIT:
        await run_press_edit(message, text)
        return

    if get_mode(message) == MODE_COVER_GEN:
        await run_cover_gen(message, text)
        return

    if get_mode(message) == MODE_COVER_GEN_EDIT:
        await run_cover_edit(message, text)
        return

    if get_mode(message) == MODE_RINGTONE:
        await handle_ringtone_text(message, text)
        return

    await message.reply_text(
        messages.FALLBACK_TEXT,
        reply_markup=keyboards.main_menu_keyboard(),
    )


@app.on_callback_query(
    filters.regex(rf"^{keyboards.PRESS_FLOW_CALLBACK_PREFIX}(generate|import)$")
)
async def press_flow_callback(_: Client, callback_query: CallbackQuery) -> None:
    if callback_query.from_user is None or callback_query.message is None:
        return

    user_id = callback_query.from_user.id
    action = callback_query.data.split(":")[1]

    if action == "generate":
        clear_press_pending(user_id)
        user_modes[user_id] = MODE_PRESS
        await callback_query.answer()
        await callback_query.message.reply_text(
            messages.PRESS_GENERATE_PROMPT_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return

    clear_press_pending(user_id)
    user_modes[user_id] = MODE_PRESS_IMPORT
    await callback_query.answer()
    await callback_query.message.reply_text(
        messages.PRESS_IMPORT_TEXT,
        reply_markup=keyboards.main_menu_keyboard(),
    )


@app.on_callback_query(filters.regex(f"^{keyboards.PRESS_EDIT_CALLBACK}$"))
async def press_edit_callback(_: Client, callback_query: CallbackQuery) -> None:
    if callback_query.from_user is None or callback_query.message is None:
        return

    user_id = callback_query.from_user.id
    if user_id not in press_pending:
        await callback_query.answer(
            "Сначала сгенерируй пресс-релиз",
            show_alert=True,
        )
        return

    user_modes[user_id] = MODE_PRESS_EDIT
    await callback_query.answer()
    await callback_query.message.reply_text(
        messages.PRESS_EDIT_PROMPT_TEXT,
        reply_markup=keyboards.main_menu_keyboard(),
    )


@app.on_callback_query(filters.regex(f"^{keyboards.COVER_GEN_EDIT_CALLBACK}$"))
async def cover_gen_edit_callback(_: Client, callback_query: CallbackQuery) -> None:
    if callback_query.from_user is None or callback_query.message is None:
        return

    user_id = callback_query.from_user.id
    if user_id not in cover_gen_pending:
        await callback_query.answer(
            "Сначала сгенерируй обложку",
            show_alert=True,
        )
        return

    user_modes[user_id] = MODE_COVER_GEN_EDIT
    await callback_query.answer()
    await callback_query.message.reply_text(
        messages.COVER_GEN_EDIT_PROMPT_TEXT,
        reply_markup=keyboards.main_menu_keyboard(),
    )


@app.on_callback_query(filters.regex(r"^ringtone_duration:(30|45|60)$"))
async def ringtone_duration_callback(_: Client, callback_query: CallbackQuery) -> None:
    if callback_query.from_user is None or callback_query.message is None:
        return

    user_id = callback_query.from_user.id
    duration_sec = int(callback_query.data.split(":")[1])
    pending = ringtone_pending.get(user_id)

    if not pending or pending.get("start_sec") is None:
        await callback_query.answer("Сначала укажи время начала", show_alert=True)
        return

    await callback_query.answer()
    await ask_ringtone_format(
        callback_query.message,
        pending,
        pending["start_sec"],
        duration_sec,
    )


@app.on_callback_query(filters.regex(r"^ringtone_format:(mp3|wav)$"))
async def ringtone_format_callback(_: Client, callback_query: CallbackQuery) -> None:
    if callback_query.from_user is None or callback_query.message is None:
        return

    user_id = callback_query.from_user.id
    output_format = callback_query.data.split(":")[1]
    pending = ringtone_pending.get(user_id)

    if (
        not pending
        or pending.get("start_sec") is None
        or pending.get("duration_sec") is None
    ):
        await callback_query.answer("Сначала укажи время и длительность", show_alert=True)
        return

    await callback_query.answer()
    await process_ringtone(
        callback_query.message,
        user_id,
        pending["start_sec"],
        pending["duration_sec"],
        output_format,
    )


@app.on_message(filters.photo)
async def handle_photo(client: Client, message: Message) -> None:
    track_user(message)
    mode = get_mode(message)
    if mode in {MODE_CONVERTER, MODE_COVER_GEN, MODE_COVER_GEN_EDIT}:
        wrong_text = messages.WRONG_MODE_COVER_TEXT
        if mode in {MODE_COVER_GEN, MODE_COVER_GEN_EDIT}:
            wrong_text = messages.COVER_GEN_WRONG_INPUT_TEXT
        await message.reply_text(
            wrong_text,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return
    if mode == MODE_RINGTONE:
        await message.reply_text(
            messages.WRONG_MODE_RINGTONE_TEXT,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return
    if mode is None:
        set_mode(message, MODE_COVER)
    await resize_and_reply(client, message)


@app.on_message(filters.document | filters.audio)
async def handle_media(client: Client, message: Message) -> None:
    track_user(message)
    mode = get_mode(message)

    if is_image_document(message):
        if mode in {MODE_CONVERTER, MODE_RINGTONE, MODE_COVER_GEN, MODE_COVER_GEN_EDIT}:
            wrong_text = messages.COVER_GEN_WRONG_INPUT_TEXT
            if mode == MODE_CONVERTER:
                wrong_text = messages.WRONG_MODE_COVER_TEXT
            elif mode == MODE_RINGTONE:
                wrong_text = messages.WRONG_MODE_RINGTONE_TEXT
            await message.reply_text(
                wrong_text,
                reply_markup=keyboards.main_menu_keyboard(),
            )
            return
        if mode is None:
            set_mode(message, MODE_COVER)
        await resize_and_reply(client, message)
        return

    if mode == MODE_RINGTONE:
        if not is_audio_media(message):
            await message.reply_text(
                messages.RINGTONE_INVALID_AUDIO_TEXT,
                reply_markup=keyboards.main_menu_keyboard(),
            )
            return
        await save_ringtone_audio(client, message)
        return

    if mode in {MODE_COVER, MODE_COVER_GEN, MODE_COVER_GEN_EDIT}:
        wrong_text = messages.WRONG_MODE_CONVERTER_TEXT
        if mode in {MODE_COVER_GEN, MODE_COVER_GEN_EDIT}:
            wrong_text = messages.COVER_GEN_WRONG_INPUT_TEXT
        await message.reply_text(
            wrong_text,
            reply_markup=keyboards.main_menu_keyboard(),
        )
        return
    if mode is None:
        set_mode(message, MODE_CONVERTER)
    await convert_and_reply(client, message)


@app.on_message(
    filters.all
    & ~filters.command(["start", "stats", "press", "gen"])
    & ~filters.text
    & ~filters.photo
    & ~filters.document
    & ~filters.audio
)
async def fallback_other(_: Client, message: Message) -> None:
    track_user(message)
    await message.reply_text(
        messages.FALLBACK_TEXT,
        reply_markup=keyboards.main_menu_keyboard(),
    )


if __name__ == "__main__":
    app.run()
