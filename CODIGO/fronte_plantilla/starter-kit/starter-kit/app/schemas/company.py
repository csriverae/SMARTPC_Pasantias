from pydantic import BaseModel, ConfigDict, field_validator


class CompanyCreate(BaseModel):
    name: str
    ruc: str | None = None

    @field_validator('ruc', mode='before')
    @classmethod
    def validate_ruc(cls, v):
        if v is None:
            return v
        if not isinstance(v, str):
            raise ValueError("RUC debe ser una cadena de texto")
        # Remove any spaces or dashes
        ruc_clean = ''.join(c for c in v if c.isdigit())
        if len(ruc_clean) != 13:
            raise ValueError("RUC debe tener exactamente 13 dígitos")
        return ruc_clean


class CompanyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    ruc: str | None = None
    restaurant_id: int | None = None
    tenant_id: str | None = None
