"""
Script to verify tenants in PostgreSQL
"""

from app.db.session import engine
from sqlalchemy import text

def check_tenants():
    """List all tenants"""
    try:
        with engine.connect() as con:
            result = con.execute(text("SELECT id, name, slug, type, created_at FROM tenants ORDER BY created_at DESC;"))
            tenants = result.fetchall()
            
            print(f"\n✅ Database connected")
            print(f"📋 Tenants found: {len(tenants)}\n")
            
            if tenants:
                print("Tenants:")
                for tenant in tenants:
                    print(f"  ID: {tenant[0]}")
                    print(f"  Name: {tenant[1]}")
                    print(f"  Slug: {tenant[2]}")
                    print(f"  Type: {tenant[3]}")
                    print(f"  Created: {tenant[4]}\n")
            else:
                print("  (No tenants found - need to insert default tenant)")
            
            return tenants
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    check_tenants()
