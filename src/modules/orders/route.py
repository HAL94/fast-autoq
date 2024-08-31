

from typing import Annotated
from fastapi import APIRouter, Depends

from auth.security import get_token_header
from common.app_response import AppResponse
from common.depends import GetUserCart
from db.db_init import get_db
from sqlalchemy.orm import Session

from modules.orders.schema import CreateOrder
from modules.orders.services import CreateOrderFromCart

router = APIRouter(
    prefix="/orders", tags=["Order"], dependencies=[Depends(get_token_header)])


@router.post('/create', response_model=AppResponse[CreateOrder])
def create_order(order_service: CreateOrderFromCart = Depends(CreateOrderFromCart)):
    try:
        return {
            "data": order_service.create_order()
        }
    except Exception as e:
        raise e
