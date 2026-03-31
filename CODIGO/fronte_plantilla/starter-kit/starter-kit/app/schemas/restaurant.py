"""
Pydantic schemas for restaurant validation and serialization
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime


class RestaurantCreate(BaseModel):
    """Schema for creating a new restaurant"""
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate restaurant name"""
        if not v or len(v) < 3:
            raise ValueError('Restaurant name must be at least 3 characters')
        return v.strip()

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format"""
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower().strip() if v else None


class RestaurantUpdate(BaseModel):
    """Schema for updating a restaurant"""
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate restaurant name"""
        if v and len(v) < 3:
            raise ValueError('Restaurant name must be at least 3 characters')
        return v.strip() if v else None


class RestaurantResponse(BaseModel):
    """Schema for restaurant response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class RestaurantListResponse(BaseModel):
    """Schema for restaurant list response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime
