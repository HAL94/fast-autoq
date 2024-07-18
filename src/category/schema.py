from typing import Optional
from pydantic import BaseModel

class CategoryId(BaseModel):
    id: int


class ProductSchema(BaseModel):
    id: int
    title: str
    description: str
    thumbnail: str
    
class SellerSchema(BaseModel):
    id: int
    seller_name: str
    selling_price: float
