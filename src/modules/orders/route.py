

from fastapi import APIRouter, Depends

from auth.security import get_token_header
from common.app_response import AppResponse
from db.db_init import get_db
from sqlalchemy.orm import Session

from modules.orders.models import OrderDb
from modules.orders.schema import CreateOrder, GetOrders
from modules.orders.services import CreateOrderFromCart
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix="/orders", tags=["Order"], dependencies=[Depends(get_token_header)])


@router.post('/create', response_model=AppResponse[CreateOrder])
def create_order(order_service: CreateOrderFromCart = Depends(CreateOrderFromCart)):
    try:
        return {
            "data": order_service.create_order()
        }
    except Exception as e:
        return AppResponse(status_code=500, message=e.__str__(), data=None)


@router.get('/', response_model=AppResponse[GetOrders])
def get_orders(db: Session = Depends(get_db)):
    try:
        result = db.query(OrderDb).options(
            selectinload(OrderDb.order_items)).all()

        return {"data": {"orders": result}}
    except Exception as e:
        raise AppResponse(status_code=500, message=e.__str__(), data=None)
