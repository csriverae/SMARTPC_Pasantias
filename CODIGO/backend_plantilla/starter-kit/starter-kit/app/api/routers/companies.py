"""Companies Router for SaaS Multi-Tenant"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud.company import create_company, get_companies, get_company_by_id
from app.core.security import get_current_user, get_current_tenant
from app.schemas.company import CompanyCreate, CompanyResponse
from uuid import UUID


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/companies", tags=["Companies"], response_model=None)
def create_company_endpoint(
    company_data: CompanyCreate,
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Create new company
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
        
        new_company = create_company(
            db=db,
            company=company_data,
            tenant_id=tenant_uuid
        )
        
        return JSONResponse(
            status_code=201,
            content={
                "message": "Compañía creada exitosamente",
                "status": 201,
                "error": False,
                "data": {
                    "data": {
                        "id": new_company.id,
                        "name": new_company.name,
                        "ruc": new_company.ruc,
                        "tenant_id": str(new_company.tenant_id) if new_company.tenant_id else None
                    }
                }
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
                "message": f"Error al crear compañía: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )


@router.get("/companies", tags=["Companies"], response_model=None)
def get_companies_endpoint(
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Get all companies for a tenant
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
        
        companies = get_companies(db=db, tenant_id=tenant_uuid)
        
        companies_data = [
            {
                "id": company.id,
                "name": company.name,
                "ruc": company.ruc,
                "tenant_id": str(company.tenant_id) if company.tenant_id else None
            }
            for company in companies
        ]
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Compañías obtenidas exitosamente",
                "status": 200,
                "error": False,
                "data": {"data": companies_data}
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
                "message": f"Error al obtener compañías: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": []}
            }
        )


@router.get("/companies/{company_id}", tags=["Companies"], response_model=None)
def get_company_endpoint(
    company_id: int,
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Get company by ID
    Headers required: Authorization: Bearer <token>, X-Tenant-ID: <tenant_id>
    """
    try:
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Tenant-ID header requerido"
            )
        
        company = get_company_by_id(db=db, company_id=company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compañía no encontrada"
            )
        
        # Verify company belongs to tenant
        if str(company.tenant_id) != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a esta compañía"
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Compañía obtenida exitosamente",
                "status": 200,
                "error": False,
                "data": {
                    "data": {
                        "id": company.id,
                        "name": company.name,
                        "ruc": company.ruc,
                        "tenant_id": str(company.tenant_id) if company.tenant_id else None
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
                "message": f"Error al obtener compañía: {str(e)}",
                "status": 500,
                "error": True,
                "data": {"data": None}
            }
        )
