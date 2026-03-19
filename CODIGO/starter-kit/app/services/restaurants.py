from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant
from app.models.user import UserRole
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:
    @staticmethod
    async def create_restaurant(db: AsyncSession, current_user, restaurant_in: RestaurantCreate):
        if current_user.role.value not in [UserRole.restaurant_admin.value, UserRole.super_admin.value]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")

        q = select(Restaurant).where(Restaurant.ruc == restaurant_in.ruc)
        result = await db.execute(q)
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="RUC already exists")

        new_restaurant = Restaurant(
            user_id=current_user.id,
            name=restaurant_in.name,
            ruc=restaurant_in.ruc,
            address=restaurant_in.address,
            phone=restaurant_in.phone,
            logo_url=restaurant_in.logo_url,
            subscription_plan=restaurant_in.subscription_plan,
            subscription_expires_at=restaurant_in.subscription_expires_at,
            is_active=restaurant_in.is_active,
            created_at=datetime.utcnow(),
        )

        db.add(new_restaurant)
        await db.commit()
        await db.refresh(new_restaurant)
        return new_restaurant

    @staticmethod
    async def get_restaurants(db: AsyncSession, current_user) -> List[Restaurant]:
        q = select(Restaurant)
        if current_user.role.value == UserRole.restaurant_admin.value:
            q = q.where(Restaurant.user_id == current_user.id)

        result = await db.execute(q)
        return result.scalars().all()

    @staticmethod
    async def get_restaurant_by_id(db: AsyncSession, restaurant_id: str, current_user):
        q = select(Restaurant).where(Restaurant.id == restaurant_id)
        result = await db.execute(q)
        restaurant = result.scalar_one_or_none()

        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

        if current_user.role.value == UserRole.restaurant_admin.value and restaurant.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")

        return restaurant

    @staticmethod
    async def update_restaurant(db: AsyncSession, restaurant_id: str, restaurant_in: RestaurantUpdate, current_user):
        restaurant = await RestaurantService.get_restaurant_by_id(db, restaurant_id, current_user)

        if restaurant_in.ruc and restaurant_in.ruc != restaurant.ruc:
            q = select(Restaurant).where(Restaurant.ruc == restaurant_in.ruc)
            result = await db.execute(q)
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="RUC already exists")

        for field, value in restaurant_in.model_dump(exclude_unset=True).items():
            setattr(restaurant, field, value)

        await db.commit()
        await db.refresh(restaurant)
        return restaurant

    @staticmethod
    async def deactivate_restaurant(db: AsyncSession, restaurant_id: str, current_user):
        restaurant = await RestaurantService.get_restaurant_by_id(db, restaurant_id, current_user)
        restaurant.is_active = False
        await db.commit()
        await db.refresh(restaurant)
        return restaurant
