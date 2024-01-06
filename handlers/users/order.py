from aiogram import types
from aiogram.types import LabeledPrice

from data.shipping_options import ordinary_delivery, fast_delivery, regular_delivery, pickup_delivery
from handlers.users.ordering import send_categories
from keyboards.inline import create_order_button, call_back_data_order, payment_data, \
    payment_method_buttons
from loader import dp, db, bot
from utils.db_api.product import Product
from data.config import PROVIDER_TOKEN_CLICK, PROVIDER_TOKEN_PAYME, ADMINS


# id, created_time, update_time, count, product_id, user_id, paid
# product - (13, '2024-01-04 16:55:47.767555', '2024-01-04 16:55:47.767555', 2, 1, 2, 0)

@dp.message_handler(text='Savat')
async def show_order(message, *args, **kwargs):
    if isinstance(message, types.Message):
        answer = True
        tg_id = message.from_user.id
        user_id = db.select_user(tg_id)[0]
    else:
        answer = False
        user_id = kwargs.get('user_id')
        message = message.message
    all_orders = db.select_order_product_all(user_id)
    info = f"Savatdagi mahsulotlar:\n\n"
    summa = 0
    products_list = []
    for order_product in all_orders:
        product = db.select_product(order_product[4])
        # product - id, cre, upd, name, desc, photo, sub, price
        name = product[3]
        count = order_product[3]
        price = product[7]
        info += f"{name}: {count} x {price} = {count * price} so'm\n"
        summa += count * price
        products_list.append(
            {'product_id': product[0],
             'user_id': user_id,
             'product_name': name,
             'count': count}
        )
    info += f"\nUmumiy summa: {summa} so'm"
    if answer:
        await message.answer(f"{info}",
                             reply_markup=await create_order_button(products_list))
    else:
        await message.edit_text(f"{info}",
                                reply_markup=await create_order_button(products_list))


async def remove_order_product(call: types.CallbackQuery, product_id, user_id,
                               product_name, count, *args, **kwargs):
    db.remove_product(product_id, user_id)
    await show_order(call, user_id=user_id)


async def add_order_product(call: types.CallbackQuery, product_id, user_id,
                            product_name, count, *args, **kwargs):
    db.add_product(product_id, user_id)
    await show_order(call, user_id=user_id)


async def remove_order(call: types.CallbackQuery, *args, **kwargs):
    tg_id = call.from_user.id
    user_id = db.select_user(tg_id)[0]
    db.clear_order_products(user_id)
    await call.message.edit_text('Savatdagi barcha mahsulotlar o\'chirildi!',
                                 reply_markup=await create_order_button([]))


async def close_order(call: types.CallbackQuery, *args, **kwargs):
    await call.message.delete()


async def payment_method(call: types.CallbackQuery, *args, **kwargs):
    user_id = db.select_user(call.from_user.id)[0]
    order_id = db.select_order(user_id)[0]
    await call.message.edit_text("To'lov turini tanlang!",
                                 reply_markup=await payment_method_buttons(order_id))


@dp.callback_query_handler(call_back_data_order.filter())
async def select_order_func(call: types.CallbackQuery, callback_data: dict):
    level = callback_data.get('level')
    product_id = callback_data.get('product_id')
    user_id = callback_data.get('user_id')
    product_name = callback_data.get('product_name')
    count = callback_data.get('count')
    if level == '-1':
        current_func = remove_order_product
    elif level == '1':
        current_func = add_order_product
    elif level == '2':
        current_func = send_categories
    elif level == '3':
        current_func = remove_order
    elif level == '4':
        current_func = payment_method
    else:
        current_func = close_order
    await current_func(call, product_id, user_id, product_name, count)


@dp.callback_query_handler(payment_data.filter())
async def send_invoice(call: types.CallbackQuery, callback_data: dict):
    method = callback_data.get('method')
    order_id = callback_data.get('order_id')
    order_products = db.select_order_products(order_id)
    description = str()
    summa = 0
    for order_product in order_products:
        order_product = db.select_order_product_id(order_product[2])
        product = db.select_product(order_product[4])
        name = product[3]
        count = order_product[3]
        price = product[7]
        description += f"\n{name}: {count} ta;\n"
        summa += count * price

    tg_id = call.from_user.id
    user_id = db.select_user(tg_id)[0]
    order = db.select_order(user_id)
    title = "Mahsulot sotib olish"
    payload = order[0]
    prices = [LabeledPrice(label="Umumiy summa", amount=summa*100)]
    photo = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fclick.uz%2F&psig=AOvVaw3_x6wFsaEbh5nBcAwHovV3&ust=1703505335145000&source=images&cd=vfe&opi=89978449&ved=0CA8QjRxqFwoTCOjNz4yCqIMDFQAAAAAdAAAAABAD"
    product = Product(title=title, description=description, payload=payload,
                      currency="UZS", prices=prices, start_parameter='123456',
                      photo_url=photo, photo_width=850, photo_height=425,
                      need_name=True, need_phone_number=True,
                      need_shipping_address=True, is_flexible=True)
    await bot.send_invoice(tg_id,
                           **product.generate_dict, )


@dp.shipping_query_handler()
async def shipping_option(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        error_message="Chetga yubora olmaymiz!",
                                        ok=False)
    elif query.shipping_address.city.lower() in ['toshkent', 'tashkent']:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[pickup_delivery,
                                                          fast_delivery,
                                                          regular_delivery,
                                                          ordinary_delivery],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[regular_delivery,
                                                          ordinary_delivery],
                                        ok=True)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    tg_id = pre_checkout_query.from_user.id
    user_id = db.select_user(tg_id)[0]
    shipping_day = pre_checkout_query.shipping_option_id
    if shipping_day == 'pickup':
        delta_day = None
    elif shipping_day == 'fast':
        delta_day = 1 / 24
    elif shipping_day == 'regular':
        delta_day = 1
    else:
        delta_day = 3
    exp_time = db.close_order(user_id, delta_day)
    text = f"Xaridingiz uchun rahmat!\n"
    text += f"Yetkazib berish vaqti: {exp_time}" if delta_day else ""
    db.paid_order_product_all(user_id)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text=text)
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Telegram user: {pre_checkout_query.from_user.first_name}\n"
                                f"To'landi: {pre_checkout_query.total_amount/100} {pre_checkout_query.currency}\n"
                                f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}")
