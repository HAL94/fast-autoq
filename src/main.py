from fastapi import FastAPI
from auth.route import router as auth_router
from modules.category.route import router as cat_router
from modules.cart.route import router as cart_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(cat_router)
app.include_router(cart_router)
