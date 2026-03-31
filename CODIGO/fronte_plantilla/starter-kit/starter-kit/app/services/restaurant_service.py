"""
Restaurant service layer - Business logic for restaurant operations
"""
from sqlalchemy.orm import Session
from typing import Optional, List
import logging

from app.models.restaurant import Restaurant
from app.models.user import User
from app.crud.restaurant import (
    create_restaurant as crud_create_restaurant,
    get_restaurant,
    get_restaurants_by_tenant,
    update_restaurant as crud_update_restaurant,
    delete_restaurant as crud_delete_restaurant,
    get_restaurant_by_name,
)
from app.crud.tenant import get_tenant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.core.exceptions import (
    ValidationError,
    ResourceNotFoundError,
    AuthorizationError,
    ConflictError,
)

logger = logging.getLogger(__name__)


class RestaurantService:
    """Service class for restaurant operations"""

    @staticmethod
    def create_restaurant(
        db: Session,
        current_user: User,
        restaurant_data: RestaurantCreate
    ) -> Restaurant:
        """
        Create a new restaurant for the user's tenant
        
        Args:
            db: Database session
            current_user: Authenticated user
            restaurant_data: Restaurant creation data
        
        Returns:
            Created restaurant object
        
        Raises:
            ValidationError: If validation fails
            ConflictError: If restaurant name already exists in tenant
        """
        # Check if tenant exists
        tenant = get_tenant(db, current_user.tenant_id)
        if not tenant:
            raise ResourceNotFoundError(
                message="Tenant not found",
                details={"tenant_id": current_user.tenant_id}
            )

        # Check if restaurant with same name exists in this tenant
        existing = get_restaurant_by_name(db, current_user.tenant_id, restaurant_data.name)
        if existing:
            logger.warning(
                f"Attempted to create restaurant with existing name: {restaurant_data.name} "
                f"in tenant {current_user.tenant_id}"
            )
            raise ConflictError(
                message=f"Restaurant '{restaurant_data.name}' already exists in your tenant",
                details={"field": "name"}
            )

        # Create restaurant
        restaurant_dict = {
            "tenant_id": current_user.tenant_id,
            "name": restaurant_data.name,
            "description": restaurant_data.description,
            "address": restaurant_data.address,
            "phone": restaurant_data.phone,
            "email": restaurant_data.email,
            "latitude": restaurant_data.latitude,
            "longitude": restaurant_data.longitude,
            "is_active": 1,
        }

        restaurant = crud_create_restaurant(db, restaurant_dict)
        logger.info(
            f"Restaurant created: {restaurant.name} (ID: {restaurant.id}) "
            f"for tenant {current_user.tenant_id}"
        )

        return restaurant

    @staticmethod
    def get_restaurant(
        db: Session,
        current_user: User,
        restaurant_id: int
    ) -> Restaurant:
        """
        Get restaurant ensuring it belongs to user's tenant
        
        Args:
            db: Database session
            current_user: Authenticated user
            restaurant_id: Restaurant ID
        
        Returns:
            Restaurant object
        
        Raises:
            ResourceNotFoundError: If not found
            AuthorizationError: If doesn't belong to user's tenant
        """
        restaurant = get_restaurant(db, restaurant_id)
        if not restaurant:
            raise ResourceNotFoundError(
                message="Restaurant not found",
                details={"restaurant_id": restaurant_id}
            )

        # Ensure restaurant belongs to user's tenant
        if restaurant.tenant_id != current_user.tenant_id:
            logger.warning(
                f"Unauthorized access attempt to restaurant {restaurant_id} "
                f"by user from tenant {current_user.tenant_id}"
            )
            raise AuthorizationError(
                message="You don't have access to this restaurant",
                details={"reason": "EM_NOT_IN_YOUR_TENANT"}
            )

        return restaurant

    @staticmethod
    def get_restaurants_for_tenant(
        db: Session,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> List[Restaurant]:
        """
        Get all restaurants for the user's tenant
        
        Args:
            db: Database session
            current_user: Authenticated user
            skip: Number of records to skip
            limit: Maximum number of records
        
        Returns:
            List of restaurants
        """
        return get_restaurants_by_tenant(db, current_user.tenant_id, skip=skip, limit=limit)

    @staticmethod
    def update_restaurant(
        db: Session,
        current_user: User,
        restaurant_id: int,
        update_data: RestaurantUpdate
    ) -> Restaurant:
        """
        Update restaurant
        
        Args:
            db: Database session
            current_user: Authenticated user
            restaurant_id: Restaurant ID
            update_data: Update data
        
        Returns:
            Updated restaurant object
        
        Raises:
            ResourceNotFoundError: If not found
            AuthorizationError: If doesn't belong to user's tenant
        """
        # Get and validate ownership
        restaurant = RestaurantService.get_restaurant(db, current_user, restaurant_id)

        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            return restaurant

        updated_restaurant = crud_update_restaurant(db, restaurant_id, update_dict)
        logger.info(f"Restaurant updated: {restaurant.name}")

        return updated_restaurant

    @staticmethod
    def delete_restaurant(
        db: Session,
        current_user: User,
        restaurant_id: int
    ) -> bool:
        """
        Delete restaurant
        
        Args:
            db: Database session
            current_user: Authenticated user
            restaurant_id: Restaurant ID
        
        Returns:
            True if deletion successful
        
        Raises:
            ResourceNotFoundError: If not found
            AuthorizationError: If doesn't belong to user's tenant
        """
        # Get and validate ownership
        restaurant = RestaurantService.get_restaurant(db, current_user, restaurant_id)

        crud_delete_restaurant(db, restaurant_id)
        logger.info(f"Restaurant deleted: {restaurant.name}")

        return True


# Singleton instance
restaurant_service = RestaurantService()
