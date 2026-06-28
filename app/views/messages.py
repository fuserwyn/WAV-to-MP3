BOT_NAME = "A&R Kit"


def start_text() -> str:
    return (
        f"Привет! Я {BOT_NAME} — бот для релизов и продакшена.\n\n"
        "Выбери режим кнопкой ниже:\n\n"
        "🖼 Обложка — квадратный формат или генерация через Nano Banana\n"
        "📰 Пресс-релиз — сгенерировать или доработать свой текст\n"
        "🎤 Описание артиста — расскажи о себе, соберу красивое bio\n"
        "🚀 Питчинг трека — опиши трек, соберу питч для плейлистов\n"
        "🎵 Конвертер — WAV ↔ MP3 (аудио или файлом)\n"
        "📱 Рингтон — нарезка с таймкода на 30/45/60 сек (MP3 или WAV)"
    )


COVER_MENU_TEXT = (
    "Режим: Обложка\n"
    "📐 Квадратный формат — ресайз фото до 3000–10000 px.\n"
    "✨ Генерация обложки — промпт или своё фото через Nano Banana."
)
COVER_MODE_TEXT = (
    "Режим: Квадратный формат\n"
    "Выбери размер, затем отправь фото или картинку файлом.\n"
    "Доступно: 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000 px."
)
COVER_PICK_SIZE_TEXT = "Сначала выбери размер кнопкой ниже."
COVER_GEN_MODE_TEXT = (
    "Режим: Генерация обложки\n"
    "✨ Сгенерировать — опиши обложку, создам с нуля.\n"
    "📷 Моё фото — пришли картинку, доработаю через Nano Banana."
)
COVER_GEN_GENERATE_PROMPT_TEXT = (
    "Опиши обложку одним сообщением — сгенерирую квадрат 3000×3000.\n"
    "После результата можно доредактировать кнопкой ✏️ или текстом.\n"
    "Пример: lo-fi обложка альбома, ночной город, неон, дождь"
)
COVER_GEN_IMPORT_TEXT = (
    "Пришли фото или картинку файлом — загружу для доработки.\n"
    "После загрузки опиши правки текстом или нажми ✏️."
)
COVER_GEN_PHOTO_UPLOADING_TEXT = "Загружаю фото..."
COVER_GEN_PHOTO_ERROR_TEXT = (
    "Не удалось загрузить фото. Попробуй другой файл (JPG, PNG, WebP)."
)
COVER_GEN_PHOTO_SAVED_TEXT = (
    "Фото загружено. Опиши правки или нажми ✏️ Доредактировать."
)
COVER_GEN_GENERATING_TEXT = "Генерирую обложку через Nano Banana..."
COVER_GEN_EDITING_TEXT = "Доредактирую обложку через Nano Banana..."
COVER_GEN_EDIT_PROMPT_TEXT = (
    "Опиши правки текстом.\n"
    "Пример: убери надпись LO-FI BEATS, добавь больше дождя"
)
COVER_GEN_NO_IMAGE_TEXT = (
    "Сначала сгенерируй обложку или пришли фото через 🖼 Обложка → Генерация."
)
COVER_GEN_NO_KEY_TEXT = "PoYo API не настроен. Добавь POYO_API_KEY в переменные окружения."
COVER_GEN_ERROR_TEXT = "Не удалось сгенерировать обложку. Попробуй другой промпт."
COVER_GEN_EDIT_ERROR_TEXT = "Не удалось доредактировать обложку. Попробуй другие правки."
COVER_GEN_SUCCESS_CAPTION = "Готово: обложка Nano Banana 3000×3000 (файл)"
COVER_GEN_PHOTO_SAVED_CAPTION = "Готово: фото загружено 3000×3000 (файл)"
COVER_GEN_EDIT_SUCCESS_CAPTION = "Готово: обложка отредактирована 3000×3000 (файл)"
WRONG_MODE_COVER_GEN_TEXT = (
    "Сейчас активен другой режим. Нажми 🖼 Обложка или 🏠 Меню."
)
COVER_GEN_WRONG_INPUT_TEXT = (
    "В режиме генерации отправь текстовый промпт.\n"
    "Для своего фото выбери 📷 Моё фото в меню генерации."
)
COVER_GEN_EDIT_WRONG_INPUT_TEXT = (
    "В режиме доработки отправь текстовый промпт с правками, не картинку."
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
ARTIST_MODE_TEXT = (
    "Режим: Описание артиста\n"
    "Расскажи о себе одним сообщением: имя/псевдоним, жанр, история, достижения, вайб.\n"
    "Соберу красивое и ёмкое bio. После результата можно доредактировать кнопкой ✏️ или текстом.\n"
    "Хочешь на английском — просто попроси."
)
ARTIST_GENERATING_TEXT = "Собираю описание артиста..."
ARTIST_EDITING_TEXT = "Доредактирую описание артиста..."
ARTIST_EDIT_PROMPT_TEXT = (
    "Опиши правки текстом.\n"
    "Пример: сделай короче, добавь про дебютный сингл, переведи на английский"
)
ARTIST_NO_TEXT_TEXT = (
    "Сначала собери описание через 🎤 Описание артиста."
)
ARTIST_ERROR_TEXT = "Не удалось собрать описание артиста. Попробуй позже."
ARTIST_EDIT_ERROR_TEXT = "Не удалось доредактировать описание. Попробуй другие правки."
PITCH_MODE_TEXT = (
    "Режим: Питчинг трека\n"
    "Опиши трек одним сообщением: название, жанр, настроение, звучание, фишку, "
    "похожих артистов, для каких плейлистов.\n"
    "Соберу короткий цепляющий питч для редакторов. После результата можно "
    "доредактировать кнопкой ✏️ или текстом.\n"
    "Хочешь на английском — просто попроси."
)
PITCH_GENERATING_TEXT = "Собираю питч трека..."
PITCH_EDITING_TEXT = "Доредактирую питч трека..."
PITCH_EDIT_PROMPT_TEXT = (
    "Опиши правки текстом.\n"
    "Пример: сделай короче, добавь референс на Billie Eilish, переведи на английский"
)
PITCH_NO_TEXT_TEXT = (
    "Сначала собери питч через 🚀 Питчинг трека."
)
PITCH_ERROR_TEXT = "Не удалось собрать питч трека. Попробуй позже."
PITCH_EDIT_ERROR_TEXT = "Не удалось доредактировать питч. Попробуй другие правки."
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
RINGTONE_DOWNLOADING_TEXT = "Получаю аудио, подожди..."
RINGTONE_DOWNLOAD_ERROR_TEXT = (
    "Не удалось скачать аудио. Отправь файл ещё раз "
    "или пришли трек напрямую, без пересылки."
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
WRONG_MODE_COVER_TEXT = (
    "Сейчас активен другой режим. Нажми 🖼 Обложка или 🏠 Меню."
)
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
RESIZING_TEXT = "Получил картинку, делаю {size}×{size}..."
IMAGE_SUCCESS_CAPTION = "Готово: {size}×{size} px (файл)"


def cover_size_selected_text(size: int) -> str:
    return f"Выбран размер {size}×{size}. Отправь фото или картинку файлом."


def resizing_text(size: int) -> str:
    return RESIZING_TEXT.format(size=size)


def image_success_caption(size: int) -> str:
    return IMAGE_SUCCESS_CAPTION.format(size=size)


IMAGE_ERROR_TEXT = "Не удалось обработать картинку."
FFMPEG_START_ERROR_TEXT = "Не удалось запустить ffmpeg."
CONVERT_ERROR_TEXT = "Ошибка конвертации. Проверь, что файл валидный."
def convert_success_caption(output_extension: str) -> str:
    if output_extension == ".wav":
        return "Готово: MP3 -> WAV (24-bit)"
    return "Готово: WAV -> MP3"
FALLBACK_TEXT = (
    "Выбери режим кнопкой: Обложка, Пресс-релиз, "
    "Конвертер или Рингтон."
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
