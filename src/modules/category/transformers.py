

from decimal import Decimal
from typing import Dict, List, Tuple, Union

from category.schema import ProductSchema, SellerSchema
from db.models import ProductDb, SellerDb


def transform_category_products(product_list: List[Tuple[ProductDb, Decimal, SellerDb]]) -> Dict[str, Union[ProductSchema, SellerSchema]]:
    result = {}
    for prod_tuple in product_list:
        product, selling_price, seller = prod_tuple[0], prod_tuple[1], prod_tuple[2]
        if product.id not in result:
            result[product.id] = {
                "product": ProductSchema(id=product.id, title=product.title, description=product.description, thumbnail=product.thumbnail).model_dump(),
                "sellers": [
                    SellerSchema(id=seller.id, seller_name=seller.seller_name,
                                 selling_price=selling_price).model_dump()
                ],
            }
        else:
            result[product.id]["sellers"].append(SellerSchema(
                id=seller.id, seller_name=seller.seller_name, selling_price=selling_price).model_dump())
    return list(result.values())
