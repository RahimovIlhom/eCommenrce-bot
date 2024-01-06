from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .data_query import call_back_data_order, create_call_back_order, create_payment_data


# product_id, user_id, product_name, count
async def create_order_button(products: list[dict]):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=3)
    for product in products:
        markup.insert(InlineKeyboardButton(
            text=" ➖ ",
            callback_data=await create_call_back_order(level=CURRENT_LEVEL-1, **product)
        ))
        markup.insert(InlineKeyboardButton(
            text=f"{product['product_name']} - {product['count']}",
            callback_data='product',
        ))
        markup.insert(InlineKeyboardButton(
            text=" ➕ ",
            callback_data=await create_call_back_order(level=CURRENT_LEVEL+1, **product)
        ))
    markup.row(InlineKeyboardButton(
        text='Yana xarid qilish',
        callback_data=await create_call_back_order(level=CURRENT_LEVEL+2)
    ))
    if products:
        markup.row(InlineKeyboardButton(
            text='Savatni tozalash',
            callback_data=await create_call_back_order(level=CURRENT_LEVEL+3)
        ))
        markup.row(InlineKeyboardButton(
            text="Sotib olish",
            callback_data=await create_call_back_order(level=CURRENT_LEVEL + 4)
        ))
    return markup


async def payment_method_buttons(order_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(
        text='Click',
        callback_data=await create_payment_data('click', order_id)
    ))
    markup.insert(InlineKeyboardButton(
        text='Payme',
        callback_data=await create_payment_data('payme', order_id)
    ))
    return markup
