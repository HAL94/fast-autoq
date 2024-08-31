

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


def service_meta(db: Session = Depends(get_db), user=Depends(AppJwtBearer()), cart: CartDb = Depends(GetUserCart(throw_error=True))):
    return db, user, cart


class CreateOrderFromCart():
    def __init__(self, deps: Tuple[Session, User, CartDb] = Depends(service_meta)):
        self.db, self.user, self.cart = deps

    def create_order(self):
        try:
            created_order = CreateOrder(external_id='ext_123', fulfillment_status='PENDING', payment_status='PAID', cart_id=self.cart.id, currency_code='SAR', tax_rate='0.15',
                                        customer_id=self.user['id'], email=self.user['sub'], phone='+96634534343', seller_id=1, order_amount=self.cart.total)
            order = OrderDb(**created_order.model_dump())

            self.cart.total = 0

            for line_item in self.cart.cart_items:
                line_item.line_type = LineTypeValues.ORDER.value

            self.db.add(order)

            self.db.commit()

            return created_order

        except Exception as e:
            print(e.__str__())
            raise e
