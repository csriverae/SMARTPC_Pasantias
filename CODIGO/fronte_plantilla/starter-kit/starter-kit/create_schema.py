from app.db.session import engine
from sqlalchemy import text

sql_script = """
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- TENANTS
CREATE TABLE IF NOT EXISTS tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- USERS
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  full_name VARCHAR(255),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- USER_TENANTS (RELACIÓN + ROLES)
CREATE TABLE IF NOT EXISTS user_tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
  role VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, tenant_id)
);

-- COMPANIES
CREATE TABLE IF NOT EXISTS companies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RESTAURANTS
CREATE TABLE IF NOT EXISTS restaurants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  address TEXT,
  phone VARCHAR(20),
  email VARCHAR(255),
  latitude FLOAT,
  longitude FLOAT,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AGREEMENTS (empresa ↔ restaurante)
CREATE TABLE IF NOT EXISTS agreements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_tenant_id UUID REFERENCES tenants(id),
  restaurant_tenant_id UUID REFERENCES tenants(id),
  subsidy_type VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- EMPLOYEES
CREATE TABLE IF NOT EXISTS employees (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  company_tenant_id UUID REFERENCES tenants(id),
  cedula VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MEAL LOGS
CREATE TABLE IF NOT EXISTS meal_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  employee_id UUID REFERENCES employees(id),
  restaurant_tenant_id UUID REFERENCES tenants(id),
  agreement_id UUID REFERENCES agreements(id),
  consumed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INVITATION CODES
CREATE TABLE IF NOT EXISTS invitation_codes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(100) UNIQUE NOT NULL,
  tenant_id UUID REFERENCES tenants(id),
  role VARCHAR(50),
  is_used BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS ix_tenants_name ON tenants(name);
CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);
CREATE INDEX IF NOT EXISTS ix_user_tenants_user_id ON user_tenants(user_id);
CREATE INDEX IF NOT EXISTS ix_user_tenants_tenant_id ON user_tenants(tenant_id);
CREATE INDEX IF NOT EXISTS ix_companies_tenant_id ON companies(tenant_id);
CREATE INDEX IF NOT EXISTS ix_restaurants_tenant_id ON restaurants(tenant_id);
CREATE INDEX IF NOT EXISTS ix_restaurants_name ON restaurants(name);
CREATE INDEX IF NOT EXISTS ix_agreements_company_tenant_id ON agreements(company_tenant_id);
CREATE INDEX IF NOT EXISTS ix_agreements_restaurant_tenant_id ON agreements(restaurant_tenant_id);
CREATE INDEX IF NOT EXISTS ix_employees_user_id ON employees(user_id);
CREATE INDEX IF NOT EXISTS ix_employees_company_tenant_id ON employees(company_tenant_id);
CREATE INDEX IF NOT EXISTS ix_meal_logs_employee_id ON meal_logs(employee_id);
CREATE INDEX IF NOT EXISTS ix_meal_logs_restaurant_tenant_id ON meal_logs(restaurant_tenant_id);
CREATE INDEX IF NOT EXISTS ix_invitation_codes_code ON invitation_codes(code);
CREATE INDEX IF NOT EXISTS ix_invitation_codes_tenant_id ON invitation_codes(tenant_id);
"""

with engine.connect() as conn:
    for statement in sql_script.split(';'):
        statement = statement.strip()
        if statement:
            conn.execute(text(statement))
    conn.commit()
    print("✓ Schema created successfully!")
    
    # Verify tables
    result = conn.execute(text("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema='public' AND table_type='BASE TABLE'
        ORDER BY table_name
    """))
    tables = [row[0] for row in result.fetchall()]
    print(f"\n✓ Created tables: {', '.join(tables)}")
