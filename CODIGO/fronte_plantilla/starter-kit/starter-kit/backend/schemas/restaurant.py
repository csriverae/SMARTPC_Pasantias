from pydantic import BaseModel
from typing import Optional


class RestaurantBase(BaseModel):
    name: str
    owner_id: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    owner_id: Optional[str] = None


class RestaurantResponse(RestaurantBase):
    id: str

    class Config:
        orm_mode = True
