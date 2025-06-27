from typing import Generic, TypeVar
from pydantic import BaseModel, constr

T = TypeVar("T")


class IResponseBase(BaseModel, Generic[T]):
    code: int = 100
    message: str = "Success"
    items: T | None = None


# Auth Service Schema

## Request
class AuthRequest(BaseModel):
    username: str
    password: constr(min_length=5)


## Response
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
