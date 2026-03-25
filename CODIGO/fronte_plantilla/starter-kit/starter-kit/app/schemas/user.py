from pydantic import BaseModel, ConfigDict, field_validator
from app.models.user import UserRole


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    role: UserRole | None = None

    @field_validator('full_name', mode='after')
    def build_full_name(cls, v, values):
        if v:
            return v
        first = values.get('first_name') or ''
        last = values.get('last_name') or ''
        combined = f"{first} {last}".strip()
        return combined or None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    full_name: str | None = None
    role: UserRole


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None


class TokenData(BaseModel):
    email: str | None = None
