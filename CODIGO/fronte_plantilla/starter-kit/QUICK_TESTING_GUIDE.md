# 🧪 TESTING RÁPIDO - Multi-Tenant Testing Summary

## ✅ Estado Actual

- ✅ Backend corriendo: `http://127.0.0.1:8000`
- ✅ PostgreSQL corriendo: `localhost:5434/mesa_db`
- ✅ Relaciones de modelos corregidas
- ✅ Documentación y herramientas de testing creadas

---

## 🎯 3 FORMAS DE TESTEAR

### 1️⃣ OPCIÓN A: Postman (Recomendado - Visual)

**Importa esta colección:**
- Archivo: `MesaPass_Testing_Hub.postman_collection.json`
- En Postman: `File → Import → Select JSON file`

**Luego sigue esta secuencia:**
1. Create Tenant 1 ← Guarda `tenant_id = 1`
2. Create Tenant 2 ← Guarda `tenant_id = 2`
3. Register User 1 ← Guarda token
4. Register User 2 ← Guarda token
5. Create Restaurant 1 (User 1)
6. Create Restaurant 2 (User 2)
7. List Restaurants (User 1) → Ver solo los de Tenant 1 ✅
8. List Restaurants (User 2) → Ver solo los de Tenant 2 ✅
9. Get Restaurant 1 (User 1) → 200 OK ✅
10. Get Restaurant 1 (User 2) → 404 Not Found ✅✅✅ **MULTI-TENANT VALIDATED**

---

### 2️⃣ OPCIÓN B: Script Python (Verifica BD)

**En terminal:**
```powershell
cd .\starter-kit\
python verify_database.py
```

**Output:**
```
✅ Conectado a PostgreSQL exitosamente

========================================================
📋 TENANTS
========================================================
ID   Name                                Users  Restaurants
1    Quantum Restaurant Group            1      1
2    Fast Burgers Inc                    1      1

✅ Total de tenants: 2

👥 USUARIOS
ID   Email                          Name                Role        Tenant Active
1    admin@quantum.com              Juan García        admin       1      1
2    owner@fastburgers.com          Maria López        admin       2      1

🍽️ RESTAURANTES
ID   Name                           Address                     Tenant Active
1    Pizza Paradise                 Calle Principal 123         1      1
2    Burger King Quality            Avenida Central 456         2      1

📊 ESTADÍSTICAS POR TENANT
Tenant ID  Tenant Name                    Users    Restaurants
1          Quantum Restaurant Group       1        1
2          Fast Burgers Inc               1        1

✅ VERIFICACIÓN COMPLETADA
```

---

### 3️⃣ OPCIÓN C: SQL Directo (Control Total)

**Conectar a PostgreSQL:**
```powershell
psql -U postgres -d mesa_db -h localhost -p 5434
```

**Ver datos:**
```sql
-- Ver todos los tenants
SELECT id, name, created_at 
FROM tenants 
ORDER BY id;

-- Ver todos los usuarios
SELECT id, email, role, tenant_id 
FROM users 
ORDER BY id;

-- Ver todos los restaurants
SELECT id, name, tenant_id 
FROM restaurants 
ORDER BY id;

-- Ver relaciones completas
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

---

## 📊 Estructura de Datos Esperada (Después de Testing)

```
TENANTS:
┌────┬───────────────────────────┬────────────────┐
│ id │        name               │  created_at    │
├────┼───────────────────────────┼────────────────┤
│ 1  │ Quantum Restaurant Group  │ TIMESTAMP      │
│ 2  │ Fast Burgers Inc          │ TIMESTAMP      │
└────┴───────────────────────────┴────────────────┘

USERS:
┌────┬──────────────────────┬────────────────┬──────┬─────────┐
│ id │       email          │   full_name    │ role │tenant_id│
├────┼──────────────────────┼────────────────┼──────┼─────────┤
│ 1  │ admin@quantum.com    │ Juan García    │admin │   1     │
│ 2  │ owner@fastburgers.com│ Maria López    │admin │   2     │
└────┴──────────────────────┴────────────────┴──────┴─────────┘

RESTAURANTS:
┌────┬──────────────────────┬─────────────────────────┬─────────┐
│ id │        name          │       address           │tenant_id│
├────┼──────────────────────┼─────────────────────────┼─────────┤
│ 1  │ Pizza Paradise       │ Calle Principal 123     │   1     │
│ 2  │ Burger King Quality  │ Avenida Central 456     │   2     │
└────┴──────────────────────┴─────────────────────────┴─────────┘
```

---

## 🔒 Validación Multi-Tenant CRÍTICA

**El test más importante:**

```
User 1 (Tenant 1) intenta acceder a Restaurant de Tenant 2:
GET /restaurants/1 with User2Token

