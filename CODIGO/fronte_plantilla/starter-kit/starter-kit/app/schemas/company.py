from pydantic import BaseModel, ConfigDict


class CompanyCreate(BaseModel):
    name: str
    ruc: str | None = None


class CompanyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    ruc: str | None = None
    restaurant_id: int | None = None
    tenant_id: str | None = None
