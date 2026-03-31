#!/usr/bin/env python3
"""
Script para verificar datos en PostgreSQL - Sistema Multi-Tenant MesaPass
Uso: python verify_database.py
"""

import sqlalchemy
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Cargar variables de ambiente
load_dotenv()

DATABASE_URL = "postgresql://postgres:1234@localhost:5434/mesa_db"

def connect_db():
    """Conectar a la base de datos"""
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        print("✅ Conectado a PostgreSQL exitosamente\n")
        return connection
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        exit(1)

def show_tenants(conn):
    """Mostrar todos los tenants"""
    print("=" * 60)
    print("📋 TENANTS")
    print("=" * 60)
    
    query = text("""
        SELECT 
            id,
            name,
            created_at,
            (SELECT COUNT(*) FROM users WHERE tenant_id = tenants.id) as user_count,
            (SELECT COUNT(*) FROM restaurants WHERE tenant_id = tenants.id) as restaurant_count
        FROM tenants
        ORDER BY id;
    """)
    
    result = conn.execute(query)
    rows = result.fetchall()
    
    if not rows:
        print("❌ No hay tenants en la BD")
        return
    
    print(f"{'ID':<5} {'Name':<30} {'Users':<8} {'Restaurants':<12} {'Created':<20}")
    print("-" * 75)
    
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<30} {row[3]:<8} {row[4]:<12} {str(row[2]):<20}")
    
    print(f"\n✅ Total de tenants: {len(rows)}\n")

def show_users(conn):
    """Mostrar todos los usuarios"""
    print("=" * 80)
    print("👥 USUARIOS")
    print("=" * 80)
    
    query = text("""
        SELECT 
            id,
            email,
            full_name,
            role,
            tenant_id,
            is_active,
            created_at
        FROM users
        ORDER BY id;
    """)
    
    result = conn.execute(query)
    rows = result.fetchall()
    
    if not rows:
        print("❌ No hay usuarios en la BD")
        return
    
    print(f"{'ID':<5} {'Email':<25} {'Name':<20} {'Role':<15} {'Tenant':<8} {'Active':<7} {'Created':<20}")
    print("-" * 100)
    
    for row in rows:
        email = row[1][:24] if len(row[1]) > 24 else row[1]
        name = row[2][:19] if row[2] and len(row[2]) > 19 else row[2]
        print(f"{row[0]:<5} {email:<25} {str(name):<20} {row[3]:<15} {row[4]:<8} {row[5]:<7} {str(row[6]):<20}")
    
    print(f"\n✅ Total de usuarios: {len(rows)}\n")

def show_restaurants(conn):
    """Mostrar todos los restaurants"""
    print("=" * 80)
    print("🍽️  RESTAURANTES")
    print("=" * 80)
    
    query = text("""
        SELECT 
            id,
            name,
            address,
            tenant_id,
            is_active,
            created_at
        FROM restaurants
        ORDER BY id;
    """)
    
    result = conn.execute(query)
    rows = result.fetchall()
    
    if not rows:
        print("❌ No hay restaurants en la BD")
        return
    
    print(f"{'ID':<5} {'Name':<30} {'Address':<30} {'Tenant':<8} {'Active':<7} {'Created':<20}")
    print("-" * 100)
    
    for row in rows:
        name = row[1][:29] if len(row[1]) > 29 else row[1]
        address = row[2][:29] if row[2] and len(row[2]) > 29 else row[2]
        print(f"{row[0]:<5} {name:<30} {str(address):<30} {row[3]:<8} {row[4]:<7} {str(row[5]):<20}")
    
    print(f"\n✅ Total de restaurants: {len(rows)}\n")

def show_tenant_structure(conn):
    """Mostrar estructura completa Tenant-User-Restaurant"""
    print("=" * 100)
    print("🏗️  ESTRUCTURA MULTI-TENANT (Tenant → User → Restaurant)")
    print("=" * 100)
    
    query = text("""
        SELECT 
            t.id as tenant_id,
            t.name as tenant_name,
            u.id as user_id,
            u.email,
            u.role,
            r.id as restaurant_id,
            r.name as restaurant_name
        FROM tenants t
        LEFT JOIN users u ON u.tenant_id = t.id
        LEFT JOIN restaurants r ON r.tenant_id = t.id
        ORDER BY t.id, u.id, r.id;
    """)
    
    result = conn.execute(query)
    rows = result.fetchall()
    
    if not rows:
        print("❌ No hay datos de estructura")
        return
    
    print(f"{'Tenant':<8} {'Tenant Name':<25} {'User ID':<8} {'Email':<25} {'Role':<15} {'Restaurant':<25}")
    print("-" * 106)
    
    for row in rows:
        tenant_id = str(row[0]) if row[0] else ""
        tenant_name = row[1][:24] if row[1] and len(row[1]) > 24 else row[1]
        user_id = str(row[2]) if row[2] else ""
        email = row[3][:24] if row[3] and len(row[3]) > 24 else row[3]
        role = row[4] if row[4] else ""
        restaurant = row[6][:24] if row[6] and len(row[6]) > 24 else row[6]
        
        print(f"{tenant_id:<8} {str(tenant_name):<25} {user_id:<8} {str(email):<25} {role:<15} {str(restaurant):<25}")
    
    print()

def tenant_statistics(conn):
    """Mostrar estadísticas por tenant"""
    print("=" * 80)
    print("📊 ESTADÍSTICAS POR TENANT")
    print("=" * 80)
    
    query = text("""
        SELECT 
            t.id,
            t.name,
            COUNT(DISTINCT u.id) as user_count,
            COUNT(DISTINCT r.id) as restaurant_count
        FROM tenants t
        LEFT JOIN users u ON u.tenant_id = t.id
        LEFT JOIN restaurants r ON r.tenant_id = t.id
        GROUP BY t.id, t.name
        ORDER BY t.id;
    """)
    
    result = conn.execute(query)
    rows = result.fetchall()
    
    print(f"{'Tenant ID':<12} {'Tenant Name':<30} {'Users':<8} {'Restaurants':<12}")
    print("-" * 62)
    
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<30} {row[2]:<8} {row[3]:<12}")
    
    print()

def main():
    """Función principal"""
    print("\n")
    print("🔍 VERIFICADOR DE BASE DE DATOS - MESAPASS MULTI-TENANT")
    print("=" * 100)
    print()
    
    conn = connect_db()
    
    try:
        show_tenants(conn)
        show_users(conn)
        show_restaurants(conn)
        tenant_statistics(conn)
        show_tenant_structure(conn)
        
        print("=" * 100)
        print("✅ VERIFICACIÓN COMPLETADA")
        print("=" * 100)
        
    except Exception as e:
        print(f"❌ Error ejecutando queries: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
