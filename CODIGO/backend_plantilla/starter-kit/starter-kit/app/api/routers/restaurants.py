"""Restaurants Router for SaaS Multi-Tenant"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.restaurant import Restaurant
from app.core.security import get_current_user, get_current_tenant
from app.schemas.restaurant import RestaurantCreate
from uuid import UUID


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/restaurants", tags=["Restaurants"], response_model=None)
def create_restaurant_endpoint(
    restaurant_data: RestaurantCreate,
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Create new restaurant
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header requerido"
            )
        
        if not restaurant_data.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del restaurante es requerido"
            )
        
        # Convert tenant_id string to UUID
        try:
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de tenant_id inválido"
            )
        
        new_restaurant = Restaurant(
            name=restaurant_data.name,
            user_id=current_user.id,
            tenant_id=tenant_uuid
        )
        
        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)
        
        return JSONResponse(
            status_code=201,
            content={
                "message": "Restaurante creado exitosamente",
                "status": 201,
                "error": False,
                "data": {
                    "data": {
                        "id": new_restaurant.id,
                        "name": new_restaurant.name,
                        "user_id": new_restaurant.user_id,
                        "tenant_id": str(new_restaurant.tenant_id) if new_restaurant.tenant_id else None
                    }
                }
            }
        )
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.detail,
                "status": e.status_code,
                "error": True,
                "data": {"data": None}
            }
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error al crear restaurante: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/restaurants", tags=["Restaurants"], response_model=None)
def get_restaurants_endpoint(
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Get all restaurants for a tenant
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header requerido"
            )
        
        # Convert tenant_id string to UUID
        try:
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de tenant_id inválido"
            )
        
        restaurants = db.query(Restaurant).filter(
            Restaurant.tenant_id == tenant_uuid
        ).all()
        
        restaurants_data = [
            {
                "id": restaurant.id,
                "name": restaurant.name,
                "user_id": restaurant.user_id,
                "tenant_id": str(restaurant.tenant_id) if restaurant.tenant_id else None
            }
            for restaurant in restaurants
        ]
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Restaurantes obtenidos exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": restaurants_data}
            }
        )
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.detail,
                "status": e.status_code,
                "error": True,
                "data": {"data": []}
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error al obtener restaurantes: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": []}
            }
        )


@router.get("/restaurants/{restaurant_id}", tags=["Restaurants"], response_model=None)
def get_restaurant_endpoint(
    restaurant_id: int,
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Get restaurant by ID
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header requerido"
            )
        
        # Convert tenant_id string to UUID
        try:
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de tenant_id inválido"
            )
        
        restaurant = db.query(Restaurant).filter(
            Restaurant.id == restaurant_id,
            Restaurant.tenant_id == tenant_uuid
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurante no encontrado"
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Restaurante obtenido exitosamente",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "id": restaurant.id,
                        "name": restaurant.name,
                        "user_id": restaurant.user_id,
                        "tenant_id": str(restaurant.tenant_id) if restaurant.tenant_id else None
                    }
                }
            }
        )
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.detail,
                "status": e.status_code,
                "error": True,
                "data": {"data": None}
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error al obtener restaurante: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )
