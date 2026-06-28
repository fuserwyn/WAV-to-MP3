from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from app.services.image_processor import COVER_SIZES

BTN_COVER = "🖼 Обложка"
BTN_COVER_GEN = "✨ Генерация обложки"
BTN_PRESS = "📰 Пресс-релиз"
BTN_ARTIST = "🎤 Описание артиста"
BTN_PITCH = "🚀 Питчинг трека"
BTN_CONVERTER = "🎵 Конвертер"
BTN_RINGTONE = "📱 Рингтон"
BTN_MENU = "🏠 Меню"

MENU_BUTTONS = {
    BTN_COVER,
    BTN_COVER_GEN,
    BTN_PRESS,
    BTN_ARTIST,
    BTN_PITCH,
    BTN_CONVERTER,
    BTN_RINGTONE,
    BTN_MENU,
}

RINGTONE_DURATION_CALLBACK_PREFIX = "ringtone_duration:"
RINGTONE_FORMAT_CALLBACK_PREFIX = "ringtone_format:"
COVER_GEN_EDIT_CALLBACK = "cover_gen_edit"
COVER_FLOW_CALLBACK_PREFIX = "cover_flow:"
COVER_SIZE_CALLBACK_PREFIX = "cover_size:"
PRESS_EDIT_CALLBACK = "press_edit"
PRESS_FLOW_CALLBACK_PREFIX = "press_flow:"
ARTIST_EDIT_CALLBACK = "artist_edit"
PITCH_EDIT_CALLBACK = "pitch_edit"


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(BTN_COVER), KeyboardButton(BTN_COVER_GEN)],
            [KeyboardButton(BTN_PRESS), KeyboardButton(BTN_ARTIST)],
            [KeyboardButton(BTN_PITCH), KeyboardButton(BTN_CONVERTER)],
            [KeyboardButton(BTN_RINGTONE), KeyboardButton(BTN_MENU)],
        ],
        resize_keyboard=True,
    )


def ringtone_duration_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("30 сек", callback_data=f"{RINGTONE_DURATION_CALLBACK_PREFIX}30"),
                InlineKeyboardButton("45 сек", callback_data=f"{RINGTONE_DURATION_CALLBACK_PREFIX}45"),
                InlineKeyboardButton("60 сек", callback_data=f"{RINGTONE_DURATION_CALLBACK_PREFIX}60"),
            ]
        ]
    )


def press_mode_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✨ Сгенерировать",
                    callback_data=f"{PRESS_FLOW_CALLBACK_PREFIX}generate",
                ),
                InlineKeyboardButton(
                    "📄 Мой текст",
                    callback_data=f"{PRESS_FLOW_CALLBACK_PREFIX}import",
                ),
            ]
        ]
    )


def press_result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✏️ Доредактировать",
                    callback_data=PRESS_EDIT_CALLBACK,
                )
            ]
        ]
    )


def artist_result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✏️ Доредактировать",
                    callback_data=ARTIST_EDIT_CALLBACK,
                )
            ]
        ]
    )


def pitch_result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✏️ Доредактировать",
                    callback_data=PITCH_EDIT_CALLBACK,
                )
            ]
        ]
    )


def cover_size_keyboard() -> InlineKeyboardMarkup:
    rows = []
    for index in range(0, len(COVER_SIZES), 2):
        chunk = COVER_SIZES[index : index + 2]
        rows.append(
            [
                InlineKeyboardButton(
                    f"{size}×{size}",
                    callback_data=f"{COVER_SIZE_CALLBACK_PREFIX}{size}",
                )
                for size in chunk
            ]
        )
    return InlineKeyboardMarkup(rows)


def cover_mode_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✨ Сгенерировать",
                    callback_data=f"{COVER_FLOW_CALLBACK_PREFIX}generate",
                ),
                InlineKeyboardButton(
                    "📷 Моё фото",
                    callback_data=f"{COVER_FLOW_CALLBACK_PREFIX}import",
                ),
            ]
        ]
    )


def cover_gen_result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✏️ Доредактировать",
                    callback_data=COVER_GEN_EDIT_CALLBACK,
                )
            ]
        ]
    )


def ringtone_format_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("MP3", callback_data=f"{RINGTONE_FORMAT_CALLBACK_PREFIX}mp3"),
                InlineKeyboardButton("WAV", callback_data=f"{RINGTONE_FORMAT_CALLBACK_PREFIX}wav"),
            ]
        ]
    )
