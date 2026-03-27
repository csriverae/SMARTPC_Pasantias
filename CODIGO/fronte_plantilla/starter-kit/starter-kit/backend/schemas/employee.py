from pydantic import BaseModel
from typing import Optional


class EmployeeBase(BaseModel):
    user_id: str
    restaurant_id: str
    company_id: str


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    user_id: Optional[str] = None
    restaurant_id: Optional[str] = None
    company_id: Optional[str] = None


class EmployeeResponse(EmployeeBase):
    id: str

    class Config:
        orm_mode = True
