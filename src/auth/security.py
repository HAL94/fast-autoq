from typing import Annotated, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
import jwt

from auth.schema import User
from settings.base import AppSettings

settings = AppSettings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "read:cats": "Read available categories"
    }
)


# if you only need to check if a user is authed,
# acting as a side effect without requiring the values
async def get_token_header(token: Annotated[str, Depends(HTTPBearer())]):
    if token is None:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


# if needed the token's payload and user information, you can use this inside the
# the operation itself
class AppJwtBearer():
    def __init__(self, scopes: List[str] = []):
        self.scopes = scopes

    def __call__(self, token: Annotated[User, Depends(oauth2_scheme)]):
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        for scope in self.scopes:
            if scope not in payload['scopes']:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authorized')
        return payload
