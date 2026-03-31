from app.db.session import engine
from sqlalchemy import text
from datetime import datetime

with engine.connect() as conn:
    conn.execute(text("""
        INSERT INTO tenants (id, name, slug, is_active, created_at)
        VALUES (1, 'Default Tenant', 'default', 1, :now)
        ON CONFLICT (id) DO NOTHING
    """), {"now": datetime.utcnow()})
    conn.commit()
    result = conn.execute(text('SELECT * FROM tenants'))
    print('Tenants:', result.fetchall())