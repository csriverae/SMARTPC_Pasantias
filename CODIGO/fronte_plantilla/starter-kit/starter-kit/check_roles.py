from app.db.session import SessionLocal
from app.models.user import User

db = SessionLocal()
try:
    users = db.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Email: {user.email}, Role: {user.role}, Role value: {user.role.value}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()