from app.db.session import SessionLocal
from app.models.user import User

db = SessionLocal()
users = db.query(User).all()

print("Current users in database:")
print("-" * 60)
for user in users:
    print(f"Email: {user.email}")
    print(f"Full Name: {user.full_name}")
    print(f"Role: {user.role}")
    print(f"Password Hash: {user.password[:50]}...")
    print("-" * 60)

db.close()
