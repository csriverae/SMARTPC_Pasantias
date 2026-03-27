from pydantic import BaseModel
from typing import Optional


class InvitationCodeBase(BaseModel):
    code: str
    is_used: bool = False


class InvitationCodeCreate(InvitationCodeBase):
    pass


class InvitationCodeUpdate(BaseModel):
    code: Optional[str] = None
    is_used: Optional[bool] = None


class InvitationCodeResponse(InvitationCodeBase):
    id: str

    class Config:
        orm_mode = True
