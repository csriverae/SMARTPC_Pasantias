from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import traceback
from app.db.session import SessionLocal
from app.schemas.response import SuccessResponse, ErrorResponse
from app.schemas.company import CompanyCreate
from app.schemas.restaurant import RestaurantCreate
from app.core.security import get_current_user, get_current_tenant

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/employees")
def get_employees(tenant_id: str = Depends(get_current_tenant), db: Session = Depends(get_db)):
    try:
        from app.models.employee import Employee
        query = db.query(Employee)
        if tenant_id:
            query = query.filter(Employee.company_tenant_id == tenant_id)
        employees = query.all()

        employees_data = []
        for emp in employees:
            employees_data.append({
                "id": emp.id,
                "name": emp.name,
                "email": emp.email,
                "company_id": emp.company_id
            })

        return JSONResponse(
            status_code=200,
            content={
                "message": "Empleados obtenidos exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": employees_data}
            }
        )
    except Exception as e:
        print(f"Get employees error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al obtener empleados",
                "status": 500,
                "error": True,
                "data": {"data": []}
            }
        )


@router.get("/companies")
def get_companies(tenant_id: str = Depends(get_current_tenant), db: Session = Depends(get_db)):
    try:
        from app.models.company import Company
        query = db.query(Company)
        if tenant_id:
            query = query.filter(Company.tenant_id == tenant_id)
        companies = query.all()

        companies_data = []
        for comp in companies:
            companies_data.append({
                "id": comp.id,
                "name": comp.name,
                "restaurant_id": comp.restaurant_id
            })

        return JSONResponse(
            status_code=200,
            content={
                "message": "Compañías obtenidas exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": companies_data}
            }
        )
    except Exception as e:
        print(f"Get companies error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al obtener compañías",
                "status": 500,
                "error": True,
                "data": {"data": []}
            }
        )


@router.post("/companies")
def create_company(
    company_data: CompanyCreate,
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    try:
        from app.crud.company import create_company
        
        new_company = create_company(db, company_data, tenant_id)
        
        company_response = {
            "id": new_company.id,
            "name": new_company.name,
            "ruc": new_company.ruc,
            "restaurant_id": new_company.restaurant_id,
            "tenant_id": str(new_company.tenant_id) if new_company.tenant_id else None
        }
        
        return JSONResponse(
            status_code=201,
            content={
                "message": "Compañía creada exitosamente",
                "status": 201,
                "error": False,
                "data": {"data": company_response}
            }
        )
    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content={
                "message": str(ve),
                "status": 400,
                "error": True,
                "data": {"data": None}
            }
        )
    except Exception as e:
        db.rollback()
        print(f"Create company error: {e}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error al crear compañía: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/restaurants")
def get_restaurants(tenant_id: str = Depends(get_current_tenant), db: Session = Depends(get_db)):
    try:
        from app.models.restaurant import Restaurant
        query = db.query(Restaurant)
        if tenant_id:
            query = query.filter(Restaurant.tenant_id == tenant_id)
        restaurants = query.all()

        restaurants_data = []
        for rest in restaurants:
            restaurants_data.append({
                "id": rest.id,
                "name": rest.name,
                "user_id": rest.user_id,
                "tenant_id": str(rest.tenant_id) if rest.tenant_id else None
            })

        return JSONResponse(
            status_code=200,
            content={
                "message": "Restaurantes obtenidos exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": restaurants_data}
            }
        )
    except Exception as e:
        print(f"Get restaurants error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al obtener restaurantes",
                "status": 500,
                "error": True,
                "data": {"data": []}
            }
        )


@router.post("/restaurants")
def create_restaurant(
    restaurant_data: RestaurantCreate,
    current_user: dict = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    try:
        from app.models.restaurant import Restaurant

        if not restaurant_data.name:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "El nombre del restaurante es requerido",
                    "status": 400,
                    "error": True,
                    "data": {"data": None}
                }
            )

        new_restaurant = Restaurant(
            name=restaurant_data.name,
            user_id=current_user.id,
            tenant_id=tenant_id
        )

        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)

        restaurant_response = {
            "id": new_restaurant.id,
            "name": new_restaurant.name,
            "user_id": new_restaurant.user_id,
            "tenant_id": str(new_restaurant.tenant_id) if new_restaurant.tenant_id else None
        }

        return JSONResponse(
            status_code=201,
            content={
                "message": "Restaurante creado exitosamente",
                "status": 201,
                "error": False,
                "data": {"data": restaurant_response}
            }
        )
    except Exception as e:
        db.rollback()
        print(f"Create restaurant error: {e}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error al crear restaurante: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )
