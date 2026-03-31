# 🧪 Guía Completa de Testing - Sistema Multi-Tenant

## Requisitos
- ✅ Backend corriendo: http://127.0.0.1:8000
- ✅ PostgreSQL corriendo: postgresql://postgres:1234@localhost:5434/mesa_db
- ✅ Postman instalado
- ✅ DBeaver o psql para verificar BD

---

## PASO 1: Crear Tenant

### 1.1 - En Postman - Crear Tenant

**Endpoint:** `POST http://127.0.0.1:8000/tenants`

**Headers:**
```
Content-Type: application/json
```

**Body (Raw JSON):**
```json
{
  "name": "Quantum Restaurant Group"
}
```

**Response Esperado (201 Created):**
```json
{
  "message": "Tenant created successfully",
  "status": 201,
  "error": false,
  "data": {
    "id": 1,
    "name": "Quantum Restaurant Group",
    "created_at": "2026-03-31T10:30:00",
    "updated_at": "2026-03-31T10:30:00"
  }
}
```

**✓ Guarda:** `tenant_id = 1`

### 1.2 - Verifica en PostgreSQL

**Terminal:**
```powershell
# Abre psql
psql -U postgres -d mesa_db -h localhost -p 5434

# Ejecuta:
SELECT * FROM tenants;
```

**Resultado esperado:**
```
 id |           name           |      created_at      |      updated_at      
----+--------------------------+----------------------+----------------------
  1 | Quantum Restaurant Group | 2026-03-31 10:30:00 | 2026-03-31 10:30:00
(1 row)
```

---

## PASO 2: Registrar Usuario

### 2.1 - En Postman - Register User

**Endpoint:** `POST http://127.0.0.1:8000/auth/register`

**Headers:**
```
Content-Type: application/json
```

**Body (Raw JSON):**
```json
{
  "email": "admin@quantum.com",
  "password": "AdminSecure123!",
  "first_name": "Juan",
  "last_name": "García",
  "full_name": "Juan García",
  "tenant_id": 1,
  "role": "admin"
}
```

**Response Esperado (201 Created):**
```json
{
  "message": "User registered successfully",
  "status": 201,
  "error": false,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600,
    "tenant_id": 1
  }
}
```

**✓ Guarda:** 
- `access_token` (para próximas requests)
- Copia completamente el token

### 2.2 - Verifica JWT Decodificado

💡 Puedes decodificar el JWT en https://jwt.io para ver el payload:

**Payload dentro del token:**
```json
{
  "sub": "admin@quantum.com",
  "tenant_id": 1,
  "role": "admin",
  "exp": 1743513000
}
```

### 2.3 - Verifica en PostgreSQL

```sql
SELECT id, email, full_name, role, tenant_id, is_active 
FROM users 
WHERE email = 'admin@quantum.com';
```

**Resultado esperado:**
```
 id |       email       | full_name | role  | tenant_id | is_active
----+-------------------+-----------+-------+-----------+-----------
  1 | admin@quantum.com | Juan García | admin |     1     |     1
(1 row)
```

---

## PASO 3: Login

### 3.1 - En Postman - Login

**Endpoint:** `POST http://127.0.0.1:8000/auth/login`

**Headers:**
```
Content-Type: application/json
```

**Body (Raw JSON):**
```json
{
  "email": "admin@quantum.com",
  "password": "AdminSecure123!"
}
```

**Response Esperado (200 OK):**
```json
{
  "message": "Login successful",
  "status": 200,
  "error": false,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600,
    "tenant_id": 1
  }
}
```

**✓ Guarda el nuevo `access_token`**

---

## PASO 4: Crear Restaurant (con Autenticación)

### 4.1 - En Postman - Crear Restaurant

**Endpoint:** `POST http://127.0.0.1:8000/restaurants`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {access_token}
```

⚠️ **IMPORTANTE:** Reemplaza `{access_token}` con el token del login anterior

**Body (Raw JSON):**
```json
{
  "name": "Pizza Paradise",
  "description": "Pizzería de fuego lento",
  "address": "Calle Principal 123, Ciudad",
  "phone": "+34-912345678",
  "email": "contact@pizzaparadise.com"
}
```

**Response Esperado (201 Created):**
```json
{
  "message": "Restaurant created successfully",
  "status": 201,
  "error": false,
  "data": {
    "id": 1,
    "name": "Pizza Paradise",
    "description": "Pizzería de fuego lento",
    "address": "Calle Principal 123, Ciudad",
    "phone": "+34-912345678",
    "email": "contact@pizzaparadise.com",
    "tenant_id": 1,
    "created_at": "2026-03-31T10:35:00"
  }
}
```

**✓ Guarda:** `restaurant_id = 1`

### 4.2 - Verifica en PostgreSQL

```sql
SELECT id, name, address, tenant_id 
FROM restaurants 
WHERE tenant_id = 1;
```

**Resultado esperado:**
```
 id |      name        |           address           | tenant_id
----+------------------+-----------------------------+-----------
  1 | Pizza Paradise   | Calle Principal 123, Ciudad |     1
(1 row)
```

---

## PASO 5: Listar Restaurants (Tenant Filtrado)

### 5.1 - En Postman - List Restaurants

**Endpoint:** `GET http://127.0.0.1:8000/restaurants`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Params (opcional):**
```
skip=0
limit=100
```

