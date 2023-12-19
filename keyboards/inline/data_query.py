from aiogram.utils.callback_data import CallbackData

call_back_data = CallbackData('orderProduct', 'level', 'category', 'subcategory', 'product')


async def create_call_back(level, category='0', subcategory='0', product='0'):
    data = call_back_data.new(level=level, category=category, subcategory=subcategory, product=product)
    return data
