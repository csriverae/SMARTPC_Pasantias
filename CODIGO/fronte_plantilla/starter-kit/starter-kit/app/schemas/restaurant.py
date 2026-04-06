from pydantic import BaseModel, ConfigDict


class RestaurantCreate(BaseModel):
    name: str


class RestaurantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    user_id: int
    tenant_id: str | None = None