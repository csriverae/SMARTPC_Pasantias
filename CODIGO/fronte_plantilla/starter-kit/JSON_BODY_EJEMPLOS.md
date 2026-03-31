# 📝 Ejemplos de JSON - Request Body para Cada Endpoint

---

## 🔐 AUTH ENDPOINTS

### **POST /auth/register** - Registrar Usuario
**Descripción**: Crea un usuario nuevo y le asigna automáticamente un tenant_id

```json
{
  "email": "seco@gordo.com",
  "password": "MiPassword123!"
}
```

**Parámetros**:
- `email` (string, requerido): Email único del usuario
- `password` (string, requerido): Mínimo 8 caracteres

**Response Success (201)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "seco@gordo.com",
  "role": "admin",
  "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
  "created_at": "2026-03-31T12:00:00"
}
```

---

### **POST /auth/login** - Iniciar Sesión
**Descripción**: Obtiene token JWT con tenant_id incluido

```json
{
  "email": "seco@gordo.com",
  "password": "MiPassword123!"
}
```

**Response Success (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzZWNvQGdvcmRvLmNvbSIsInJvbGUiOiJhZG1pbiIsInRlbmFudF9pZCI6IjY2MGU4NDAwLWUyOWItNDFkNC1hNzE2LTQ0NjY1NTQ0MDAwMSIsImV4cCI6MTcwNDAxNjAwMH0.xxx",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxx"
}
```

**Token Payload (decodificado)**:
```json
{
  "sub": "seco@gordo.com",
  "role": "admin",
  "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
  "exp": 1704016000
}
```

---

### **POST /auth/refresh-token** - Renovar Token
**Descripción**: Obtiene nuevo token usando el refresh_token

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxx"
}
```

**Response Success (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 🏢 TENANTS ENDPOINTS (Admin Only)

### **POST /tenants/** - Crear Tenant
**Descripción**: Crea un nuevo tenant (Solo admin)

```json
{
  "name": "Acme Corporation"
}
```

**Parámetros**:
- `name` (string, requerido): Nombre único del tenant

**Headers REQUERIDOS**:
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Response Success (201)**:
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "name": "Acme Corporation",
  "created_at": "2026-03-31T12:00:00",
  "updated_at": "2026-03-31T12:00:00"
}
```

---

### **GET /tenants/** - Listar Tenants
**Descripción**: Lista todos los tenants (Admin only)

**URL con Query Parameters**:
```
http://127.0.0.1:8000/tenants/?skip=0&limit=10
```

**Parámetros Query**:
- `skip` (int, default: 0): Número de resultados a saltar
- `limit` (int, default: 10): Número máximo de resultados

**Headers REQUERIDOS**:
```
Authorization: Bearer {{token}}
```

**Response Success (200)**:
```json
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "name": "Acme Corporation",
    "created_at": "2026-03-31T12:00:00",
    "updated_at": "2026-03-31T12:00:00"
  },
  {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "name": "TechStart Inc",
    "created_at": "2026-03-31T13:00:00",
    "updated_at": "2026-03-31T13:00:00"
  }
]
```

---

### **GET /tenants/{id}** - Obtener Tenant por ID
**Descripción**: Obtiene detalles de un tenant específico

**URL**:
```
GET http://127.0.0.1:8000/tenants/770e8400-e29b-41d4-a716-446655440002
```

**Headers REQUERIDOS**:
```
Authorization: Bearer {{token}}
```

**Response Success (200)**:
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "name": "Acme Corporation",
  "created_at": "2026-03-31T12:00:00",
  "updated_at": "2026-03-31T12:00:00"
}
```

---

### **PATCH /tenants/{id}** - Actualizar Tenant
**Descripción**: Actualiza detalles del tenant (Solo admin)

**URL**:
```
PATCH http://127.0.0.1:8000/tenants/770e8400-e29b-41d4-a716-446655440002
```

**Body**:
```json
{
  "name": "Acme Corporation - Updated"
}
```

**Headers REQUERIDOS**:
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Response Success (200)**:
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "name": "Acme Corporation - Updated",
  "created_at": "2026-03-31T12:00:00",
  "updated_at": "2026-03-31T14:30:00"
}
```

---

### **DELETE /tenants/{id}** - Eliminar Tenant
**Descripción**: Elimina un tenant (Solo admin)

**URL**:
```
DELETE http://127.0.0.1:8000/tenants/770e8400-e29b-41d4-a716-446655440002
```

**Headers REQUERIDOS**:
```
Authorization: Bearer {{token}}
```

**Response Success (204)**:
```
(Sin body - Solo status 204 No Content)
```

---

## 🍽️ RESTAURANTS ENDPOINTS

### **POST /restaurants/** - Crear Restaurante
**Descripción**: Crea un nuevo restaurante en el tenant actual

```json
{
  "name": "La Pizzería del Gordo",
  "description": "Pizzas auténticas italianas hechas al horno de leña",
  "address": "Calle Alcalá 123, 28009 Madrid",
  "phone": "+34 912 345 678",
  "email": "pizza@gordo.com"
}
```

**Parámetros**:
- `name` (string, requerido): Nombre del restaurante
- `description` (string, opcional): Descripción
- `address` (string, opcional): Dirección
- `phone` (string, opcional): Teléfono
- `email` (string, opcional): Email de contacto

