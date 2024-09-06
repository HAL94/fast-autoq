

from typing import Tuple
from fastapi import Depends
from auth.schema import User
from auth.security import AppJwtBearer
from common.depends import GetUserCart
from db.db_init import get_db
from modules.cart.models import CartDb, LineTypeValues
from sqlalchemy.orm import Session

from modules.orders.models import OrderDb
from modules.orders.schema import CreateOrder
from dataclasses import dataclass


def order_service_meta(db: Session = Depends(get_db), user=Depends(AppJwtBearer()), cart: CartDb = Depends(GetUserCart(throw_error=True))):
    return db, user, cart


@dataclass
class OrderServiceBase():
    deps: Tuple[Session, User, CartDb] = Depends(order_service_meta)
    
    
@dataclass
class CreateOrderFromCart(OrderServiceBase):    
    def create_order(self):
        try:
            db, user, cart = self.deps
            if len(cart.cart_items) == 0:
                raise Exception('Cannot create order from empty cart')
            
            created_order = CreateOrder(external_id='ext_123', fulfillment_status='PENDING', payment_status='PAID', cart_id=cart.id, currency_code='SAR', tax_rate='0.15',
                                        customer_id=user['id'], email=user['sub'], phone='+96634534343', seller_id=1, order_amount=cart.total)
            
            order = OrderDb(**created_order.model_dump())

            cart.total = 0

            order_items = []
            
            for line_item in cart.cart_items:
                line_item.line_type = LineTypeValues.ORDER.value
                line_item.order_id = order.id
                
                order_items.append(line_item)
            
            order.order_items = order_items

            db.add(order)

            db.commit()

            return created_order

        except Exception as e:
            print(e.__str__())
            raise e
