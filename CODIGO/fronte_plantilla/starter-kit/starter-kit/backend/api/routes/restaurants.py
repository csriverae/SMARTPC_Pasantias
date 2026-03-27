from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.routes.auth import get_current_user, require_role
from backend.crud.restaurant import create_restaurant, get_restaurants, get_restaurant, update_restaurant, delete_restaurant
from backend.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from backend.db.session import SessionLocal
from backend.core.response import api_success, api_error
from backend.models.user import User

restaurant_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@restaurant_router.post("/", response_model=None)
def create_restaurant_endpoint(restaurant: RestaurantCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    created = create_restaurant(db, restaurant)
    return api_success("Restaurante creado", data={"restaurant": {"id": str(created.id), "name": created.name, "owner_id": str(created.owner_id)}})


@restaurant_router.get("/", response_model=None)
def list_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rest = get_restaurants(db, skip=skip, limit=limit)
    data = [{"id": str(r.id), "name": r.name, "owner_id": str(r.owner_id)} for r in rest]
    return api_success("Restaurantes obtenidos", data={"restaurants": data})


@restaurant_router.get("/{restaurant_id}", response_model=None)
def get_restaurant_endpoint(restaurant_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    restaurant = get_restaurant(db, restaurant_id)
    if not restaurant:
        return api_error("Restaurante no encontrado", status=404)
    return api_success("Restaurante encontrado", data={"restaurant": {"id": str(restaurant.id), "name": restaurant.name, "owner_id": str(restaurant.owner_id)}})


@restaurant_router.put("/{restaurant_id}", response_model=None)
def update_restaurant_endpoint(restaurant_id: str, payload: RestaurantUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    restaurant = update_restaurant(db, restaurant_id, payload)
    if not restaurant:
        return api_error("Restaurante no encontrado", status=404)
    return api_success("Restaurante actualizado", data={"restaurant": {"id": str(restaurant.id), "name": restaurant.name, "owner_id": str(restaurant.owner_id)}})


@restaurant_router.delete("/{restaurant_id}", response_model=None)
def delete_restaurant_endpoint(restaurant_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    if not delete_restaurant(db, restaurant_id):
        return api_error("Restaurante no encontrado", status=404)
    return api_success("Restaurante eliminado", data={})
