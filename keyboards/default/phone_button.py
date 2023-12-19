from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


phone_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Telefon raqamni ulashish', request_contact=True)]
    ],
    resize_keyboard=True
)
