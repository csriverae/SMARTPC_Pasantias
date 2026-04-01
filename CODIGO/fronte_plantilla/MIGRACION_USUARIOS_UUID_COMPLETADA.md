# ✅ Migración de Sistema de Usuarios a UUID Multi-Tenant - COMPLETADA

## Resumen Ejecutivo

El sistema de autenticación y gestión de usuarios ha sido completamente modernizado para soportar:
- **UUID** como identificadores (en lugar de enteros secuenciales)
- **Multi-tenancy real** con tabla junction `user_tenants`
- **Roles por tenant** - un usuario puede tener roles diferentes en distintas organizaciones
- **Tokens JWT enriquecidos** con tenant_id y role

## Cambios Arquitectónicos

### Estructura de Datos - ANTES vs DESPUÉS

#### ANTES (Schema Antiguo):
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE,
    password VARCHAR,
    tenant_id INTEGER,  -- ❌ Directo en tabla users
    role ENUM('admin', 'employee'),  -- ❌ Directo en tabla users
    is_active BOOLEAN
);
```
**Problema**: Un usuario solo puede pertenencer a UN tenant

#### DESPUÉS (Schema Nuevo):
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE,
    password VARCHAR,
    is_active BOOLEAN
    -- ✅ NO tenant_id, NO role aquí
);

CREATE TABLE user_tenants (
    user_id UUID FOREIGN KEY,
    tenant_id UUID FOREIGN KEY,
    role ENUM('admin', 'employee'),  -- ✅ Role es por tenant
    PRIMARY KEY (user_id, tenant_id)
);
```
**Ventaja**: Un usuario puede pertenecer a MÚLTIPLES tenants con roles diferentes

## Archivos Actualizados

### 1. **Schemas Pydantic** (`app/schemas/user.py`) ✅
**Cambios principales:**
```python
class UserCreate(BaseModel):
    email: str
    password: str
    tenant_id: UUID  # ✅ Ahora es UUID
    role: UserRole  # ✅ Nuevo campo (admin/employee)

class UserResponse(BaseModel):
    id: UUID  # ✅ ID es UUID
    email: str
    is_active: bool
    # ✅ Removed: tenant_id, role, first_name, last_name, full_name
```

### 2. **CRUD Layer** (`app/crud/user.py`) ✅
**Nuevas funciones:**
```python
def create_user_with_tenant(db, user_data: UserCreate) -> tuple[User, UserTenant]:
    """Crea usuario + relación con tenant en una transacción"""

def get_tenant_users(db, tenant_id: UUID) -> List[User]:
    """Obtiene usuarios de un tenant mediante join con UserTenant"""

def get_user_tenants(db, user_id: UUID) -> List[UserTenant]:
    """Obtiene los tenants a los que pertenece un usuario"""

def update_user_role(db, user_id: UUID, tenant_id: UUID, role: UserRole):
    """Actualiza el role de un usuario en un tenant específico"""
```

### 3. **Service Layer** (`app/services/user_service.py`) ✅
**Funciones modernizadas:**

#### `register_user(db, user_data)`
```python
# ANTES: user.tenant_id  ❌
# DESPUÉS:
user, user_tenant = create_user_with_tenant(db, user_data)
access_token = create_access_token({
    "sub": user.email,
    "tenant_id": str(user_data.tenant_id),  # ✅ UUID en token
    "role": user_data.role.value  # ✅ Role en token
})
```

#### `login_user(db, login_data)`
```python
# ANTES: user.tenant_id  ❌
# DESPUÉS:
user_tenants = get_user_tenants(db, user.id)  # ✅ Query junction table
tenant_id = user_tenants[0].tenant_id
role = user_tenants[0].role
access_token = create_access_token({
    "sub": user.email,
    "tenant_id": str(tenant_id),
    "role": role.value
})
```

#### `get_all_users(db, tenant_id, skip, limit, role)`
```python
# ANTES: query = db.query(User); query.filter(User.tenant_id == tenant_id)  ❌
# DESPUÉS:
users = get_tenant_users(db, tenant_id)  # ✅ Join automático con UserTenant
```

#### `update_user_profile_admin(db, user_id, update_data, tenant_id)`
```python
# ANTES: user.tenant_id != tenant_id  ❌
# DESPUÉS:
user_tenant = db.query(UserTenant).filter(
    UserTenant.user_id == user_id,
    UserTenant.tenant_id == tenant_id
).first()
# ✅ Valida pertenencia a tenant
```

### 4. **API Routes** (`app/api/routes/user.py`) ✅
**Endpoints actualizados:**

#### Authentication
| Endpoint | Cambios | Status |
|----------|---------|--------|
| `POST /register` | Acepta UUID tenant_id, role en token | ✅ |
| `POST /login` | Obtiene tenant_id de UserTenant, incluye role | ✅ |
| `POST /refresh` | Token con tenant_id + role | ✅ |

#### Profile
| Endpoint | Cambios | Status |
|----------|---------|--------|
| `GET /me` | Sin cambios | ✅ |
| `PATCH /me` | Actualiza usuario actual | ✅ |
| `DELETE /me` | Obtiene tenant_id de UserTenant | ✅ |

#### Admin Management
| Endpoint | Cambios | Status |
|----------|---------|--------|
| `GET /users` | Requiere tenant_id como parámetro | ✅ |
| `GET /users/{user_id}` | user_id es UUID (string para parsing) | ✅ |
| `PATCH /users/{user_id}` | Valida pertenencia a tenant | ✅ |
| `DELETE /users/{user_id}` | Requiere tenant_id de UserTenant | ✅ |

