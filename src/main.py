from fastapi import FastAPI
from auth.route import router as auth_router
from modules.category.route import router as cat_router
from modules.cart.route import router as cart_router
from modules.orders.route import router as order_router

import common.all_models
from db.base import Base
from db.db_init import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(cat_router)
app.include_router(cart_router)
app.include_router(order_router)
