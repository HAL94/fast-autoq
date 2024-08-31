from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import CartDb, CartStatusValues
from modules.user.models import UserDb

def create_user_cart(db: Session, user_id: int):
    user = db.query(UserDb).filter(UserDb.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=500, detail="Creating cart for user failed, not found")
    
    cart = CartDb()
    cart.user = user
    cart.status = CartStatusValues.ACTIVE.value
    
    db.add(cart)
        
    db.commit()
    
    return cart
        