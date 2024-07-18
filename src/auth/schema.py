from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    id: int
    username: str
    email: Union[str, None] = None
    disabled: Union[bool, None] = None
    


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class RegisterUser(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    email: Union[str, None] = None
