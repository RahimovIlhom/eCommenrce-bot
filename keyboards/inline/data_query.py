from aiogram.utils.callback_data import CallbackData

call_back_data = CallbackData('orderProduct', 'level', 'category', 'subcategory', 'product')
call_back_data_order = CallbackData('orderPayment', 'level', 'product_id', 'user_id', 'product_name', 'count')

payment_data = CallbackData('payment', 'method', 'order_id')


async def create_call_back(level, category='0', subcategory='0', product='0'):
    data = call_back_data.new(level=level, category=category, subcategory=subcategory, product=product)
    return data


async def create_call_back_order(level, product_id='0', user_id='0', product_name='0', count='0'):
    data = call_back_data_order.new(level=level, product_id=product_id, user_id=user_id, product_name=product_name, count=count)
    return data


async def create_payment_data(payment_method, order_id):
    data = payment_data.new(method=payment_method, order_id=order_id)
    return data
