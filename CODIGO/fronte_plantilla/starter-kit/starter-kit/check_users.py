"""
Script to verify users in PostgreSQL with tenant info
"""

from app.db.session import engine
from sqlalchemy import text

def check_users():
    """List all users with their tenant and role info"""
    try:
        with engine.connect() as con:
            result = con.execute(text("""
                SELECT u.id, u.email, u.first_name, u.last_name, u.full_name, 
                       u.is_active, u.created_at,
                       t.name as tenant_name, ut.role
                FROM users u
                LEFT JOIN user_tenants ut ON u.id = ut.user_id
                LEFT JOIN tenants t ON ut.tenant_id = t.id
                ORDER BY u.created_at DESC;
            """))
            users = result.fetchall()
            
            print(f"\n✅ Database connected")
            print(f"👥 Users found: {len(users)}\n")
            
            if users:
                print("Users:")
                for user in users:
                    print(f"  ID: {user[0]}")
                    print(f"  Email: {user[1]}")
                    print(f"  Name: {user[3]}, {user[2]} (Full: {user[4]})")
                    print(f"  Active: {user[5]}")
                    print(f"  Tenant: {user[7]} | Role: {user[8]}")
                    print(f"  Created: {user[6]}\n")
            else:
                print("  (No users found)")
            
            return users
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    check_users()
