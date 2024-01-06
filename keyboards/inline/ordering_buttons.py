from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.data_query import create_call_back
from loader import db


# product - (1, '2023-12-14 12:53:34.054650', '2023-12-14 12:54:10.269572', 'Qizil olma', 'Judayam foydali', 12000, 1, None)

async def categories_markup(category_id='0', subcategory_id='0', product_id='0'):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)
    categories = db.select_categories()
    for category in categories:
        markup.insert(InlineKeyboardButton(
            text=category[1],
            callback_data=await create_call_back(CURRENT_LEVEL+1, category[0], subcategory_id, product_id)
        ))
    markup.row(InlineKeyboardButton(
        text=" ❌ ",
        callback_data=await create_call_back(CURRENT_LEVEL-1)
    ))
    return markup


async def subcategories_markup(category_id, subcategory_id, product_id):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)
    subcategories = db.select_sub_categories(category_id)
    for subcategory in subcategories:
        markup.insert(InlineKeyboardButton(
            text=subcategory[1],
            callback_data=await create_call_back(CURRENT_LEVEL + 1, subcategory[2], subcategory[0], product_id)
        ))
    markup.insert(InlineKeyboardButton(
        text="🔙 Ortga",
        callback_data=await create_call_back(CURRENT_LEVEL - 1)
    ))
    return markup


async def products_markup(category_id, subcategory_id, product_id):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    products = db.select_products(subcategory_id)
    for product in products:
        markup.insert(InlineKeyboardButton(
            text=f"{product[3]} - {product[7]}so'm",
            callback_data=await create_call_back(CURRENT_LEVEL+1, category_id, subcategory_id, product[0])
        ))
    markup.insert(InlineKeyboardButton(
        text="🔙 Ortga",
        callback_data=await create_call_back(CURRENT_LEVEL - 1, category_id)
    ))
    return markup


async def product_markup(category_id, subcategory_id, product_id, user_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=3)
    product = db.select_product(product_id)
    order_product = db.select_order_product(user_id, product_id)
    if order_product:
        markup.insert(InlineKeyboardButton(
            text=' ➖ ',
            callback_data=await create_call_back(CURRENT_LEVEL+2, category_id, subcategory_id, product_id)
        ))
        markup.insert(InlineKeyboardButton(
            text=f'🛒 {order_product[3]}',
            callback_data='order'
        ))
        markup.insert(InlineKeyboardButton(
            text=' ➕ ',
            callback_data=await create_call_back(CURRENT_LEVEL+1, category_id, subcategory_id, product_id)
        ))
    else:
        markup.insert(InlineKeyboardButton(
            text="Savatga qo'shish",
            callback_data=await create_call_back(CURRENT_LEVEL+1, category_id, subcategory_id, product_id)
        ))
    markup.row(InlineKeyboardButton(
        text="🔙 Ortga",
        callback_data=await create_call_back(CURRENT_LEVEL-1, category_id, subcategory_id, product_id)
    ))
    return markup
