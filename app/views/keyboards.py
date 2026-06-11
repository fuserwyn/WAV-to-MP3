from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

BTN_COVER = "🖼 Обложка"
BTN_COVER_GEN = "✨ Генерация обложки"
BTN_PRESS = "📰 Пресс-релиз"
BTN_CONVERTER = "🎵 Конвертер"
BTN_RINGTONE = "📱 Рингтон"
BTN_MENU = "🏠 Меню"

MENU_BUTTONS = {
    BTN_COVER,
    BTN_COVER_GEN,
    BTN_PRESS,
    BTN_CONVERTER,
    BTN_RINGTONE,
    BTN_MENU,
}

RINGTONE_DURATION_CALLBACK_PREFIX = "ringtone_duration:"
RINGTONE_FORMAT_CALLBACK_PREFIX = "ringtone_format:"


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(BTN_COVER), KeyboardButton(BTN_COVER_GEN)],
            [KeyboardButton(BTN_PRESS), KeyboardButton(BTN_CONVERTER)],
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


def ringtone_format_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("MP3", callback_data=f"{RINGTONE_FORMAT_CALLBACK_PREFIX}mp3"),
                InlineKeyboardButton("WAV", callback_data=f"{RINGTONE_FORMAT_CALLBACK_PREFIX}wav"),
            ]
        ]
    )
