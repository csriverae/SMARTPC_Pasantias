from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: float
    type: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str]
    role: Optional[str] = "employee"


class AuthLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class TokenRefresh(BaseModel):
    refresh_token: str


class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str]
    role: str
    is_active: bool

    class Config:
        orm_mode = True
