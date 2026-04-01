"""
Complete system verification script
Checks tables, tenants, users, and relationships
"""

from app.db.session import engine
from sqlalchemy import text

def verify_system():
    """Complete system verification"""
    try:
        with engine.connect() as con:
            print("\n" + "="*60)
            print("🔍 SISTEMA VERIFICATION - MesaPass Multi-Tenant")
            print("="*60)
            
            # 1. Check tables
            print("\n1️⃣  CHECKING TABLES...")
            result = con.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema='public' 
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result]
            
            required_tables = ['tenants', 'users', 'user_tenants']
            for table in required_tables:
                if table in tables:
                    print(f"   ✅ {table}")
                else:
                    print(f"   ❌ {table} (MISSING)")
            
            # 2. Check tenants
            print("\n2️⃣  CHECKING TENANTS...")
            result = con.execute(text("SELECT COUNT(*) FROM tenants;"))
            tenant_count = result.scalar()
            print(f"   Tenants: {tenant_count}")
            
            if tenant_count > 0:
                result = con.execute(text("SELECT name, slug FROM tenants ORDER BY created_at;"))
                for name, slug in result:
                    print(f"   ✅ {name} (slug: {slug})")
            else:
                print("   ⚠️  No tenants found")
            
            # 3. Check users
            print("\n3️⃣  CHECKING USERS...")
            result = con.execute(text("SELECT COUNT(*) FROM users;"))
            user_count = result.scalar()
            print(f"   Users: {user_count}")
            
            if user_count > 0:
                result = con.execute(text("""
                    SELECT u.email, u.full_name, t.name as tenant, ut.role
                    FROM users u
                    LEFT JOIN user_tenants ut ON u.id = ut.user_id
                    LEFT JOIN tenants t ON ut.tenant_id = t.id
                    ORDER BY u.created_at;
                """))
                for email, full_name, tenant, role in result:
                    print(f"   ✅ {email} ({full_name}) - Tenant: {tenant}, Role: {role}")
            else:
                print("   ⚠️  No users found")
            
            # 4. Check user_tenants relationships
            print("\n4️⃣  CHECKING USER-TENANT RELATIONSHIPS...")
            result = con.execute(text("SELECT COUNT(*) FROM user_tenants;"))
            rel_count = result.scalar()
            print(f"   Relationships: {rel_count}")
            
            if rel_count > 0:
                result = con.execute(text("""
                    SELECT t.name, COUNT(*) as user_count
                    FROM user_tenants ut
                    JOIN tenants t ON ut.tenant_id = t.id
                    GROUP BY t.name;
                """))
                for tenant_name, count in result:
                    print(f"   ✅ {tenant_name}: {count} user(s)")
            
            # 5. Verify admin uniqueness per tenant
            print("\n5️⃣  CHECKING ADMIN UNIQUENESS PER TENANT...")
            result = con.execute(text("""
                SELECT t.name, COUNT(*) as admin_count
                FROM user_tenants ut
                JOIN tenants t ON ut.tenant_id = t.id
                WHERE ut.role = 'admin'
                GROUP BY t.name;
            """))
            
            admin_data = result.fetchall()
            if admin_data:
                for tenant_name, admin_count in admin_data:
                    if admin_count == 1:
                        print(f"   ✅ {tenant_name}: {admin_count} admin")
                    else:
                        print(f"   ❌ {tenant_name}: {admin_count} admins (INVALID)")
            else:
                print("   ⚠️  No admins found")
            
            print("\n" + "="*60)
            print("✅ VERIFICATION COMPLETE")
            print("="*60 + "\n")
            
            return {
                'tables': len(tables),
                'tenants': tenant_count,
                'users': user_count,
                'relationships': rel_count
            }
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        return None

if __name__ == "__main__":
    verify_system()
