from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.routes.auth import get_current_user, require_role
from backend.crud.meal_log import create_meal_log, get_meal_logs, get_meal_log, update_meal_log, delete_meal_log
from backend.schemas.meal_log import MealLogCreate, MealLogUpdate
from backend.db.session import SessionLocal
from backend.core.response import api_success, api_error
from backend.models.user import User

meal_log_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@meal_log_router.post("/", response_model=None)
def create_meal_log_endpoint(meal_log: MealLogCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("restaurant_admin"))):
    created = create_meal_log(db, meal_log)
    return api_success("Registro de comida creado", data={"meal_log": {"id": str(created.id), "user_id": str(created.user_id), "restaurant_id": str(created.restaurant_id), "meal_type": created.meal_type, "consumed_at": created.consumed_at.isoformat()}})


@meal_log_router.get("/", response_model=None)
def list_meal_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logs = get_meal_logs(db, skip=skip, limit=limit)
    data = [{"id": str(l.id), "user_id": str(l.user_id), "restaurant_id": str(l.restaurant_id), "meal_type": l.meal_type, "consumed_at": l.consumed_at.isoformat()} for l in logs]
    return api_success("Registros de comida obtenidos", data={"meal_logs": data})


@meal_log_router.get("/{meal_log_id}", response_model=None)
def get_meal_log_endpoint(meal_log_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    log = get_meal_log(db, meal_log_id)
    if not log:
        return api_error("Registro de comida no encontrado", status=404)
    return api_success("Registro de comida encontrado", data={"meal_log": {"id": str(log.id), "user_id": str(log.user_id), "restaurant_id": str(log.restaurant_id), "meal_type": log.meal_type, "consumed_at": log.consumed_at.isoformat()}})


@meal_log_router.put("/{meal_log_id}", response_model=None)
def update_meal_log_endpoint(meal_log_id: str, payload: MealLogUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role("restaurant_admin"))):
    log = update_meal_log(db, meal_log_id, payload)
    if not log:
        return api_error("Registro de comida no encontrado", status=404)
    return api_success("Registro de comida actualizado", data={"meal_log": {"id": str(log.id), "user_id": str(log.user_id), "restaurant_id": str(log.restaurant_id), "meal_type": log.meal_type, "consumed_at": log.consumed_at.isoformat()}})


@meal_log_router.delete("/{meal_log_id}", response_model=None)
def delete_meal_log_endpoint(meal_log_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role("restaurant_admin"))):
    if not delete_meal_log(db, meal_log_id):
        return api_error("Registro de comida no encontrado", status=404)
    return api_success("Registro de comida eliminado", data={})
