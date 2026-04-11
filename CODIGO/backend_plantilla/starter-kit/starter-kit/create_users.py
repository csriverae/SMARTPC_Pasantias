from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

db = SessionLocal()
try:
    # Crear usuario admin
    admin_user = User(
        email="admin@example.com",
        password=get_password_hash("admin123"),
        full_name="Admin User",
        role=UserRole.admin
    )
    db.add(admin_user)

    # Crear usuario employee
    employee_user = User(
        email="employee@example.com",
        password=get_password_hash("employee123"),
        full_name="Employee User",
        role=UserRole.employee
    )
    db.add(employee_user)

    db.commit()
    print("Usuarios creados:")
    print(f"Admin: {admin_user.email} - {admin_user.role}")
    print(f"Employee: {employee_user.email} - {employee_user.role}")
except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()