### 5. **Security Layer** (`app/core/security.py`) ✅
**Sistema de tokens mejorado:**
```python
def get_current_user(token, db):
    payload = verify_token(token)
    email = payload.get("sub")
    tenant_id = payload.get("tenant_id")  # ✅ Nuevo
    role = payload.get("role")  # ✅ Nuevo
    
    user = get_user_by_email(db, email)
    user.tenant_id = UUID(tenant_id)  # ✅ Attach para compatibilidad
    user.role_name = role
    return user
```

**Token actual:**
```json
{
    "sub": "user@example.com",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
    "role": "admin",
    "exp": 1234567890
}
```

## Flujo de Autenticación

### Registro (Register)
```
1. POST /register { email, password, tenant_id: UUID, role: "admin" }
2. Valida: email único, solo 1 admin por tenant
3. Crea User (sin tenant_id ni role)
4. Crea UserTenant (user_id, tenant_id, role)
5. Genera token con {sub: email, tenant_id, role}
6. Retorna { access_token, tenant_id }
```

### Login
```
1. POST /login { email, password }
2. Valida password
3. Query: SELECT * FROM user_tenants WHERE user_id = ?
4. Si no hay tenants → InvalidCredentials
5. Usa primer tenant: tenant_id = first_user_tenant.tenant_id, role = first_user_tenant.role
6. Genera token con {sub: email, tenant_id, role}
7. Retorna { access_token, refresh_token, tenant_id }
```

### Operaciones Multi-Tenant
```
1. Admin realiza acción: PATCH /users/{user_id}
2. Extrae de token: tenant_id (admin's tenant)
3. Verifica: ¿usuario_a_actualizar está en este tenant?
4. Query: SELECT * FROM user_tenants 
          WHERE user_id = {user_id} AND tenant_id = {admin's_tenant}
5. Si no existe → 404 Not Found
6. Si existe → Realiza operación solo en contexto del tenant
```

## Aislamiento Multi-Tenant

Cada endpoint de administración valida:
```python
# Obtener tenant del admin desde token
admin_tenant = db.query(UserTenant).filter(
    UserTenant.user_id == current_user.id
).first()

# Verificar que usuario destino está en mismo tenant
target_user_tenant = db.query(UserTenant).filter(
    UserTenant.user_id == target_user_id,
    UserTenant.tenant_id == admin_tenant.tenant_id  # ✅ Mismo tenant
).first()

if not target_user_tenant:
    raise ResourceNotFoundError()  # No existe en este tenant
```

## Beneficios

✅ **Seguridad mejorada**: UUID vs secuencial reduces predictability
✅ **Multi-tenancy real**: Un usuario en múltiples organizaciones
✅ **Roles contextuales**: Admin en una org, employee en otra
✅ **Escalabilidad**: Fácil agregar más tenants
✅ **Migración limpia**: Separación clara de concerns (User vs UserTenant)

## Testing Recomendado

### 1. Registro de usuario
```bash
POST /register
{
  "email": "admin@company.com",
  "password": "SecurePass123!",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
  "role": "admin"
}

Esperado: 201 Created con { access_token, tenant_id }
```

### 2. Login multi-tenant
```bash
# Usuario en dos tenants
POST /login { "email": "user@company.com", "password": "..." }
Esperado: Token con primer tenant_id

# Usuario en otro tenant (misma persona)
POST /register { ..., "tenant_id": "otro-uuid", "role": "employee" }
Esperado: Nuevo UserTenant creado
```

### 3. Aislamiento de datos
```bash
# Admin A intenta ver usuarios de Admin B
GET /users
- Token contiene tenant_id de Admin A
- Response solo contiene usuarios de tenant A
- Admin B usuarios NO visibles ✅
```

### 4. Validación de pertenencia
```bash
# Admin A intenta actualizar usuario de Admin B
PATCH /users/{usuario_b_id} { ... }
- Endpoint verifica: ¿usuario_b está en tenant de Admin A?
- Si NO → 404 Not Found ✅
```

## Notas Importantes

⚠️ **Si hay datos existentes:**
- Requiere migración Alembic para convertir datos antiguos
- Crear registros UserTenant basados en User.tenant_id antiguo
- Se puede usar `rebuild_db.py` para resetear si es desarrollo

⚠️ **Compatibilidad frontend:**
- IDs ahora son UUID strings (no integers)
- Token contiene `role` - frontend puede validar localmente
- Tenant_id es UUID - debe almacenarse como string en localStorage

## Próximos Pasos

1. ✅ Actualizar backend models/schemas/routes
2. ⏳ **Generar migración Alembic** (si hay datos existentes):
   ```bash
   alembic revision --autogenerate -m "Add user_tenants table"
   alembic upgrade head
   ```
3. ⏳ **Actualizar frontend** para usar UUID strings
4. ⏳ **Testing end-to-end** con Postman collection
5. ⏳ **Deploy a staging**

## Estado de Completion

| Componente | Estado | Archivos |
|-----------|--------|----------|
| Models SQLAlchemy | ✅ Completo | user.py, tenant.py |
| Schemas Pydantic | ✅ Completo | schemas/user.py |
| CRUD Layer | ✅ Completo | crud/user.py |
| Service Layer | ✅ Completo | services/user_service.py |
| API Routes | ✅ Completo | api/routes/user.py |
| Security/Tokens | ✅ Completo | core/security.py |
| Database | ✅ Existente | PostgreSQL mesa_db |

**Resultado**: ✅ 100% COMPLETADO - Sistema listo para testing
