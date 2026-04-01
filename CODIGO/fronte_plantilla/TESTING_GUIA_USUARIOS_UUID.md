# Testing Guía - Sistema de Usuarios UUID Multi-Tenant

## Base URL
```
http://localhost:8000
```

## 1. Registro de Usuario (Register)

### Request
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "admin@smartpc.com",
  "password": "Admin@123456",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
  "role": "admin"
}
```

### Response (201 Created)
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600,
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### Notas
- `role` es requerido: "admin" o "employee"
- `tenant_id` es requerido (UUID)
- Email debe ser único
- Solo 1 admin por tenant

---

## 2. Login

### Request
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "admin@smartpc.com",
  "password": "Admin@123456"
}
```

### Response (200 OK)
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600,
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### Token Claims (decodificar para ver)
```json
{
  "sub": "admin@smartpc.com",
  "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
  "role": "admin",
  "exp": 1698765432
}
```

---

## 3. Obtener Perfil Actual (Get Current User)

### Request
```bash
GET /auth/me
Authorization: Bearer {access_token}
```

### Response (200 OK)
```json
{
  "success": true,
  "message": "User profile retrieved",
  "data": {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "email": "admin@smartpc.com",
    "is_active": true
  }
}
```

---

## 4. Listar Usuarios del Tenant (Admin Only)

### Request
```bash
GET /auth/users?skip=0&limit=100
Authorization: Bearer {admin_access_token}
```

### Response (200 OK)
```json
{
  "success": true,
  "message": "Retrieved 5 users",
  "data": [
    {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "email": "admin@smartpc.com",
      "is_active": true
    },
    {
      "id": "a47ac10b-58cc-4372-a567-0e02b2c3d480",
      "email": "employee@smartpc.com",
      "is_active": true
    }
  ]
}
```

### Notas
- Solo usuarios del MISMO tenant aparecen
- Solo admin puede acceder (validado desde token)
- Parámetros: skip (default 0), limit (default 100)

---

## 5. Obtener Usuario Específico (Admin Only)

### Request
```bash
GET /auth/users/f47ac10b-58cc-4372-a567-0e02b2c3d479
Authorization: Bearer {admin_access_token}
```

### Response (200 OK)
```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "email": "employee@smartpc.com",
    "is_active": true
  }
}
```

### Errores Posibles
```json
// Usuario no existe en este tenant
{
  "success": false,
  "status_code": 404,
  "message": "User not found"
}

// Invalid UUID format
{
  "success": false,
  "status_code": 404,
  "message": "Invalid user ID format"
}

// No permissions
{
  "success": false,
  "status_code": 403,
  "message": "Only admin users can access this resource"
}
```

---

## 6. Actualizar Usuario (Admin Only)

### Request
```bash
PATCH /auth/users/f47ac10b-58cc-4372-a567-0e02b2c3d479
Authorization: Bearer {admin_access_token}
Content-Type: application/json

{
  "is_active": false
}
```

### Response (200 OK)
```json
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "email": "employee@smartpc.com",
    "is_active": false
  }
}
```

### Cambios Soportados
- `is_active` (boolean)
- `role` (admin/employee) - actualiza en UserTenant

---

## 7. Cambiar Contraseña (Cualquier Usuario)

### Request
```bash
POST /auth/change-password
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "current_password": "Admin@123456",
  "new_password": "NewPass@789456",
  "confirm_password": "NewPass@789456"
}
```

### Response (200 OK)
```json
{
  "success": true,
  "message": "Password changed successfully",
  "data": {
    "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
  }
}
```

### Validaciones
- Contraseña actual debe ser correcta
- Nuevas contraseñas deben coincidir
- Mínimo 6 caracteres

---

## 8. Actualizar Perfil Actual (Cualquier Usuario)

### Request
```bash
PATCH /auth/me
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "is_active": true
}
```

