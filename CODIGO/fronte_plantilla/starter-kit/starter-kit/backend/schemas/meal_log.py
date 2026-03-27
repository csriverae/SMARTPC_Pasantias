from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MealLogBase(BaseModel):
    user_id: str
    restaurant_id: str
    meal_type: str
    consumed_at: datetime


class MealLogCreate(MealLogBase):
    pass


class MealLogUpdate(BaseModel):
    user_id: Optional[str] = None
    restaurant_id: Optional[str] = None
    meal_type: Optional[str] = None
    consumed_at: Optional[datetime] = None


class MealLogResponse(MealLogBase):
    id: str

    class Config:
        orm_mode = True
