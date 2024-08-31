

import datetime
from pydantic import BaseModel, Field


class CreateOrder(BaseModel):
    external_id: str
    fulfillment_status: str
    payment_status: str
    cart_id: int
    customer_id: int
    email: str
    phone: str
    currency_code: str
    tax_rate: float
    seller_id: int
    order_amount: float
