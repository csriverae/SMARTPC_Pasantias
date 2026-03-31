"""
Restaurant management routes - Multi-tenant filtered
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse, RestaurantListResponse
from app.core.security import get_current_user
from app.api.dependencies import get_db
from app.api.utils.response import success_response, created_response
from app.services.restaurant_service import restaurant_service

router = APIRouter()


@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create restaurant in user's tenant",
    tags=["Restaurants"]
)
def create_restaurant(
    restaurant_data: RestaurantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new restaurant (authenticated users only)"""
    restaurant = restaurant_service.create_restaurant(db, current_user, restaurant_data)
    
    return created_response(
        message="Restaurant created successfully",
        data=restaurant
    )


@router.get(
    "/",
    response_model=List[RestaurantListResponse],
    status_code=status.HTTP_200_OK,
    summary="List restaurants in user's tenant",
    tags=["Restaurants"]
)
def list_restaurants(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of restaurants for authenticated user's tenant"""
    restaurants = restaurant_service.get_restaurants_for_tenant(
        db,
        current_user,
        skip=skip,
        limit=limit
    )
    
    return success_response(
        message=f"Retrieved {len(restaurants)} restaurants",
        data=restaurants
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
    status_code=status.HTTP_200_OK,
    summary="Get restaurant by ID",
    tags=["Restaurants"]
)
def get_restaurant_endpoint(
    restaurant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific restaurant (must belong to user's tenant)"""
    restaurant = restaurant_service.get_restaurant(db, current_user, restaurant_id)
    
    return success_response(
        message="Restaurant retrieved successfully",
        data=restaurant
    )


@router.patch(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
    status_code=status.HTTP_200_OK,
    summary="Update restaurant",
    tags=["Restaurants"]
)
def update_restaurant_endpoint(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update restaurant (must belong to user's tenant)"""
    restaurant = restaurant_service.update_restaurant(
        db,
        current_user,
        restaurant_id,
        restaurant_data
    )
    
    return success_response(
        message="Restaurant updated successfully",
        data=restaurant
    )


@router.delete(
    "/{restaurant_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete restaurant",
    tags=["Restaurants"]
)
def delete_restaurant_endpoint(
    restaurant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete restaurant (must belong to user's tenant)"""
    restaurant_service.delete_restaurant(db, current_user, restaurant_id)
    
    return success_response(
        message="Restaurant deleted successfully",
        data={"restaurant_id": restaurant_id}
    )
