from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

# from auth.security import AppJwtBearer
from .schema import ProductSchema
from common.app_response import AppResponse
from db.db_init import get_db
from .models import CategoryDb
from ..sellers.models import ProductSellerDb
from ..products.models import ProductDb


router = APIRouter(prefix="/category", tags=["Category"])


class CategoryProduct(ProductSchema, BaseModel):
    seller_id: int
    price: float


@router.get('/{id}/products', response_model=AppResponse[List[CategoryProduct]])
async def get_category_products(id: int, db: Session = Depends(get_db)):

    ranked_subquery = select(ProductSellerDb.product_id, ProductSellerDb.price, ProductSellerDb.seller_id,
                             func.dense_rank()
                             .over(partition_by=ProductSellerDb.product_id, order_by=ProductSellerDb.price)
                             .label('rank')).subquery()

    result_set = db.query(ProductDb, ranked_subquery.c.price, ranked_subquery.c.seller_id).\
        join(ranked_subquery, ProductDb.id == ranked_subquery.c.product_id).\
        filter(ranked_subquery.c.rank == 1, ProductDb.category_id == id).\
        all()

    result = []

    for result_item in result_set:
        product: ProductDb = result_item[0]

        p_dict = product.__dict__
        p_map = {k: v for k, v in zip(p_dict.keys(), p_dict.values())}

        p_map['price'] = result_item[1]
        p_map['seller_id'] = result_item[2]

        result.append(CategoryProduct(**p_map))

    return {
        "data": result
    }


@router.get('/all')
async def get_all_categories(db: Session = Depends(get_db)):
    try:
        return db.query(CategoryDb).\
            filter(CategoryDb.parent_id == None).\
            options(joinedload(CategoryDb.children)).\
            all()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong"
        )


@router.get('/{id}')
async def get_category(id: int, db: Session = Depends(get_db)):
    try:
        category = db.query(CategoryDb).where(CategoryDb.id == id).first()

        return {
            "name": category.name,
            "id": category.id,
            "children": category.children
        }
    except Exception:
        # print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
