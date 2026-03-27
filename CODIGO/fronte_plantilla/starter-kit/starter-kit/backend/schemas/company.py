from pydantic import BaseModel
from typing import Optional


class CompanyBase(BaseModel):
    name: str
    owner_id: str


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    owner_id: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: str

    class Config:
        orm_mode = True
