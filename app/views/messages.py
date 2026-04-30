def start_text() -> str:
    return (
        "Привет! Отправь мне WAV-файл как документ, и я верну его в MP3.\n"
        "Для статистики: /stats"
    )


INVALID_EXTENSION_TEXT = "Нужен файл с расширением .wav"
CONVERTING_TEXT = "Получил файл, конвертирую..."
FFMPEG_START_ERROR_TEXT = "Не удалось запустить ffmpeg."
CONVERT_ERROR_TEXT = "Ошибка конвертации. Проверь, что это валидный WAV."
CONVERT_SUCCESS_CAPTION = "Готово: WAV -> MP3"
FALLBACK_TEXT = "Отправь WAV-файл как документ."


def file_too_big_text(max_mb: int) -> str:
    return (
        "Файл слишком большой.\n"
        f"Отправь WAV размером до {max_mb} МБ."
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
