from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.models.restaurant import Restaurant
from backend.schemas.restaurant import RestaurantCreate, RestaurantUpdate


def create_restaurant(db: Session, restaurant: RestaurantCreate) -> Restaurant:
    try:
        db_restaurant = Restaurant(name=restaurant.name, owner_id=restaurant.owner_id)
        db.add(db_restaurant)
        db.commit()
        db.refresh(db_restaurant)
        return db_restaurant
    except SQLAlchemyError:
        db.rollback()
        raise


def get_restaurants(db: Session, skip: int = 0, limit: int = 100) -> list[Restaurant]:
    return db.query(Restaurant).offset(skip).limit(limit).all()


def get_restaurant(db: Session, restaurant_id: str) -> Restaurant | None:
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()


def update_restaurant(db: Session, restaurant_id: str, restaurant: RestaurantUpdate) -> Restaurant | None:
    db_restaurant = get_restaurant(db, restaurant_id)
    if not db_restaurant:
        return None
    if restaurant.name is not None:
        db_restaurant.name = restaurant.name
    if restaurant.owner_id is not None:
        db_restaurant.owner_id = restaurant.owner_id
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def delete_restaurant(db: Session, restaurant_id: str) -> bool:
    db_restaurant = get_restaurant(db, restaurant_id)
    if not db_restaurant:
        return False
    db.delete(db_restaurant)
    db.commit()
    return True
