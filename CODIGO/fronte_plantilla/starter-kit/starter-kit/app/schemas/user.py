from pydantic import BaseModel, ConfigDict
from app.models.user import UserRole


class UserCreate(BaseModel):
    email: str
    password: str
    role: UserRole


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    role: UserRole


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
