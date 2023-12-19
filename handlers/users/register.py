from aiogram import types
from aiogram.types import ContentType

from keyboards.default import menu
from loader import dp, db


@dp.message_handler(content_types=[ContentType.CONTACT])
async def send_phone(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name
    phone = message.contact.phone_number
    profile_url = message.from_user.mention
    db.add_user(tg_id, username, fullname, phone, profile_url)
    await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz.\n"
                         "Xariq qilish uchun Menu tugmasini bosing!", reply_markup=menu)
