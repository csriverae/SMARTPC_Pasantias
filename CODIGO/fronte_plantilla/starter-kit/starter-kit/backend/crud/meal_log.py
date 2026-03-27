from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.models.meal_log import MealLog
from backend.schemas.meal_log import MealLogCreate, MealLogUpdate


def create_meal_log(db: Session, meal_log: MealLogCreate) -> MealLog:
    try:
        db_meal_log = MealLog(
            user_id=meal_log.user_id,
            restaurant_id=meal_log.restaurant_id,
            meal_type=meal_log.meal_type,
            consumed_at=meal_log.consumed_at,
        )
        db.add(db_meal_log)
        db.commit()
        db.refresh(db_meal_log)
        return db_meal_log
    except SQLAlchemyError:
        db.rollback()
        raise


def get_meal_logs(db: Session, skip: int = 0, limit: int = 100) -> list[MealLog]:
    return db.query(MealLog).offset(skip).limit(limit).all()


def get_meal_log(db: Session, meal_log_id: str) -> MealLog | None:
    return db.query(MealLog).filter(MealLog.id == meal_log_id).first()


def update_meal_log(db: Session, meal_log_id: str, meal_log: MealLogUpdate) -> MealLog | None:
    db_meal_log = get_meal_log(db, meal_log_id)
    if not db_meal_log:
        return None
    if meal_log.user_id is not None:
        db_meal_log.user_id = meal_log.user_id
    if meal_log.restaurant_id is not None:
        db_meal_log.restaurant_id = meal_log.restaurant_id
    if meal_log.meal_type is not None:
        db_meal_log.meal_type = meal_log.meal_type
    if meal_log.consumed_at is not None:
        db_meal_log.consumed_at = meal_log.consumed_at
    db.commit()
    db.refresh(db_meal_log)
    return db_meal_log


def delete_meal_log(db: Session, meal_log_id: str) -> bool:
    db_meal_log = get_meal_log(db, meal_log_id)
    if not db_meal_log:
        return False
    db.delete(db_meal_log)
    db.commit()
    return True
