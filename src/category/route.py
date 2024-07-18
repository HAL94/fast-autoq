
from decimal import Decimal
from typing import Annotated, List, Tuple
from fastapi import APIRouter, Depends, HTTPException, Security, status

from sqlalchemy import distinct, func
from sqlalchemy.orm import Session, joinedload

from auth.schema import User
from auth.security import AppJwtBearer
from category.transformers import transform_category_products
from common.logger import app_test
from db.db_init import get_db
from db.models import CategoryDb, ProductDb, ProductSellerDb, SellerDb

router = APIRouter(prefix="/category", tags=["Category"])

# Annotated[User, Security(get_current_user, scopes=['read:cats'])]


@router.get('/{id}/products')
# type: ignore
async def get_category_products(id: int,  _=Depends(AppJwtBearer(['read:cats'])), db: Session = Depends(get_db)):

    """ 
        Equivalent to:
        SELECT 
            distinct(product_id), min(price) as price 
        FROM 
            product_sellers 
        GROUP BY 
            product_id 
        ORDER BY 
            product_id;
    """
    min_price_subquery = (
        db.query(distinct(ProductSellerDb.product_id), 
                 func.min(ProductSellerDb.price).label('price')).\
            group_by(ProductSellerDb.product_id).\
            order_by(ProductSellerDb.product_id).\
            subquery()
    )
    
    # 
    main_query = db.query(ProductDb, ProductSellerDb.price, SellerDb).\
        join(ProductSellerDb, ProductSellerDb.product_id == ProductDb.id).\
        join(SellerDb, ProductSellerDb.seller_id == SellerDb.id).\
        filter(ProductDb.category_id == id, ProductSellerDb.price == min_price_subquery.c.price).\
        order_by(ProductDb.id).\
        group_by(ProductDb.id, SellerDb.id, ProductSellerDb.price)

    # print(f"query: {main_query}")

    products: List[Tuple[ProductDb, Decimal, SellerDb]] = main_query.all()

    # print(products)

    result = transform_category_products(product_list=products)

    return {
        "result": result
    }


@router.get('/all')
async def get_all_categories(db: Session = Depends(get_db)):
    try:
        return db.query(CategoryDb).\
            filter(CategoryDb.parent_id == None).\
            options(joinedload(CategoryDb.children)).\
            all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong"
        )


@router.get('/{id}')
async def get_category(id: int, db: Session = Depends(get_db), some_value: str = Depends(app_test)):
    try:
        category = db.query(CategoryDb).where(CategoryDb.id == id).first()
        
        return {
            "name": category.name,
            "id": category.id,
            "children": category.children            
        }
    except Exception as exc:
        # print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
