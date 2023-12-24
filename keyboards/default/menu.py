from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Menu'),
            KeyboardButton(text="Savat"),
        ]
    ],
    resize_keyboard=True
)