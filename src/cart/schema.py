
from decimal import Decimal
from pydantic import BaseModel, Field

from common.mixins import TwoDecimalPlacesMixin
from db.models import CartStatusValues


class CartItemAdd(BaseModel):
    product_id: int
    seller_id: int
    qty: int = 1


class GetCart(BaseModel):
    cart_id: int
    status: CartStatusValues
    total_amount: Decimal = Field(decimal_places=2)
    cart: list["CartItem"]

class CartItem(BaseModel):
    id: int
    product_id: int
    seller_id: int
    purchase_price: Decimal = Field(decimal_places=2)
    qty: int
    total: Decimal = Field(decimal_places=2)

class ClearCart(BaseModel):
    success: bool