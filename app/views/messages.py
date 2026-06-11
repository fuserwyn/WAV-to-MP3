def start_text() -> str:
    return (
        "Привет! Я мультитул для музыки, картинок и текстов.\n\n"
        "Что умею:\n\n"
        "🎵 Аудио\n"
        "Отправь WAV или MP3 — как трек (с play) или файлом.\n"
        "• WAV → MP3\n"
        "• MP3 → WAV (24-bit)\n"
        "Имя файла сохраняется.\n\n"
        "🖼 Картинки\n"
        "Отправь фото или изображение файлом — верну JPG 3000×3000 px "
        "(масштабирую с сохранением пропорций, отдаю файлом).\n\n"
        "📰 Пресс-релизы\n"
        "/press описание — сгенерирую готовый пресс-релиз по твоему промпту.\n\n"
        "📊 Статистика\n"
        "/stats — сколько пользователей и конвертаций.\n\n"
        "Просто отправь файл или команду — разберусь."
    )


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
FALLBACK_TEXT = "Отправь WAV/MP3 (аудио или файлом) или картинку."
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
