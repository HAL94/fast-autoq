

from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel, Field

from common.mixins import TruncatedFloat


class LineItemSchema(BaseModel):
    id: int
    seller_id: int
    purchase_price: TruncatedFloat
    qty: int
    total: TruncatedFloat

class OrderSchema(BaseModel):
    id: int
    external_id: str
    fulfillment_status: str
    payment_status: str
    cart_id: int
    customer_id: int
    email: str
    phone: str
    currency_code: str
    tax_rate: TruncatedFloat
    canceld_at: Optional[datetime]
    created_date: datetime
    updated_at: datetime
    seller_id: int
    order_amount: TruncatedFloat
    order_items: Optional[List["LineItemSchema"]] = Field(default=[])


class GetOrders(BaseModel):
    orders: List[OrderSchema]


class CreateOrder(BaseModel):
    external_id: str
    fulfillment_status: str
    payment_status: str
    cart_id: int
    customer_id: int
    email: str
    phone: str
    currency_code: str
    tax_rate: TruncatedFloat
    seller_id: int
    order_amount: TruncatedFloat
    order_items: Optional[List[LineItemSchema]] = Field(default=[])
