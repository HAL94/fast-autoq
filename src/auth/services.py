from datetime import datetime, timedelta, timezone
from typing import Union
from fastapi import Depends, HTTPException
import jwt

from auth.hashing import get_password_hash, verify_password
from auth.schema import RegisterUser
from auth.security import ALGORITHM, SECRET_KEY
from db.db_init import get_db
from sqlalchemy.orm import Session

from db.models import RolesValues, UserDb

def register_user(data: RegisterUser, db: Session = Depends(get_db)):
    try:
        user = UserDb()
        found_user = db.query(UserDb).filter(
            UserDb.email == data.email).first()
        
        if found_user is not None:
            raise HTTPException(400, "Unauthorized: failed to register")

        user.email = data.email
        user.hashed_password = get_password_hash(data.password)
        user.user_role = RolesValues.CUSTOMER.value

        db.add(user)
        db.commit()
        return True
    except Exception as exc:
        print(exc)
        raise HTTPException(400, "unauthorized: failed to register")


class AuthLogin():
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
    
    def get_user(self, username: str):
        user = self.db.query(UserDb).filter(UserDb.email == username).first()
            
        return user
    
    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
