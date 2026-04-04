"""Agreement Service"""
from sqlalchemy.orm import Session
from app.models.agreement import Agreement
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime, date


class AgreementService:
    """Handle agreement operations"""
    
    @staticmethod
    def create_agreement(db: Session, company_id: int, restaurant_id: int, start_date: date, end_date: date, tenant_id: UUID):
        """Create new agreement"""
        if start_date >= end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio debe ser antes que la fecha de fin"
            )
        
        new_agreement = Agreement(
            company_id=company_id,
            restaurant_id=restaurant_id,
            start_date=start_date,
            end_date=end_date,
            company_tenant_id=tenant_id
        )
        
        db.add(new_agreement)
        db.commit()
        db.refresh(new_agreement)
        
        return new_agreement
    
    @staticmethod
    def get_agreement_by_id(db: Session, agreement_id: int, tenant_id: UUID):
        """Get agreement by ID"""
        agreement = db.query(Agreement).filter(Agreement.id == agreement_id).first()
        
        if not agreement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Acuerdo no encontrado"
            )
        
        if agreement.company_tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este acuerdo"
            )
        
        return agreement
    
    @staticmethod
    def get_tenant_agreements(db: Session, tenant_id: UUID, company_id: int = None):
        """Get agreements for tenant"""
        query = db.query(Agreement).filter(Agreement.company_tenant_id == tenant_id)
        
        if company_id:
            query = query.filter(Agreement.company_id == company_id)
        
        return query.all()
    
    @staticmethod
    def is_agreement_active(db: Session, agreement_id: int) -> bool:
        """Check if agreement is active"""
        agreement = db.query(Agreement).filter(Agreement.id == agreement_id).first()
        
        if not agreement:
            return False
        
        today = date.today()
        return agreement.start_date <= today <= agreement.end_date
    
    @staticmethod
    def update_agreement(db: Session, agreement_id: int, tenant_id: UUID, **kwargs):
        """Update agreement"""
        agreement = AgreementService.get_agreement_by_id(db, agreement_id, tenant_id)
        
        for key, value in kwargs.items():
            if hasattr(agreement, key) and value is not None:
                setattr(agreement, key, value)
        
        db.commit()
        db.refresh(agreement)
        
        return agreement
    
    @staticmethod
    def delete_agreement(db: Session, agreement_id: int, tenant_id: UUID):
        """Delete agreement"""
        agreement = AgreementService.get_agreement_by_id(db, agreement_id, tenant_id)
        
        db.delete(agreement)
        db.commit()
        
        return {"message": "Acuerdo eliminado"}
