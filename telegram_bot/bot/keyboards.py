from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_buttons: list = [
    [KeyboardButton(text="/CreateQR")],
    [KeyboardButton(text="/buy")]
]

menu_keyboard = ReplyKeyboardMarkup(keyboard=menu_buttons)
