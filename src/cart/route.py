from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import delete
from sqlalchemy.orm import Session

from cart.schema import CartItem, CartItemAdd, GetCart
from cart.services import create_user_cart

from common.depends import GetUserCart
from common.app_response import AppResponse

from db.db_init import get_db
from db.models import CartDb, CartItemDb

from auth.security import AppJwtBearer, get_token_header


router = APIRouter(
    prefix="/cart", tags=["Cart"], dependencies=[Depends(get_token_header)])

@router.get('/', response_model=AppResponse[GetCart])
def get_cart(cart: CartDb = Depends(GetUserCart(throw_error=True))):
    return {
        "data": {
            "cart_id": cart.id,
            "cart": cart.cart_items
        }
    }


@router.post('/plus/{cart_item_id}', response_model=AppResponse[CartItem])
def plus_cart_item(cart_item_id: int, cart: CartDb = Depends(GetUserCart(throw_error=True)), db: Session = Depends(get_db)):
    cart_item = db.query(CartItemDb).where(
        CartItemDb.id == cart_item_id).where(CartItemDb.cart_id == cart.id).first()

    if not cart_item:
        raise HTTPException(status_code=500, detail='Could not get cart_item')

    cart_item.qty = cart_item.qty + 1

    db.commit()

    return {
        "data": cart_item
    }


@router.post('/minus/{cart_item_id}', response_model=CartItem)
def minus_cart_item(cart_item_id: int, cart: CartDb = Depends(GetUserCart(throw_error=True)), db: Session = Depends(get_db)):
    cart_item = db.query(CartItemDb).where(
        CartItemDb.id == cart_item_id).\
        where(CartItemDb.cart_id == cart.id).first()

    if not cart_item:
        raise HTTPException(
            status_code=500, detail="could not get cart_item")

    if cart_item.qty > 1:
        cart_item.qty = cart_item.qty - 1
        db.commit()
    else:
        raise HTTPException(
            status_code=400, detail="Cannot decrement to 0, call remove instead")

    return cart_item


@router.post('/remove/{cart_item_id}', response_model=GetCart)
def remove_cart_item(cart_item_id: int, cart: CartDb = Depends(GetUserCart(throw_error=True)), db: Session = Depends(get_db)):
    cart_item = db.query(CartItemDb).where(
        CartItemDb.id == cart_item_id).first()

    if not cart_item:
        raise HTTPException(
            status_code=400, detail="could not find cart_item with passed id")

    del_query = delete(CartItemDb).where(CartItemDb.id == cart_item_id)

    db.execute(del_query)

    db.commit()
    
    return {
        "cart_id": cart.id,
        "cart": cart.cart_items
    }


@router.post('/clear')
def clear_cart(cart: CartDb = Depends(GetUserCart(throw_error=True)), db: Session = Depends(get_db)):
    try:
        del_query = delete(CartItemDb).where(CartItemDb.cart_id == cart.id)

        db.execute(del_query)

        db.commit()

        return {"success": True}
    except Exception as exc:
        print(exc)


@router.post('/add', response_model=AppResponse[GetCart])
def add_cart_item(cart_item_data: CartItemAdd, user = Depends(AppJwtBearer()), db: Session = Depends(get_db), cart = Depends(GetUserCart(throw_error=False))):
    user_cart = cart

    if not cart:
        user_cart = create_user_cart(db, user["id"])

    cart_item = CartItemDb(**cart_item_data.model_dump())

    user_cart.cart_items.append(cart_item)

    db.commit()

    return {
        "data": {
            "cart_id": user_cart.id,
            "cart": user_cart.cart_items            
        }
    }
