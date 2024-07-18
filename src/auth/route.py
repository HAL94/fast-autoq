from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from auth.schema import RegisterUser, Token, User
from auth.security import AppJwtBearer, ACCESS_TOKEN_EXPIRE_MINUTES
from auth.services import AuthLogin, register_user
from db.db_init import get_db

from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    login_service = AuthLogin(db)

    user: User | None = login_service.authenticate_user(
        form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token = login_service.create_access_token(
        {"sub": user.email, "id": user.id, "role": user.user_role, "scopes": ["read:cats"]}, 
        expires_delta=access_token_expires)

    return Token(access_token=token, token_type="bearer")


@router.post("/register")
async def register(data: RegisterUser, db: Session = Depends(get_db)) -> dict[str, bool]:
    return {"success": register_user(data, db)}


@router.get('/me')
async def get_me(current_user = Depends(AppJwtBearer())):
    print(f"user: {current_user}")
    return current_user
