from pydantic import BaseModel, ConfigDict, field_validator
from app.models.user import UserRole


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    role: UserRole | None = None

    @field_validator('password', mode='before')
    @classmethod
    def validate_password_length(cls, v):
        """Validar que la contraseña no sea más larga de 72 bytes (límite de bcrypt)"""
        if not isinstance(v, str):
            return v
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError(f"La contraseña es demasiado larga. Máximo 72 bytes. Actual: {len(password_bytes)} bytes")
        return v

    @field_validator('password', mode='before')
    @classmethod
    def validate_password_required(cls, v):
        """Validar que la contraseña tenga mínimo 6 caracteres"""
        if not v or len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v

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

    @field_validator('password', mode='before')
    @classmethod
    def truncate_password_login(cls, v):
        """Truncar contraseña a 72 bytes para bcrypt"""
        if v:
            password_bytes = v.encode('utf-8')[:72]
            return password_bytes.decode('utf-8', errors='ignore')
        return v


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None


class TokenData(BaseModel):
    email: str | None = None


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @field_validator('new_password', mode='before')
    @classmethod
    def validate_new_password_length(cls, v):
        """Validar que la nueva contraseña no sea más larga de 72 bytes"""
        if v:
            password_bytes = v.encode('utf-8')
            if len(password_bytes) > 72:
                raise ValueError(f"La nueva contraseña es demasiado larga. Máximo 72 bytes")
        return v
