from pydantic import BaseModel

from common.mixins import TruncatedFloat
from db.models import CartStatusValues

class CartItemAdd(BaseModel):
    product_id: int
    seller_id: int
    qty: int = 1


class GetCart(BaseModel):
    cart_id: int
    status: CartStatusValues
    total_amount: TruncatedFloat
    cart: list["CartItem"]
    # _total_amount = field_validator('total_amount')(decimals_normalize)


class CartItem(BaseModel):
    id: int
    product_id: int
    seller_id: int
    
    purchase_price: TruncatedFloat
    
    qty: int
    
    total: TruncatedFloat


class ClearCart(BaseModel):
    success: bool
