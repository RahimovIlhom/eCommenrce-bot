from aiogram import types
from aiogram.utils.exceptions import BadRequest

from keyboards.inline import categories_markup, call_back_data, subcategories_markup, products_markup, product_markup
from loader import dp, db


async def close_menu(call: types.CallbackQuery, *args, **kwargs):
    await call.message.delete()


@dp.message_handler(text=['Menu'])
async def send_categories(message, *args, **kwargs):
    if isinstance(message, types.Message):
        await message.answer("Bo'limni tanlang: ",
                             reply_markup=await categories_markup())
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text("Categoriyani tanlang: ",
                                     reply_markup=await categories_markup())


async def send_subcategories(call: types.CallbackQuery, category_id, subcategory_id, product_id, *args, **kwargs):
    await call.message.edit_text(f"Mahsulot turini tanlang: ",
                                 reply_markup=await subcategories_markup(category_id, subcategory_id, product_id))


async def send_products(call: types.CallbackQuery, category_id, subcategory_id, product_id):
    await call.message.delete()
    await call.message.answer(f"Mahsulotni tanlang: ",
                              reply_markup=await products_markup(category_id, subcategory_id, product_id))


# product - (1, '2023-12-14 12:53:34.054650', '2023-12-14 12:54:10.269572', 'Qizil olma', 'Judayam foydali', 12000, 1, None)
async def send_product(call: types.CallbackQuery, category_id, subcategory_id, product_id):
    product = db.select_product(product_id)
    subcategory_name = db.select_subcategory(product[6])
    info = f"Mahsulot turi: {subcategory_name}\n\n" \
           f"Mahsulot: {product[3]}\n\n" \
           f"{product[4]}\n\n" \
           f"Narxi: {product[5]}"
    await call.message.delete()
    try:
        await call.message.answer_photo(photo=product[-1], caption=info,
                                        reply_markup=await product_markup(category_id, subcategory_id, product_id))
    except BadRequest:
        await call.message.answer(info, reply_markup=await product_markup(category_id, subcategory_id, product_id))


async def order_product(call: types.Message, *args, **kwargs):
    pass


@dp.callback_query_handler(call_back_data.filter())
async def select_func(call: types.CallbackQuery, callback_data: dict):
    level = callback_data.get('level')
    category_id = callback_data.get('category')
    subcategory_id = callback_data.get('subcategory')
    product_id = callback_data.get('product')
    if level == '0':
        func_name = send_categories
    elif level == '1':
        func_name = send_subcategories
    elif level == '2':
        func_name = send_products
    elif level == '3':
        func_name = send_product
    elif level == '4':
        func_name = order_product
    else:
        func_name = close_menu
    await func_name(call, category_id, subcategory_id, product_id)
