#!/usr/bin/env python
"""Insert test tenant into database"""
import psycopg2
from datetime import datetime

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="mesa_db",
    user="postgres",
    password="1234"
)

cur = conn.cursor()

# Insert test tenant with the UUID that the user is using
tenant_id = '96261def-bc6b-422a-9592-edaaa1874662'
tenant_name = 'KFC'
tenant_slug = 'kfc'

try:
    cur.execute("""
        INSERT INTO tenants (id, name, slug, type, created_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT(id) DO NOTHING;
    """, (tenant_id, tenant_name, tenant_slug, 'company', datetime.utcnow()))
    
    # Also insert other test tenants if needed
    cur.execute("""
        INSERT INTO tenants (name, slug, type, created_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT(slug) DO NOTHING;
    """, ('McDonald\'s', 'mcdonalds', 'company', datetime.utcnow()))
    
    conn.commit()
    print("✓ Test tenants inserted successfully!")
    
    # Verify
    cur.execute("SELECT id, name, slug FROM tenants LIMIT 5;")
    rows = cur.fetchall()
    print("\nExisting tenants:")
    for row in rows:
        print(f"  - {row[1]} (slug={row[2]}, id={row[0]})")
        
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
finally:
    cur.close()
    conn.close()
