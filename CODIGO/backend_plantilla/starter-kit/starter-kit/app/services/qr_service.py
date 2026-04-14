"""QR Code Generation and Validation Service"""
import io
import base64
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.employee import Employee
from uuid import UUID
from PIL import Image
import qrcode


class QRService:
    """Handle QR code generation and validation"""
    
    @staticmethod
    def generate_qr_image(employee_id: int, qr_token: str) -> bytes:
        """Generate QR code image (PNG bytes)"""
        try:
            qr_data = f"employee:{employee_id}:token:{qr_token}"
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return img_bytes.getvalue()
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating QR image: {str(e)}"
            )
    
    @staticmethod
    def get_employee_qr_image(db: Session, employee_id: int, tenant_id: UUID):
        """Get employee QR code as PNG image"""
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        
        if not employee or employee.company_tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        # Generate QR image
        qr_image_bytes = QRService.generate_qr_image(employee.id, employee.qr_token)
        
        return qr_image_bytes
    
    @staticmethod
    def get_qr_code_base64(employee_id: int, qr_token: str) -> str:
        """Generate QR code as base64 string"""
        try:
            qr_image_bytes = QRService.generate_qr_image(employee_id, qr_token)
            qr_base64 = base64.b64encode(qr_image_bytes).decode('utf-8')
            return qr_base64
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating QR base64: {str(e)}"
            )
    
    @staticmethod
    def get_qr_code_text(employee_id: int, qr_token: str) -> str:
        """Get QR code data as text (what's encoded in the QR)"""
        return f"employee:{employee_id}:token:{qr_token}"
    
    @staticmethod
    def validate_qr_token(db: Session, qr_token: str, tenant_id: UUID):
        """Validate QR token"""
        employee = db.query(Employee).filter(Employee.qr_token == qr_token).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token QR inválido"
            )
        
        if employee.company_tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado"
            )
        
        return employee
