"""
Script to insert default tenants if they don't exist
"""

from app.db.session import engine
from sqlalchemy import text
from uuid import UUID

def insert_default_tenants():
    """Insert default tenants"""
    try:
        with engine.connect() as con:
            # Check if tenants already exist
            result = con.execute(text("SELECT COUNT(*) FROM tenants;"))
            count = result.scalar()
            
            if count > 0:
                print(f"\n✅ Tenants already exist ({count} found)")
                return
            
            print("\n➕ Inserting default tenants...")
            
            # Insert default tenants
            con.execute(text("""
                INSERT INTO tenants (id, name, slug, type, created_at)
                VALUES 
                ('96261def-bc6b-422a-9592-edaaa1874662', 'Default Company', 'default', 'company', CURRENT_TIMESTAMP),
                ('cc74d75c-db7e-41c4-a0f4-c674c2a83843', 'KFC', 'kfc', 'company', CURRENT_TIMESTAMP)
                ON CONFLICT (id) DO NOTHING;
            """))
            con.commit()
            
            print("✅ Default tenants inserted successfully!")
            
            # Show inserted tenants
            result = con.execute(text("SELECT id, name, slug FROM tenants ORDER BY created_at;"))
            tenants = result.fetchall()
            print(f"\n📋 Tenants in database:")
            for tenant in tenants:
                print(f"  - {tenant[1]} (slug: {tenant[2]})")
                print(f"    ID: {tenant[0]}\n")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    insert_default_tenants()
