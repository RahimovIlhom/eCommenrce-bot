from aiogram import types
from aiogram.types import ContentType

from loader import dp


@dp.message_handler(content_types=[ContentType.PHOTO])
async def send_product_photo(msg: types.Message):
    await msg.answer(f"{msg.photo[-1].file_id}")


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)