**Headers REQUERIDOS**:
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Response Success (201)**:
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "name": "La Pizzería del Gordo",
  "description": "Pizzas auténticas italianas hechas al horno de leña",
  "address": "Calle Alcalá 123, 28009 Madrid",
  "phone": "+34 912 345 678",
  "email": "pizza@gordo.com",
  "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "active",
  "created_at": "2026-03-31T12:00:00",
  "updated_at": "2026-03-31T12:00:00"
}
```

---

### **GET /restaurants/** - Listar Restaurantes
**Descripción**: Lista restaurantes del tenant actual (filtrado automáticamente por JWT)

**URL con Query Parameters**:
```
GET http://127.0.0.1:8000/restaurants/?skip=0&limit=10
```

**Parámetros Query**:
- `skip` (int, default: 0): Número de resultados a saltar
- `limit` (int, default: 10): Número máximo de resultados

**Headers REQUERIDOS**:
```
Authorization: Bearer {{token}}
```

**Response Success (200)**:
```json
[
  {
    "id": "990e8400-e29b-41d4-a716-446655440004",
    "name": "La Pizzería del Gordo",
    "description": "Pizzas auténticas...",
    "address": "Calle Alcalá 123, 28009 Madrid",
    "phone": "+34 912 345 678",
    "email": "pizza@gordo.com",
    "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
    "status": "active",
    "created_at": "2026-03-31T12:00:00",
    "updated_at": "2026-03-31T12:00:00"
  },
  {
    "id": "aa0e8400-e29b-41d4-a716-446655440005",
    "name": "El Seco Gourmet",
    "description": "Cocina fusion contemporánea",
    "address": "Plaza Mayor 456, 28012 Madrid",
    "phone": "+34 913 456 789",
    "email": "gourmet@seco.com",
    "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
    "status": "active",
    "created_at": "2026-03-31T13:00:00",
    "updated_at": "2026-03-31T13:00:00"
  }
]
```

---

### **GET /restaurants/{id}** - Obtener Restaurante por ID
**Descripción**: Obtiene detalles de un restaurante específico

**URL**:
```
GET http://127.0.0.1:8000/restaurants/990e8400-e29b-41d4-a716-446655440004
```

**Headers REQUERIDOS**:
```
Authorization: Bearer {{token}}
```

**Response Success (200)**:
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "name": "La Pizzería del Gordo",
  "description": "Pizzas auténticas italianas hechas al horno de leña",
  "address": "Calle Alcalá 123, 28009 Madrid",
  "phone": "+34 912 345 678",
  "email": "pizza@gordo.com",
  "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "active",
  "created_at": "2026-03-31T12:00:00",
  "updated_at": "2026-03-31T12:00:00"
}
```

---

### **PATCH /restaurants/{id}** - Actualizar Restaurante
**Descripción**: Actualiza detalles del restaurante

**URL**:
```
PATCH http://127.0.0.1:8000/restaurants/990e8400-e29b-41d4-a716-446655440004
```

**Body** (actualiza solo los campos que necesites):
```json
{
  "name": "La Pizzería del Gordo - Premium",
  "description": "Pizzas auténticas italianas + Pasta gourmet",
  "phone": "+34 912 999 999",
  "email": "premium@gordo.com"
}
```

**Headers REQUERIDOS**:
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Response Success (200)**:
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "name": "La Pizzería del Gordo - Premium",
  "description": "Pizzas auténticas italianas + Pasta gourmet",
  "address": "Calle Alcalá 123, 28009 Madrid",
  "phone": "+34 912 999 999",
  "email": "premium@gordo.com",
  "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "active",
  "created_at": "2026-03-31T12:00:00",
  "updated_at": "2026-03-31T15:45:00"
}
```

---

### **DELETE /restaurants/{id}** - Eliminar Restaurante
**Descripción**: Elimina un restaurante

**URL**:
```
DELETE http://127.0.0.1:8000/restaurants/990e8400-e29b-41d4-a716-446655440004
```

**Headers REQUERIDOS**:
```
Authorization: Bearer {{token}}
```

**Response Success (204)**:
```
(Sin body - Solo status 204 No Content)
```

---

## 🚨 ERROR RESPONSES

### **Error 400 - Bad Request**
```json
{
  "message": "Validation error",
  "status": 400,
  "error": true,
  "data": {
    "details": "Email must be valid"
  }
}
```

### **Error 401 - Unauthorized**
```json
{
  "message": "Could not validate credentials",
  "status": 401,
  "error": true,
  "data": {
    "details": "Invalid token or token expired"
  }
}
```

### **Error 403 - Forbidden**
```json
{
  "message": "Access denied",
  "status": 403,
  "error": true,
  "data": {
    "details": "You need admin role for this operation"
  }
}
```

### **Error 404 - Not Found**
```json
{
  "message": "Resource not found",
  "status": 404,
  "error": true,
  "data": {
    "details": "Tenant with ID xxx not found"
  }
}
```

### **Error 409 - Conflict**
```json
{
  "message": "Resource already exists",
  "status": 409,
  "error": true,
  "data": {
    "details": "Email already registered"
  }
}
```

---

## ✅ CHECKLIST: Validación de JSON

- ✅ Todo JSON está entre `{` `}` o `[` `]`
- ✅ Todos los strings entre comillas dobles: `"key": "value"`
- ✅ No hay comas después del último item
- ✅ Comillas escapadas en strings si es necesario: `"email\\"domain.com"`
- ✅ Headers siempre incluyen `Authorization: Bearer {{token}}`
- ✅ Content-Type es `application/json` para POST/PATCH

---

¡Listos los JSONs! Cópialos directamente en Postman. 🎉
