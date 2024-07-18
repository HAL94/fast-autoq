from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')

class AppResponse(BaseModel, Generic[T]):
    status_code: int = Field(description="status code", default=200)
    message: str = Field(description="Message back to client", default="done")
    data: Optional[T]
    
