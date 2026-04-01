#!/usr/bin/env python
"""Seed initial data for multi-tenant system."""

from datetime import datetime
import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import bcrypt
from app.db.session import engine

def hash_pwd(password):
    """Hash password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Create default tenant (Company)
    default_tenant_id = str(uuid.uuid4())
    db.execute(text("""
        INSERT INTO tenants (id, name, slug, type, created_at) 
        VALUES (:id, :name, :slug, :type, NOW())
    """), {
        "id": default_tenant_id,
        "name": "Default Company",
        "slug": "default-company",
        "type": "company"
    })
    print(f"✓ Created tenant: Default Company")
    
    # Create KFC tenant (Restaurant)
    kfc_tenant_id = str(uuid.uuid4())
    db.execute(text("""
        INSERT INTO tenants (id, name, slug, type, created_at) 
        VALUES (:id, :name, :slug, :type, NOW())
    """), {
        "id": kfc_tenant_id,
        "name": "KFC",
        "slug": "kfc",
        "type": "restaurant"
    })
    print(f"✓ Created tenant: KFC")
    
    # Create admin user
    admin_id = str(uuid.uuid4())
    admin_pwd = hash_pwd("123456")
    db.execute(text("""
        INSERT INTO users (id, email, password, is_active, created_at)
        VALUES (:id, :email, :password, true, NOW())
    """), {
        "id": admin_id,
        "email": "admin@company.com",
        "password": admin_pwd
    })
    print(f"✓ Created user: admin@company.com")
    
    # Assign admin to company
    db.execute(text("""
        INSERT INTO user_tenants (id, user_id, tenant_id, role, created_at)
        VALUES (:id, :user_id, :tenant_id, :role, NOW())
    """), {
        "id": str(uuid.uuid4()),
        "user_id": admin_id,
        "tenant_id": default_tenant_id,
        "role": "admin"
    })
    print(f"✓ Assigned admin to company")
    
    # Create employee user
    employee_id = str(uuid.uuid4())
    employee_pwd = hash_pwd("123456")
    db.execute(text("""
        INSERT INTO users (id, email, password, is_active, created_at)
        VALUES (:id, :email, :password, true, NOW())
    """), {
        "id": employee_id,
        "email": "employee@company.com",
        "password": employee_pwd
    })
    print(f"✓ Created user: employee@company.com")
    
    # Assign employee to company
    db.execute(text("""
        INSERT INTO user_tenants (id, user_id, tenant_id, role, created_at)
        VALUES (:id, :user_id, :tenant_id, :role, NOW())
    """), {
        "id": str(uuid.uuid4()),
        "user_id": employee_id,
        "tenant_id": default_tenant_id,
        "role": "employee"
    })
    print(f"✓ Assigned employee to company")
    
    db.commit()
    
    # Verify
    result = db.execute(text("SELECT id, name, type FROM tenants"))
    print("\n✅ Tenants inserted:")
    for row in result:
        print(f"  - {row[1]} ({row[2]}): {row[0]}")
    
    print("\n" + "="*60)
    print("TEST CREDENTIALS")
    print("="*60)
    print("Admin:    admin@company.com / 123456")
    print("Employee: employee@company.com / 123456")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