### Response (200 OK)
```json
{
  "success": true,
  "message": "User profile updated successfully",
  "data": {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "email": "admin@smartpc.com",
    "is_active": true
  }
}
```

---

## 9. Eliminar Usuario (Admin Only)

### Request
```bash
DELETE /auth/users/f47ac10b-58cc-4372-a567-0e02b2c3d479
Authorization: Bearer {admin_access_token}
```

### Response (200 OK)
```json
{
  "success": true,
  "message": "User deleted successfully",
  "data": {
    "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
  }
}
```

### Notas
- Elimina usuario Y todo en UserTenant (cascade)
- Solo admin del mismo tenant puede eliminar

---

## 10. Eliminar Propia Cuenta (Cualquier Usuario)

### Request
```bash
DELETE /auth/me
Authorization: Bearer {access_token}
```

### Response (200 OK)
```json
{
  "success": true,
  "message": "User account deleted successfully",
  "data": {
    "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
  }
}
```

---

## 11. Refrescar Token (Cualquier Usuario)

### Request
```bash
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Response (200 OK)
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600,
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

---

## Casos de Testing Multi-Tenant

### Caso 1: Mismo Usuario, Múltiples Tenants
```
1. Registrar admin en Tenant A
   POST /register { tenant_id: A, role: admin }
   
2. Registrar MISMO EMAIL en Tenant B
   → Email already exists ✅ (emails únicos globales)
   
3. Registrar diferente email, Tenant B
   POST /register { email: user@b.com, tenant_id: B, role: admin }
   
4. MISMO usuario (@a.com) añadido a Tenant B por admin
   POST /register { email: admin@a.com, tenant_id: B, role: employee }
   → Ahora el usuario está en 2 tenants

5. Login con @a.com
   - Token tendrá tenant_id = A (primer tenant)
   - Pero usuario también existe en B
```

### Caso 2: Aislamiento de Datos
```
1. Admin A login → tenant_id = A, role = admin
   GET /users → Solo usuarios de Tenant A ✅
   
2. Admin A intenta ver usuario de Tenant B
   GET /users/user_b_id
   → 404 Not Found ✅ (no existe en su tenant)
   
3. Admin A intenta actualizar usuario de Tenant B
   PATCH /users/user_b_id
   → 404 Not Found ✅ (protección de sandbox)
```

### Caso 3: Error Multi-Admin
```
1. Admin A (Tenant A) login
   POST /register { tenant_id: A, email: admin2@a.com, role: admin }
   → Error: "Only one admin allowed per tenant" ✅
```

---

## Variables de Entorno Esperadas

```env
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/mesa_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Server
API_PORT=8000
```

---

## UUID de Tenants de Prueba

Usar estos UUID para testing (ya existen en BD):

```
Tenant 1 (Default Company):
550e8400-e29b-41d4-a716-446655440000

Tenant 2 (KFC):
550e8400-e29b-41d4-a716-446655440001
```

---

## Postman Collection

Importar `MesaPass_Complete.postman_collection.json` que contiene:
- ✅ Todas las rutas de auth
- ✅ Variables pre-configuradas ({{TOKEN}}, {{USER_ID}}, {{TENANT_ID}})
- ✅ Tests automáticos para validar respuestas

---

## Checklist de Testing

- [ ] Register: crear usuario con tenant_id UUID
- [ ] Register: rechazar email duplicado
- [ ] Register: rechazar 2 admins en mismo tenant
- [ ] Login: retorna token con tenant_id + role
- [ ] Get /me: sin auth retorna 401
- [ ] Get /users: admin puede listar usuarios de su tenant
- [ ] Get /users: employee retorna 403
- [ ] Get /users: solo usuarios del tenant aparecen
- [ ] GET /users/{id}: aislamiento de datos
- [ ] PATCH /users/{id}: validar pertenencia a tenant
- [ ] DELETE /users/{id}: aislamiento de datos
- [ ] Refresh token: genera nuevo access_token
- [ ] Multi-tenant: usuario en 2 tenants
