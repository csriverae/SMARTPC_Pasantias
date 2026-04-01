# 🚀 MesaPass UUID Multi-Tenant System - Setup Completo

## ✅ Estado Actual

### Base de Datos PostgreSQL ✓
- **Ubicación**: `postgresql://postgres:1234@localhost:5434/mesa_db`
- **Estado**: 9 tablas creadas con UUIDs
- **Tablas**: 
  - `tenants` - Organizaciones (Company o Restaurant)
  - `users` - Usuarios globales
  - `user_tenants` - Relación user-tenant con roles
  - `restaurants` - Restaurantes
  - `companies` - Empresas
  - `agreements` - Acuerdos entre empresas y restaurantes
  - `employees` - Empleados
  - `meal_logs` - Registro de comidas
  - `invitation_codes` - Códigos de invitación

### Backend FastAPI ✓
- **Puerto**: 8000
- **Host**: http://localhost:8000
- **Estado**: ✓ Corriendo
- **Endpoints**: 11 endpoints activos
  - `/auth/register` - Registrar usuario
  - `/auth/login` - Iniciar sesión
  - `/auth/refresh` - Refrescar token
  - `/auth/me` - Perfil del usuario actual
  - `/auth/change-password` - Cambiar contraseña
  - `/auth/users` - Listar usuarios (Admin)
  - `/auth/users/{user_id}` - Obtener usuario (Admin)
  - `/auth/users/{user_id}` (PATCH) - Actualizar usuario (Admin)
  - `/auth/users/{user_id}` (DELETE) - Eliminar usuario (Admin)
  - `/tenants` - Gestionar tenants
  - `/restaurants` - Gestionar restaurantes

### Frontend Next.js ✓
- **Páginas Dashboard Creadas**:
  - `/home/meals` - Gestión de comidas
  - `/home/users` - Gestión de usuarios (admin)
  - `/home/restaurants` - Gestión de restaurantes
  - `/home/employees` - Gestión de empleados
  - `/home/tenants` - Gestión de tenants
  - `/home/profile` - Perfil del usuario

## 🧪 Datos de Prueba

### Tenants Creados
1. **Default Company** (type: company)
   - ID: `67648dc8-e4b8-4d15-ac4f-37574903c9af`
   - Slug: `default-company`

2. **KFC** (type: restaurant)
   - ID: `3526aa67-2c15-42ff-9772-dca5dc86d3a0`
   - Slug: `kfc`

### Usuarios de Prueba
| Email | Password | Role | Tenant |
|-------|----------|------|--------|
| `admin@company.com` | `123456` | admin | Default Company |
| `employee@company.com` | `123456` | employee | Default Company |

## 📮 Guía Rápida de Postman

### 1. Login (Obtener Token)
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "admin@company.com",
  "password": "123456"
}
```
**Respuesta**:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "token_type": "bearer",
    "expires_in": 3600,
    "tenant_id": "67648dc8-e4b8-4d15-ac4f-37574903c9af"
  }
}
```

### 2. Usar Token en Requests
```
Header: Authorization: Bearer <access_token>
```

### 3. Registrar Nuevo Usuario
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "newuser@company.com",
  "password": "SecurePassword123",
  "tenant_id": "67648dc8-e4b8-4d15-ac4f-37574903c9af",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 4. Listar Usuarios (Admin)
```bash
GET /auth/users?skip=0&limit=100
Authorization: Bearer <access_token>
```

### 5. Actualizar Usuario (Admin)
```bash
PATCH /auth/users/{user_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Updated",
  "last_name": "Name",
  "is_active": true,
  "role": "employee"
}
```

### 6. Eliminar Usuario (Admin)
```bash
DELETE /auth/users/{user_id}
Authorization: Bearer <access_token>
```

### 7. Obtener Perfil Actual
```bash
GET /auth/me
Authorization: Bearer <access_token>
```

