from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AgreementBase(BaseModel):
    company_id: str
    restaurant_id: str
    terms: str
    signed_at: datetime


class AgreementCreate(AgreementBase):
    pass


class AgreementUpdate(BaseModel):
    company_id: Optional[str] = None
    restaurant_id: Optional[str] = None
    terms: Optional[str] = None
    signed_at: Optional[datetime] = None


class AgreementResponse(AgreementBase):
    id: str

    class Config:
        orm_mode = True
