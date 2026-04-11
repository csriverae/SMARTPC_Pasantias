import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine
from app.db.base import Base
from app.models import Tenant, UserTenant
from sqlalchemy.orm import sessionmaker
import uuid

# Create tables if not exist
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Create sample tenants
    tenant1 = Tenant(id=uuid.uuid4(), name="Restaurant ABC", type="restaurant")
    tenant2 = Tenant(id=uuid.uuid4(), name="Company XYZ", type="company")

    db.add(tenant1)
    db.add(tenant2)
    db.commit()

    # Assuming user with id=1 exists (admin)
    user_tenant1 = UserTenant(user_id=1, tenant_id=tenant1.id, role="admin")
    user_tenant2 = UserTenant(user_id=1, tenant_id=tenant2.id, role="admin")

    db.add(user_tenant1)
    db.add(user_tenant2)
    db.commit()

    print("Sample tenants and user_tenants created successfully")
    print(f"Tenant 1 ID: {tenant1.id}")
    print(f"Tenant 2 ID: {tenant2.id}")

except Exception as e:
    print(f"Error: {e}")
    db.rollback()

finally:
    db.close()