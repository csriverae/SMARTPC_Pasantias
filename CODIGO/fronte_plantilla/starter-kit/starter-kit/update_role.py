from app.db.session import SessionLocal
from app.models.user import User, UserRole

db = SessionLocal()
try:
    user = db.query(User).filter(User.email == "carlos@gmail.com").first()
    if user:
        user.role = UserRole.admin
        db.commit()
        print(f"Updated role for {user.email} to {user.role}")
    else:
        print("User not found")
finally:
    db.close()