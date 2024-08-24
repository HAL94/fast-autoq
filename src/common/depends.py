from fastapi import Depends, HTTPException

from auth.security import AppJwtBearer
from sqlalchemy.orm import Session

from db.db_init import get_db
from db.models import CartDb, CartStatusValues


class GetUserCart():
    def __init__(self, throw_error: bool):
        self.throw_error = throw_error

    def __call__(self, user=Depends(AppJwtBearer()), db: Session = Depends(get_db)):
        cart: CartDb = db.query(CartDb).filter(
            CartDb.user_id == user["id"], CartDb.status == CartStatusValues.ACTIVE.value).first()

        if cart is None and self.throw_error:
            raise HTTPException(
                status_code=500, detail='Could not find cart for user')

        return cart
