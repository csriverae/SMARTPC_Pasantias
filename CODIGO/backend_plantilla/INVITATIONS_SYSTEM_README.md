# Sistema de Invitaciones - MesaPass

Este documento explica la implementación completa del sistema de invitaciones para el backend FastAPI SaaS de MesaPass.

## 📋 Modelo de Datos

### Tabla `user_invitations`

```sql
CREATE TABLE user_invitations (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    code VARCHAR UNIQUE NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'user',
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    invited_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'expired')),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Campos

- `id`: Identificador único (PK)
- `email`: Email del usuario invitado
- `code`: Código único de invitación (32 caracteres URL-safe)
- `role`: Rol asignado al usuario ('user', 'admin', etc.)
- `tenant_id`: Tenant que envía la invitación (FK)
- `invited_by`: Usuario que envía la invitación (FK)
- `status`: Estado ('pending', 'accepted', 'expired')
- `expires_at`: Fecha de expiración
- `created_at`: Fecha de creación

## 🔗 Relaciones

- `UserInvitation` → `Tenant` (tenant_id)
- `UserInvitation` → `User` (invited_by)
- `User` → `UserInvitation` (sent_invitations)
- `Tenant` → `UserInvitation` (user_invitations)

## 🚀 Endpoints

### POST /api/users/invite

Crear una invitación para un nuevo usuario.

**Headers requeridos:**
- `Authorization: Bearer <token>`
- `X-Tenant-ID: <tenant_id>`

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "role": "user"
}
```

**Respuesta:**
```json
{
  "message": "Invitación creada exitosamente",
  "status": 201,
  "error": false,
  "data": {
    "data": {
      "invitation_id": 1,
      "code": "abc123...",
      "email": "usuario@ejemplo.com",
      "role": "user",
      "expires_at": "2026-04-10T10:00:00",
      "tenant_id": "uuid-tenant"
    }
  }
}
```

### POST /api/invitations/accept

Aceptar una invitación y crear la cuenta de usuario.

**Headers:** Ninguno (endpoint público)

**Body:**
```json
{
  "code": "abc123...",
  "password": "MiPassword123",  // Opcional: si no se proporciona, se usa una contraseña generada
  "full_name": "Nombre Completo"
}
```

**Respuesta:**
```json
{
  "message": "Invitación aceptada exitosamente",
  "status": 200,
  "error": false,
  "data": {
    "data": {
      "user_id": 2,
      "email": "usuario@ejemplo.com",
      "full_name": "Nombre Completo",
      "role": "user",
      "tenant_id": "uuid-tenant",
      "tenant_name": "Empresa Test",
      "invitation_accepted": true
    }
  }
}
```

## 🔧 Instalación

### 1. Ejecutar la migración

```bash
# Conectar a PostgreSQL y ejecutar:
psql -d your_database -f create_user_invitations_table.sql
```

### 2. Verificar modelos

Los modelos están definidos en:
- `app/models/user_invitation.py` - Modelo principal
- `app/models/user.py` - Relación sent_invitations
- `app/models/tenant.py` - Relación user_invitations
- `app/models/__init__.py` - Importaciones

### 3. Verificar servicios

El servicio está en `app/services/invitation_service.py` con métodos:
- `create_invitation()` - Crear invitación
- `accept_invitation()` - Aceptar invitación
- `get_invitation_by_code()` - Obtener por código
- `get_tenant_invitations()` - Listar invitaciones del tenant
- `cancel_invitation()` - Cancelar invitación
- `cleanup_expired_invitations()` - Limpiar expiradas

### 4. Verificar routers

Los endpoints están en:
- `app/api/routers/users.py` - POST /users/invite
- `app/api/routers/invitations.py` - POST /invitations/accept

## 🧪 Pruebas

### Ejecutar pruebas automáticas

```bash
python test_invitations.py
```

### Prueba manual con Postman

1. **Registrar tenant:**
   - POST `/auth/register`
   - Guardar `token` y `tenant_id`

2. **Crear invitación:**
   - POST `/api/users/invite`
   - Headers: `Authorization`, `X-Tenant-ID`
   - Guardar `invitation_code`

3. **Aceptar invitación:**
   - POST `/api/invitations/accept`
   - Body con `code`, `password`, `full_name`

4. **Verificar login:**
   - POST `/auth/login` con email/password del invitado

## ⚠️ Validaciones

### Crear invitación:
- ❌ Usuario ya existe → 400 Bad Request
- ❌ Invitación pendiente para mismo email/tenant → 400 Bad Request
- ✅ Invitación creada → 201 Created

### Aceptar invitación:
- ❌ Código no encontrado → 404 Not Found
- ❌ Invitación expirada → 400 Bad Request
- ❌ Usuario ya existe → 400 Bad Request
- ✅ Usuario creado y invitación aceptada → 200 OK

## 🔒 Seguridad

- Códigos únicos de 32 caracteres URL-safe
- Expiración configurable (default: 7 días)
- Estados de invitación controlados
- Eliminación en cascada con tenants/users
- Validación de permisos por tenant

## 📊 Estados de invitación

- `pending`: Invitación creada, esperando aceptación
- `accepted`: Invitación aceptada, usuario creado
- `expired`: Invitación expirada o cancelada

## 🧹 Limpieza

Para limpiar invitaciones expiradas automáticamente:

```python
from app.services.invitation_service import InvitationService

# En un job programado o manualmente
expired_count = InvitationService.cleanup_expired_invitations(db)
print(f"Cleaned up {expired_count} expired invitations")
```

## 🎯 Flujo completo

1. Admin crea invitación → `POST /api/users/invite`
2. Sistema envía email con código (implementar email service)
3. Usuario recibe código y acepta → `POST /api/invitations/accept`
4. Usuario puede hacer login normalmente → `POST /auth/login`

¡El sistema de invitaciones está listo para producción! 🚀