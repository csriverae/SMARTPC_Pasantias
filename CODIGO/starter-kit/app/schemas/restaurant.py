from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SubscriptionPlan(str, Enum):
    basic = "basic"
    pro = "pro"
    enterprise = "enterprise"


class RestaurantBase(BaseModel):
    name: str = Field(..., max_length=255)
    ruc: str = Field(..., max_length=50)
    address: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None
    subscription_plan: Optional[SubscriptionPlan] = SubscriptionPlan.basic
    subscription_expires_at: Optional[datetime] = None
    is_active: Optional[bool] = True


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    ruc: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None
    subscription_plan: Optional[SubscriptionPlan] = None
    subscription_expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class RestaurantResponse(RestaurantBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
