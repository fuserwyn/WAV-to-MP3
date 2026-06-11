from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

BTN_COVER = "🖼 Обложка"
BTN_PRESS = "📰 Пресс-релиз"
BTN_CONVERTER = "🎵 Конвертер"
BTN_RINGTONE = "📱 Рингтон"
BTN_MENU = "🏠 Меню"

MENU_BUTTONS = {BTN_COVER, BTN_PRESS, BTN_CONVERTER, BTN_RINGTONE, BTN_MENU}

RINGTONE_DURATION_CALLBACK_PREFIX = "ringtone_duration:"


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(BTN_COVER), KeyboardButton(BTN_PRESS)],
            [KeyboardButton(BTN_CONVERTER), KeyboardButton(BTN_RINGTONE)],
            [KeyboardButton(BTN_MENU)],
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
