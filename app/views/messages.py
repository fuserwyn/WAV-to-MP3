BOT_NAME = "A&R Kit"


def start_text() -> str:
    return (
        f"Привет! Я {BOT_NAME} — бот для релизов и продакшена.\n\n"
        "Выбери режим кнопкой ниже:\n\n"
        "🖼 Обложка — фото → JPG 3000×3000 (файлом)\n"
        "✨ Генерация обложки — промпт → Nano Banana 3000×3000 (с доредактированием)\n"
        "📰 Пресс-релиз — сгенерировать или доработать свой текст\n"
        "🎵 Конвертер — WAV ↔ MP3 (аудио или файлом)\n"
        "📱 Рингтон — нарезка с таймкода на 30/45/60 сек (MP3 или WAV)"
    )


COVER_MODE_TEXT = (
    "Режим: Обложка\n"
    "Отправь фото или картинку файлом — верну JPG 3000×3000 px."
)
COVER_GEN_MODE_TEXT = (
    "Режим: Генерация обложки\n"
    "Опиши обложку одним сообщением — сгенерирую квадрат 3000×3000 через Nano Banana.\n"
    "После результата можно доредактировать кнопкой ✏️ или текстом.\n"
    "Пример: lo-fi обложка альбома, ночной город, неон, дождь"
)
COVER_GEN_GENERATING_TEXT = "Генерирую обложку через Nano Banana..."
COVER_GEN_EDITING_TEXT = "Доредактирую обложку через Nano Banana..."
COVER_GEN_EDIT_PROMPT_TEXT = (
    "Опиши правки текстом.\n"
    "Пример: убери надпись LO-FI BEATS, добавь больше дождя"
)
COVER_GEN_NO_IMAGE_TEXT = (
    "Сначала сгенерируй обложку через ✨ Генерация обложки."
)
COVER_GEN_NO_KEY_TEXT = "PoYo API не настроен. Добавь POYO_API_KEY в переменные окружения."
COVER_GEN_ERROR_TEXT = "Не удалось сгенерировать обложку. Попробуй другой промпт."
COVER_GEN_EDIT_ERROR_TEXT = "Не удалось доредактировать обложку. Попробуй другие правки."
COVER_GEN_SUCCESS_CAPTION = "Готово: обложка Nano Banana 3000×3000 (файл)"
COVER_GEN_EDIT_SUCCESS_CAPTION = "Готово: обложка отредактирована 3000×3000 (файл)"
WRONG_MODE_COVER_GEN_TEXT = (
    "Сейчас активен другой режим. Нажми ✨ Генерация обложки или 🏠 Меню."
)
COVER_GEN_WRONG_INPUT_TEXT = (
    "В режиме генерации отправь текстовый промпт, не картинку."
)
PRESS_MODE_TEXT = (
    "Режим: Пресс-релиз\n"
    "✨ Сгенерировать — опиши релиз, напишу текст с нуля.\n"
    "📄 Мой текст — пришли готовый релиз, доработаю по правкам."
)
PRESS_GENERATE_PROMPT_TEXT = (
    "Опиши релиз одним сообщением — сгенерирую текст.\n"
    "После результата можно доредактировать кнопкой ✏️ или текстом."
)
PRESS_IMPORT_TEXT = (
    "Пришли текст своего пресс-релиза одним сообщением.\n"
    "Сохраню его и смогу доработать по твоим правкам."
)
PRESS_SAVED_TEXT = "Текст сохранён. Опиши правки или нажми ✏️ Доредактировать."
PRESS_IMPORT_EMPTY_TEXT = "Пришли непустой текст пресс-релиза."
PRESS_EDIT_PROMPT_TEXT = (
    "Опиши правки текстом.\n"
    "Пример: сделай тон короче, добавь цитату артиста, убери блок контактов"
)
PRESS_EDITING_TEXT = "Доредактирую пресс-релиз..."
PRESS_NO_TEXT_TEXT = (
    "Сначала сгенерируй релиз или пришли свой текст через 📰 Пресс-релиз."
)
PRESS_EDIT_ERROR_TEXT = "Не удалось доредактировать пресс-релиз. Попробуй другие правки."
CONVERTER_MODE_TEXT = (
    "Режим: Конвертер\n"
    "Отправь WAV или MP3 — как трек или файлом.\n"
    "WAV → MP3, MP3 → WAV (24-bit)."
)
RINGTONE_MODE_TEXT = (
    "Режим: Рингтон\n"
    "1. Отправь аудио (трек или файлом)\n"
    "2. Укажи время начала и длину:\n"
    "   • `1:30 45` — с 1:30 на 45 сек\n"
    "   • `90 60` — с 90-й сек на 60 сек\n"
    "   • или время, затем кнопки 30/45/60 и формат MP3/WAV"
)
RINGTONE_AUDIO_SAVED_TEXT = (
    "Аудио получил.\n"
    "Укажи время начала и длительность (30, 45 или 60 сек).\n"
    "Пример: `1:30 45`, затем выбери MP3 или WAV"
)
RINGTONE_PICK_DURATION_TEXT = "Выбери длительность кнопкой ниже:"
RINGTONE_PICK_FORMAT_TEXT = "Выбери формат выхода:"
RINGTONE_INVALID_INPUT_TEXT = (
    "Не понял формат.\n"
    "Пример: `1:30 45` или `90 60`"
)
RINGTONE_NO_AUDIO_TEXT = "Сначала отправь аудио в режиме Рингтон."
RINGTONE_CUTTING_TEXT = "Нарезаю рингтон..."
RINGTONE_ERROR_TEXT = "Не удалось нарезать рингтон. Проверь таймкод и файл."
RINGTONE_INVALID_AUDIO_TEXT = "Нужен аудиофайл (MP3, WAV и др.)."
def ringtone_success_caption(
    start_sec: float, duration_sec: int, output_format: str
) -> str:
    fmt = output_format.upper()
    return f"Готово: рингтон {fmt}, {duration_sec} сек с {format_timecode(start_sec)}"
