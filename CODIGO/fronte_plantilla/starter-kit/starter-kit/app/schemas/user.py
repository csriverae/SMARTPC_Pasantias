"""
Pydantic schemas for user validation and serialization
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator, EmailStr
from datetime import datetime
from app.models.user import UserRole


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: str
    password: str
    tenant_id: int  # Required: must belong to a tenant
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.employee  # Default to employee

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format"""
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower().strip()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password requirements"""
        if not v or len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

    @field_validator('tenant_id')
    @classmethod
    def validate_tenant_id(cls, v):
        """Validate tenant ID"""
        if not v or v < 1:
            raise ValueError('Invalid tenant ID')
        return v

    @field_validator('full_name', mode='after')
    @classmethod
    def build_full_name(cls, v, info):
        """Build full name from first and last names if not provided"""
        if v:
            return v.strip()
        
        values = info.data
        first = values.get('first_name') or ''
        last = values.get('last_name') or ''
        combined = f"{first} {last}".strip()
        return combined if combined else None


class UserLogin(BaseModel):
    """Schema for user login"""
    email: str
    password: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format"""
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower().strip()


class PasswordChangeRequest(BaseModel):
    """Schema for password change"""
    current_password: str
    new_password: str
    confirm_password: str

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        """Validate new password"""
        if not v or len(v) < 6:
            raise ValueError('New password must be at least 6 characters')
        return v

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        """Verify password confirmation"""
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('Passwords do not match')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

    @field_validator('full_name', mode='after')
    @classmethod
    def build_full_name(cls, v, info):
        """Build full name from first and last names if not provided"""
        if v:
            return v.strip()
        
        values = info.data
        first = values.get('first_name') or ''
        last = values.get('last_name') or ''
        combined = f"{first} {last}".strip()
        return combined if combined else None


class UserResponse(BaseModel):
    """Schema for user response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    email: str
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True


class UserListResponse(BaseModel):
    """Schema for user list response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: Optional[str] = None
    role: UserRole
    is_active: bool = True
    created_at: Optional[datetime] = None


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    tenant_id: Optional[int] = None


class TokenData(BaseModel):
    """Schema for token claims"""
    email: Optional[str] = None
    tenant_id: Optional[int] = None
    exp: Optional[int] = None
    iat: Optional[int] = None
    sub: Optional[str] = None


class ErrorDetail(BaseModel):
    """Schema for error response details"""
    message: str
    status: int
    error: bool = True
    data: Optional[dict] = None


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