**Response Esperado (200 OK):**
```json
{
  "message": "Restaurants retrieved successfully",
  "status": 200,
  "error": false,
  "data": {
    "data": [
      {
        "id": 1,
        "name": "Pizza Paradise",
        "description": "Pizzería de fuego lento",
        "address": "Calle Principal 123, Ciudad",
        "phone": "+34-912345678",
        "email": "contact@pizzaparadise.com",
        "tenant_id": 1,
        "created_at": "2026-03-31T10:35:00"
      }
    ]
  }
}
```

✅ **Validación Multi-Tenant:** IF you try with a token from another tenant, it will ONLY show that tenant's restaurants.

---

## PASO 6: VALIDAR MULTI-TENANT (Seguridad)

### 6.1 - Crear SEGUNDO Tenant

**Endpoint:** `POST http://127.0.0.1:8000/tenants`

**Body:**
```json
{
  "name": "Fast Burgers Inc"
}
```

**Guarda:** `tenant_id_2 = 2`

### 6.2 - Registrar Usuario en SEGUNDO Tenant

**Endpoint:** `POST http://127.0.0.1:8000/auth/register`

**Body:**
```json
{
  "email": "owner@fastburgers.com",
  "password": "Secure123!",
  "full_name": "Maria López",
  "tenant_id": 2,
  "role": "admin"
}
```

**Guarda el token de Maria:** `access_token_tenant2`

### 6.3 - Crear Restaurant en SEGUNDO Tenant

**Endpoint:** `POST http://127.0.0.1:8000/restaurants`

**Headers:**
```
Authorization: Bearer {access_token_tenant2}
```

**Body:**
```json
{
  "name": "Burger King Quality",
  "address": "Avenida Central 456"
}
```

### 6.4 - PRUEBA CRÍTICA: Intenta Acceder a Restaurant de Otro Tenant

**Endpoint:** `GET http://127.0.0.1:8000/restaurants/1`

**Headers:**
```
Authorization: Bearer {access_token_tenant2}
```

**Response Esperado (404 Not Found) - ✅ SEGURIDAD VALIDADA:**
```json
{
  "message": "Restaurant not found",
  "status": 404,
  "error": true,
  "data": null
}
```

⚠️ **ESTO ES CORRECTO** - Maria (Tenant 2) NO puede ver restaurant de Juan (Tenant 1)

---

## PASO 7: Verificar en PostgreSQL - Datos Completos

### Conectar a PostgreSQL

```powershell
psql -U postgres -d mesa_db -h localhost -p 5434
```

### Ver todos los Tenants
```sql
SELECT id, name FROM tenants;
```

### Ver todos los Usuarios
```sql
SELECT id, email, full_name, role, tenant_id FROM users;
```

### Ver todos los Restaurants
```sql
SELECT id, name, address, tenant_id FROM restaurants;
```

### Ver Relación Tenant-User-Restaurant
```sql
SELECT 
  t.id as tenant_id,
  t.name as tenant_name,
  u.email as user_email,
  r.name as restaurant_name
FROM tenants t
LEFT JOIN users u ON u.tenant_id = t.id
LEFT JOIN restaurants r ON r.tenant_id = t.id
ORDER BY t.id;
```

**Resultado esperado:**
```
 tenant_id |    tenant_name     |      user_email        | restaurant_name
-----------+--------------------+------------------------+--------------------
    1      | Quantum Rest Group | admin@quantum.com      | Pizza Paradise
    1      | Quantum Rest Group | admin@quantum.com      | NULL (si solo hay 1)
    2      | Fast Burgers Inc   | owner@fastburgers.com  | Burger King Quality
```

---

## 🔍 Checklist de Validación

- [ ] ✅ Tenant 1 creado correctamente
- [ ] ✅ User 1 registrado en Tenant 1
- [ ] ✅ Login funciona y devuelve access_token
- [ ] ✅ JWT incluye `tenant_id` en payload
- [ ] ✅ Restaurant creado en Tenant 1
- [ ] ✅ Listar restaurants muestra solo del Tenant 1
- [ ] ✅ Tenant 2 creado correctamente
- [ ] ✅ User 2 registrado en Tenant 2
- [ ] ✅ Restaurant de Tenant 2 creado
- [ ] ✅ User 2 NO puede acceder a restaurants de Tenant 1 (404)
- [ ] ✅ Datos visibles en PostgreSQL correctamente

---

## 🔧 Troubleshooting

### Error: "Authorization header missing"
**Solución:** Asegúrate de incluir header `Authorization: Bearer {token}`

### Error: "Invalid or expired token"
**Solución:** El token expiró. Haz login de nuevo y copia el nuevo token

### Error: "Could not validate credentials"
**Solución:** Email o credenciales incorrectas

### Restaurant no aparece en lista
**Solución:** Verifica que el `tenant_id` del restaurant coincida con el del user autenticado

### 404 Not Found en GET /restaurants/{id}
**Solución:** Ese restaurant pertenece a otro tenant. ¡Esto es correcto!

---

## 📊 Estructura de Datos Esperada

```
PostgreSQL (mesa_db)
├── tenants (tabla)
│   └── id: 1, 2, ...
│
├── users (tabla)
│   ├── tenant_id: 1 → Tenant 1
│   └── tenant_id: 2 → Tenant 2
│
├── restaurants (tabla)
│   ├── tenant_id: 1 → Tenant 1
│   └── tenant_id: 2 → Tenant 2
│
└── Queries SIEMPRE filtran por tenant_id
```

---

## 🎯 Próximos Pasos

1. **TESTEAR:** Sigue esta guía completamente
2. **VERIFY:** Confirma que todos los checkboxes estén ✅
3. **FRONTEND:** Una vez validado, integrar con Next.js
4. **DEPLOY:** Preparar para producción