MENU_TEXT = "Главное меню. Выбери режим кнопкой ниже."
WRONG_MODE_COVER_TEXT = "Сейчас активен другой режим. Нажми 🖼 Обложка или 🏠 Меню."
WRONG_MODE_CONVERTER_TEXT = "Сейчас активен другой режим. Нажми 🎵 Конвертер или 🏠 Меню."
WRONG_MODE_RINGTONE_TEXT = "Сейчас активен другой режим. Нажми 📱 Рингтон или 🏠 Меню."


def format_timecode(seconds: float) -> str:
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


INVALID_EXTENSION_TEXT = "Нужен файл с расширением .wav или .mp3"
CONVERTING_TEXT = "Получил файл, конвертирую..."
RESIZING_TEXT = "Получил картинку, делаю 3000×3000..."
IMAGE_ERROR_TEXT = "Не удалось обработать картинку."
IMAGE_SUCCESS_CAPTION = "Готово: 3000×3000 px (файл)"
FFMPEG_START_ERROR_TEXT = "Не удалось запустить ffmpeg."
CONVERT_ERROR_TEXT = "Ошибка конвертации. Проверь, что файл валидный."
def convert_success_caption(output_extension: str) -> str:
    if output_extension == ".wav":
        return "Готово: MP3 -> WAV (24-bit)"
    return "Готово: WAV -> MP3"
FALLBACK_TEXT = (
    "Выбери режим кнопкой: Обложка, Генерация обложки, "
    "Пресс-релиз, Конвертер или Рингтон."
)
PRESS_USAGE_TEXT = "Использование: /press описание для пресс-релиза"
PRESS_NO_KEY_TEXT = "OpenRouter не настроен. Добавь OPEN_ROUTER_KEY в переменные окружения."
PRESS_GENERATING_TEXT = "Генерирую пресс-релиз..."
PRESS_ERROR_TEXT = "Не удалось сгенерировать пресс-релиз. Попробуй позже."


def file_too_big_text(max_mb: int) -> str:
    return (
        "Файл слишком большой.\n"
        f"Отправь файл размером до {max_mb} МБ."
    )


FILE_TOO_BIG_TEXT = file_too_big_text(50)


def stats_text(rows: list[tuple], total_users: int, total_conversions: int) -> str:
    lines = [
        f"Пользователей: {total_users}",
        f"Всего конвертаций: {total_conversions}",
        "",
        f"Последние {len(rows)} активных пользователей:",
    ]

    for user_id, username, first_name, last_name, conversions_count, last_seen_at in rows:
        display_name = " ".join(
            part for part in [first_name or "", last_name or ""] if part
        ).strip()
        if not display_name:
            display_name = username or str(user_id)
        username_part = f"@{username}" if username else "без username"
        lines.append(
            f"- {display_name} ({username_part}) | id={user_id} | "
            f"конвертаций={conversions_count} | last_seen={last_seen_at}"
        )

    return "\n".join(lines)
