from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup

BTN_COVER = "🖼 Обложка"
BTN_PRESS = "📰 Пресс-релиз"
BTN_CONVERTER = "🎵 Конвертер"
BTN_MENU = "🏠 Меню"

MENU_BUTTONS = {BTN_COVER, BTN_PRESS, BTN_CONVERTER, BTN_MENU}


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(BTN_COVER), KeyboardButton(BTN_PRESS)],
            [KeyboardButton(BTN_CONVERTER), KeyboardButton(BTN_MENU)],
        ],
        resize_keyboard=True,
    )
