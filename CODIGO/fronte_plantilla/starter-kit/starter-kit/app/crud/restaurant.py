"""
CRUD operations for Restaurant model
"""
from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant


def create_restaurant(db: Session, restaurant_data: dict) -> Restaurant:
    """Create a new restaurant"""
    restaurant = Restaurant(**restaurant_data)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def get_restaurant(db: Session, restaurant_id: int) -> Restaurant | None:
    """Get restaurant by ID"""
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()


def get_restaurants_by_tenant(db: Session, tenant_id: int, skip: int = 0, limit: int = 100) -> list[Restaurant]:
    """Get all restaurants for a specific tenant"""
    return (
        db.query(Restaurant)
        .filter(Restaurant.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_restaurant(db: Session, restaurant_id: int, update_data: dict) -> Restaurant | None:
    """Update restaurant"""
    restaurant = get_restaurant(db, restaurant_id)
    if not restaurant:
        return None
    for key, value in update_data.items():
        setattr(restaurant, key, value)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def delete_restaurant(db: Session, restaurant_id: int) -> bool:
    """Delete restaurant"""
    restaurant = get_restaurant(db, restaurant_id)
    if not restaurant:
        return False
    db.delete(restaurant)
    db.commit()
    return True


def get_restaurant_by_name(db: Session, tenant_id: int, name: str) -> Restaurant | None:
    """Get restaurant by name within a tenant"""
    return (
        db.query(Restaurant)
        .filter(Restaurant.tenant_id == tenant_id, Restaurant.name == name)
        .first()
    )
