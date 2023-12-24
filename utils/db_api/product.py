from dataclasses import dataclass

from aiogram.types import LabeledPrice

from data.config import PROVIDER_TOKEN_CLICK


@dataclass
class Product:
    title: str
    description: str
    payload: str
    currency: str
    prices: list[LabeledPrice]
    max_tip_amount: int = None
    suggested_tip_amounts: list[int] = None
    start_parameter: str = None
    provider_data: str = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    need_name: bool = False
    need_phone_number: bool = False
    need_email: bool = False
    need_shipping_address: bool = False
    send_phone_number_to_provider: bool = False
    send_email_to_provider: bool = False
    is_flexible: bool = False

    provider_token: str = PROVIDER_TOKEN_CLICK

    @property
    def generate_dict(self):
        return self.__dict__
