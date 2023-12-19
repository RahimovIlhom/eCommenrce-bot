from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Menu')]
    ],
    resize_keyboard=True
)