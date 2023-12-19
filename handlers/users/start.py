from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu, phone_button
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    user = db.select_user(user_id)
    if user is None:
        info = f"Salom, {message.from_user.full_name}!\n" \
               f"Botimizdan foydalanish uchun telefon raqamingizni yuboring!"
        await message.reply(info, reply_markup=phone_button)
    else:
        await message.answer(f"Xarid qilish uchun 'Menu' tugmasini bosing!", reply_markup=menu)
