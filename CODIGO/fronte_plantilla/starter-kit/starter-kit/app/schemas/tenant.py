"""
Pydantic schemas for tenant validation and serialization
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime


class TenantCreate(BaseModel):
    """Schema for creating a new tenant"""
    name: str
    slug: str
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate tenant name"""
        if not v or len(v) < 3:
            raise ValueError('Tenant name must be at least 3 characters')
        return v.strip()

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v):
        """Validate slug format"""
        if not v or len(v) < 3:
            raise ValueError('Slug must be at least 3 characters')
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Slug must contain only alphanumeric characters, hyphens, and underscores')
        return v.lower().strip()


class TenantUpdate(BaseModel):
    """Schema for updating a tenant"""
    name: Optional[str] = None
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate tenant name"""
        if v and len(v) < 3:
            raise ValueError('Tenant name must be at least 3 characters')
        return v.strip() if v else None


class TenantResponse(BaseModel):
    """Schema for tenant response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TenantListResponse(BaseModel):
    """Schema for tenant list response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
