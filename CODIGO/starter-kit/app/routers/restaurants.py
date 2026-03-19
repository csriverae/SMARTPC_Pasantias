from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_current_user, require_role
from app.db.session import get_db
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from app.services.restaurants import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.post("/", response_model=RestaurantResponse)
async def create_restaurant(
    restaurant_in: RestaurantCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("restaurant_admin", "super_admin")),
):
    restaurant = await RestaurantService.create_restaurant(db, current_user, restaurant_in)
    return restaurant


@router.get("/", response_model=list[RestaurantResponse])
async def list_restaurants(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("restaurant_admin", "super_admin")),
):
    restaurants = await RestaurantService.get_restaurants(db, current_user)
    return restaurants


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("restaurant_admin", "super_admin")),
):
    restaurant = await RestaurantService.get_restaurant_by_id(db, restaurant_id, current_user)
    return restaurant


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: str,
    restaurant_in: RestaurantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("restaurant_admin", "super_admin")),
):
    restaurant = await RestaurantService.update_restaurant(db, restaurant_id, restaurant_in, current_user)
    return restaurant


@router.patch("/{restaurant_id}/deactivate", response_model=RestaurantResponse)
async def deactivate_restaurant(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("restaurant_admin", "super_admin")),
):
    restaurant = await RestaurantService.deactivate_restaurant(db, restaurant_id, current_user)
    return restaurant
