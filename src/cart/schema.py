
from pydantic import BaseModel


class CartItemAdd(BaseModel):
    product_id: int
    seller_id: int
    qty: int = 1
    purchase_price: float


class GetCart(BaseModel):
    cart_id: int
    cart: list["CartItem"]

class CartItem(BaseModel):
    id: int
    product_id: int
    seller_id: int
    purchase_price: float
    qty: int
