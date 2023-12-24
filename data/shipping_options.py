from aiogram.types import ShippingOption, LabeledPrice


pickup_delivery = ShippingOption(
    id='pickup',
    title='Do\'kondan olib ketish',
    prices=[LabeledPrice(label="Yektazib berish", amount=0)]
)
fast_delivery = ShippingOption(
    id='fast',
    title="1 soat ichida yetkazib berish",
    prices=[LabeledPrice(label='Yektazib berish', amount=2000000)]
)

regular_delivery = ShippingOption(
    id='regular',
    title='1 kun ichida yetkazib berish',
    prices=[LabeledPrice(label="Yektazib berish", amount=1000000)]
)
ordinary_delivery = ShippingOption(
    id='ordinary',
    title='3 kun ichida yetkazib berish',
    prices=[LabeledPrice(label="Yektazib berish", amount=500000)]
)