## 🔑 Variables de Entorno Actualizadas
```
DATABASE_URL=postgresql://postgres:1234@localhost:5434/mesa_db
SQLALCHEMY_DATABASE_URL=postgresql://postgres:1234@localhost:5434/mesa_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## 📁 Estructura de Archivos Importante
```
starter-kit/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── models/
│   │   ├── user.py               # User & UserTenant models (UUID)
│   │   ├── tenant.py             # Tenant model (UUID)
│   │   └── restaurant.py         # Restaurant model (UUID)
│   ├── api/routes/
│   │   ├── user.py               # User routes (11 endpoints)
│   │   ├── tenant.py             # Tenant routes
│   │   └── restaurant.py         # Restaurant routes
│   ├── schemas/
│   │   └── user.py               # Pydantic validation schemas
│   ├── services/
│   │   └── user_service.py       # Business logic for users
│   ├── core/
│   │   ├── security.py           # JWT & password hashing
│   │   └── config.py             # Settings
│   └── db/
│       ├── session.py            # Database session
│       └── base.py               # SQLAlchemy Base
├── migrations/
│   └── versions/
│       └── 001_uuid_schema.py    # Revision: 002_fresh_uuid_schema
├── seed_data.py                   # Script para crear datos iniciales
├── alembic.ini                    # Alembic configuration
├── requirements.txt               # Python dependencies
└── MesaPass_UUID_Collection.postman_collection.json
```

## 🧬 Esquema de Relaciones

```
Tenants (Multi-tenant base)
├─ Companies (type: company)
└─ Restaurants (type: restaurant)

Users (Global users)
└─ UserTenants (Join table for multi-tenancy)
   ├─ tenant_id (FK → Tenants)
   └─ role (admin | employee)

Restaurants
├─ tenant_id (FK → Tenants)
├─ Companies (1-to-many)
└─ MealLogs (1-to-many)

Employees
├─ user_id (FK → Users)
├─ company_tenant_id (FK → Tenants/Companies)
└─ MealLogs (1-to-many)

Agreements (Subsidy arrangements)
├─ company_tenant_id (FK → Tenants/Companies)
└─ restaurant_tenant_id (FK → Tenants/Restaurants)
```

## 🔐 Sistema de Roles

- **admin**: Acceso completo a gestión de usuarios y configuración del tenant
- **employee**: Acceso limitado, solo puede ver su propio perfil y registrar comidas

## 🚀 Próximos Pasos Recomendados

1. **Importar Postman Collection**
   - Abrir Postman
   - File → Import
   - Seleccionar `MesaPass_UUID_Collection.postman_collection.json`

2. **Probar Endpoints**
   - Usar las credenciales de prueba proporcionadas
   - Obtener access token del login
   - Usar token en otros requests

3. **Crear Datos Adicionales**
   - Restaurantes
   - Acuerdos entre empresas y restaurantes
   - Empleados

4. **Configurar Frontend**
   - Conectar Dashboard con API endpoints
   - Implementar manejo de tokens
   - Agregar validaciones front-end

## 🐛 Troubleshooting

### Error: "User not found"
- Verificar que el usuario existe en la base de datos
- Verificar que tenant_id es correcto

### Error: "Unauthorized"
- Verificar que el token no ha expirado
- Verificar que el header Authorization está correcto: `Bearer <token>`

### Error: "Admin access required"
- Verificar que el usuario tiene rol "admin"
- Verificar que el usuario está en el mismo tenant

### Error: "Invalid token"
- Obtener nuevo token con login
- Verificar que el token no ha sido modificado

## 📊 Verificación de Base de Datos

### Usando comando psql
```sql
-- Ver all tenants
SELECT id, name, type, created_at FROM tenants;

-- Ver all users
SELECT id, email, is_active, created_at FROM users;

-- Ver user-tenant relationships
SELECT ut.id, u.email, t.name, ut.role, ut.created_at 
FROM user_tenants ut
JOIN users u ON ut.user_id = u.id
JOIN tenants t ON ut.tenant_id = t.id;

-- Ver table structure
\dt              -- List all tables
\d users         -- Describe users table
```

## ✨ Características Implementadas

✓ UUID-based schema (no Integer IDs)
✓ Multi-tenant architecture with user-tenant join table
✓ JWT authentication with refresh tokens
✓ Role-based access control (admin/employee only)
✓ Password hashing with bcrypt
✓ 9 database tables with proper relationships
✓ FastAPI backend with 11 working endpoints
✓ Alembic migrations
✓ Postman collection with example requests
✓ Seed script for test data
✓ Frontend dashboard pages

## 📞 Soporte

Para consultas o problemas, revisar:
- Logs del servidor: `Terminal → FastAPI`
- PostgreSQL logs
- Postman console (F12)
- Browser console (Dev Tools)