❌ Respuesta esperada (404):
{
  "message": "Restaurant not found",
  "status": 404,
  "error": true,
  "data": null
}
```

✅ Si obtienes 404, significa: **¡LA SEGURIDAD MULTI-TENANT FUNCIONA!**

---

## 🎬 VIDEOGUÍA - Paso a Paso en Postman

### Paso 1: Import Collection
```
1. Abre Postman
2. File → Import
3. Selecciona MesaPass_Testing_Hub.postman_collection.json
4. Click Import
```

### Paso 2: Ejecutar Tenants
```
1. Click: "Create Tenant 1"
2. Send
3. Copy response: id = 1
4. Click: "Create Tenant 2"
5. Send
6. Copy response: id = 2
```

### Paso 3: Registrar Usuarios
```
1. Click: "Register User 1 (Tenant 1)"
2. Send
3. Verifica que se guardó el token automáticamente (test script)
4. Click: "Register User 2 (Tenant 2)"
5. Send
6. Verifica que se guardó el token automáticamente
```

### Paso 4: Crear Restaurants
```
1. Click: "Create Restaurant in Tenant 1 (User 1)"
2. Send
3. Copy response: id = 1
4. Click: "Create Restaurant in Tenant 2 (User 2)"
5. Send
6. Copy response: id = 2
```

### Paso 5: Validar Multi-Tenant
```
1. Click: "List Restaurants (User 1 - sees only Tenant 1)"
2. Send → Debe mostrar solo Pizza Paradise
3. Click: "List Restaurants (User 2 - sees only Tenant 2)"
4. Send → Debe mostrar solo Burger King Quality
5. Click: "Get Restaurant 1 (User 2 - ❌ 404 Not Found)"
6. Send → Debe devolver 404 ✅
```

---

## 🚀 Próximo: Frontend Integration

Una vez confirmado que todo funciona:

1. **Crear página de Tenants** en Next.js
   - Form para crear nuevo tenant
   - Lista de tenants

2. **Integrar con Login**
   - Mostrar selección de tenant si usuario pertenece a múltiples
   - Guardar `tenant_id` en JWT

3. **Dashboard Filtrado por Tenant**
   - Sidebar mostrará solo restaurants del tenant actual
   - Listar, crear, editar, eliminar restaurants

4. **Protección de Rutas**
   - Verificar tenant_id en localStorage
   - Redirigir si token no pertenece al tenant

---

## ❓ FAQ - Troubleshooting

**P: "Authorization header missing" en restaurant creation**
A: Asegúrate de copiar el token completo en el header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**P: "Could not validate credentials" en login**
A: Verifica que el email y password sean exactos:
- Email: `admin@quantum.com`
- Password: `AdminSecure123!`

**P: Restaurant no aparece en la lista**
A: Verifica que:
1. Usaste el token correcto (del usuario que creó el restaurant)
2. El restaurant pertenece al mismo tenant_id que el usuario

**P: Obtengo 404 al intentar acceder a un restaurant**
A: ¡Esto es correcto! Significa que el restaurant pertenece a otro tenant. Validación multi-tenant funcionando ✅

---

## 📋 Checklist Final

Después de completar todos los tests:

- [ ] Tenants creados (1 y 2)
- [ ] Usuarios registrados (1 en Tenant 1, 1 en Tenant 2)
- [ ] Tokens funcionando (se actualizan automáticamente)
- [ ] Restaurants creados (1 en Tenant 1, 1 en Tenant 2)
- [ ] User 1 ve solo restaurants de Tenant 1
- [ ] User 2 ve solo restaurants de Tenant 2
- [ ] User 2 obtiene 404 al acceder a restaurants de Tenant 1
- [ ] Datos verificados en PostgreSQL
- [ ] Sistema multi-tenant validado ✅

**Después de esto:** LISTO PARA FRONTEND

---

## 📞 Errores Comunes & Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| 500 Internal Server | Modelos relacionados mal | ✅ Ya está corregido |
| 401 Unauthorized | Token inválido/expirado | Login de nuevo |
| 404 Not Found | Recurso pertenece a otro tenant | Es seguridad, es correcto ✅ |
| 400 Bad Request | Email existe/datos inválidos | Verifica bodydel request |
| CORS error | Frontend-Backend URL | Verificar CORS en main.py |

---

## 🎓 Lo que Validaremos

✅ **Aislamiento por Tenant:** Cada usuario solo ve datos de su tenant
✅ **Autenticación JWT:** Tokens incluyen tenant_id 
✅ **Queries Filtradas:** Base de datos filtra por tenant_id
✅ **Seguridad:** No se puede acceder a datos de otro tenant
✅ **Datos Persistentes:** PostgreSQL guarda correctamente

---

**¡LISTO PARA EMPEZAR? 🚀 Sigue el paso 1 en Postman!**
