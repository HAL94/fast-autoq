from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import delete
from sqlalchemy.orm import Session

from cart.schema import CartItem, CartItemAdd, ClearCart, GetCart
from cart.services import create_user_cart

from common.depends import GetUserCart
from common.app_response import AppResponse

from db.db_init import get_db
from db.models import CartDb, CartStatusValues, LineItemDb, LineTypeValues, ProductSellerDb

from auth.security import AppJwtBearer, get_token_header


router = APIRouter(
    prefix="/cart", tags=["Cart"], dependencies=[Depends(get_token_header)])


@router.get('/', response_model=AppResponse[GetCart])
def get_cart(cart: CartDb = Depends(GetUserCart(throw_error=True))):
    return {
        "data": {
            "cart_id": cart.id,
            "status": cart.status,
            "total_amount": cart.total,
            "cart": cart.cart_items
        }
    }


@router.post('/plus/{cart_item_id}', response_model=AppResponse[GetCart])
def plus_cart_item(cart_item_id: int, cart: CartDb = Depends(GetUserCart(throw_error=True)), db: Session = Depends(get_db)):
    cart_item = db.query(LineItemDb).where(
        LineItemDb.id == cart_item_id).where(LineItemDb.cart_id == cart.id, LineItemDb.line_type == LineTypeValues.CART.value).first()

    if not cart_item:
        raise HTTPException(status_code=500, detail='Could not get cart_item')

    cart_item.qty = cart_item.qty + 1
    cart_item.total = round(cart_item.purchase_price * cart_item.qty, 2)
    cart.total = round(cart.total + cart_item.purchase_price, 2)

    db.commit()

    return {
        "data": {
            "cart_id": cart.id,
            "status": cart.status,
            "cart": cart.cart_items,
            "total_amount": cart.total
        }
    }


@router.post('/minus/{cart_item_id}', response_model=AppResponse[GetCart])
def minus_cart_item(cart_item_id: int, cart: CartDb = Depends(GetUserCart(throw_error=True)), db: Session = Depends(get_db)):
    cart_item = db.query(LineItemDb).where(
        LineItemDb.id == cart_item_id).\
        where(LineItemDb.cart_id == cart.id, LineItemDb.line_type ==
              LineTypeValues.CART.value).first()

    if not cart_item:
        raise HTTPException(
            status_code=500, detail="could not get cart_item")

    if cart_item.qty > 1:
        cart_item.qty = cart_item.qty - 1
        cart_item.total = round(cart_item.purchase_price * cart_item.qty, 2)
        cart.total = round(cart.total - cart_item.purchase_price, 2)
        db.commit()
    else:
        raise HTTPException(
            status_code=400, detail="Cannot decrement to 0, call remove instead")

    return {
        "data": {
            "cart_id": cart.id,
            "status": cart.status,
            "cart": cart.cart_items,
            "total_amount": cart.total
        }
    }


@router.post('/remove/{cart_item_id}', response_model=AppResponse[GetCart])
def remove_cart_item(cart_item_id: int, cart: CartDb = Depends(GetUserCart(throw_error=True)), db: Session = Depends(get_db)):
    cart_item = db.query(LineItemDb).where(
        LineItemDb.id == cart_item_id).first()

    if not cart_item:
        raise HTTPException(
            status_code=400, detail="could not find cart_item with passed id")

    cart.total = round(cart.total - cart_item.total, 2)

    del_query = delete(LineItemDb).where(
        LineItemDb.id == cart_item_id, LineItemDb.line_type == LineTypeValues.CART.value)

    db.execute(del_query)

    db.commit()

    return {
        "data": {
            "cart_id": cart.id,
            "status": cart.status,
            "cart": cart.cart_items,
            "total_amount": cart.total
        }
    }


@router.post('/clear', response_model=AppResponse[ClearCart])
def clear_cart(cart: CartDb = Depends(GetUserCart(throw_error=True)), db: Session = Depends(get_db)):
    try:
        del_query = delete(LineItemDb).where(
            LineItemDb.cart_id == cart.id, LineItemDb.line_type == LineTypeValues.CART.value)

        cart.total = 0
        cart.status = CartStatusValues.EMPTY.value

        db.execute(del_query)

        db.commit()

        return {"data": {"sucess": True}}
    except Exception as exc:
        print(exc)


@router.post('/add', response_model=AppResponse[GetCart])
def add_cart_item(cart_item_data: CartItemAdd, user=Depends(AppJwtBearer()), db: Session = Depends(get_db), cart=Depends(GetUserCart(throw_error=False))):
    user_cart = cart

    if not cart:
        user_cart = create_user_cart(db, user["id"])

    seller_id = cart_item_data.seller_id
    product_id = cart_item_data.product_id

    product_price = db.query(ProductSellerDb.price).\
        filter(ProductSellerDb.seller_id == seller_id,
               ProductSellerDb.product_id == product_id).\
        first()

    if not product_price:
        raise HTTPException(
            status_code=400, detail='Could not find selected product and seller')

    line_item_data = {**cart_item_data.model_dump()}
    line_item_data['purchase_price'] = product_price[0]
    line_item_data['line_type'] = LineTypeValues.CART.value
    line_item_data['total'] = product_price[0] * cart_item_data.qty

    cart_item = LineItemDb(**line_item_data)

    user_cart.cart_items.append(cart_item)
    user_cart.status = CartStatusValues.ACTIVE.value
    user_cart.total = user_cart.total + float(cart_item.total)

    db.commit()

    return {
        "data": {
            "cart_id": user_cart.id,
            "status": user_cart.status,
            "cart": user_cart.cart_items,
            "total_amount": user_cart.total
        }
    }
