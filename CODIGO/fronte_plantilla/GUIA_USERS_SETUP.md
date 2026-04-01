# 🚀 MesaPass - Sistema Completamente Configurado

## 📊 Datos de los Tenants Creados

```
Tenant 1 (Compañía):
  ID: 96261def-bc6b-422a-9592-edaaa1874662
  Nombre: Default Company
  Tipo: company

Tenant 2 (Restaurante):
  ID: cc74d75c-db7e-41c4-a0f4-c674c2a83843
  Nombre: KFC
  Tipo: restaurant
```

## 💾 Base de Datos
- **Base de datos**: `mesa_db`
- **Servidor**: `localhost:5434`
- **Usuario**: `postgres`
- **Contraseña**: `1234`

## 📋 Tablas Creadas
✅ tenants
✅ users
✅ user_tenants (relación usuario-tenant con roles)
✅ companies
✅ restaurants
✅ agreements
✅ employees
✅ meal_logs
✅ invitation_codes

---

## 🔑 Consultas SQL Útiles

### 1. Ver todos los tenants
```sql
SELECT id, name, type, created_at FROM tenants;
```

### 2. Ver todos los usuarios
```sql
SELECT id, email, first_name, last_name, full_name, is_active FROM users;
```

### 3. Ver relación usuario-tenant con roles
```sql
SELECT ut.id, u.email, t.name, ut.role, ut.created_at 
FROM user_tenants ut
JOIN users u ON ut.user_id = u.id
JOIN tenants t ON ut.tenant_id = t.id;
```

### 4. Ver administradores de un tenant
```sql
SELECT u.email, u.full_name, ut.role 
FROM user_tenants ut
JOIN users u ON ut.user_id = u.id
WHERE ut.tenant_id = '96261def-bc6b-422a-9592-edaaa1874662' AND ut.role = 'admin';
```

### 5. Ver empleados de una compañía
```sql
SELECT u.email, u.full_name, e.cedula, t.name as company
FROM employees e
JOIN users u ON e.user_id = u.id
JOIN tenants t ON e.company_tenant_id = t.id;
```

### 6. Ver restaurantes de un tenant
```sql
SELECT id, name, address, phone FROM restaurants 
WHERE tenant_id = 'cc74d75c-db7e-41c4-a0f4-c674c2a83843';
```

### 7. Contar usuarios por tenant
```sql
SELECT t.name, COUNT(ut.user_id) as user_count
FROM tenants t
LEFT JOIN user_tenants ut ON t.id = ut.tenant_id
GROUP BY t.id, t.name;
```

### 8. Listar acuerdos (empresa-restaurante)
```sql
SELECT a.id, tc.name as company, tr.name as restaurant, a.subsidy_type
FROM agreements a
JOIN tenants tc ON a.company_tenant_id = tc.id
JOIN tenants tr ON a.restaurant_tenant_id = tr.id;
```

### 9. Ver registros de comidas
```sql
SELECT ml.id, u.full_name, r.name as restaurant, ml.consumed_at
FROM meal_logs ml
JOIN employees e ON ml.employee_id = e.id
JOIN users u ON e.user_id = u.id
JOIN restaurants r ON ml.restaurant_tenant_id = r.id
ORDER BY ml.consumed_at DESC;
```

### 10. Ver códigos de invitación activos
```sql
SELECT id, code, role, is_used, created_at FROM invitation_codes 
WHERE is_used = FALSE;
```

---

## 📮 Postman Collection

Archivo: `MesaPass_Usuarios.postman_collection.json`

### Requests Disponibles:

#### Autenticación
1. **Registrar Admin**
   - POST: `/auth/register`
   - Body: Email, contraseña, nombre, apellido, rol="admin", tenant_id

2. **Registrar Employee**
   - POST: `/auth/register`
   - Body: Email, contraseña, nombre, apellido, rol="employee", tenant_id

3. **Login Admin**
   - POST: `/auth/login`
   - Body: Email, contraseña

4. **Login Employee**
   - POST: `/auth/login`
   - Body: Email, contraseña

#### Gestión de Usuarios
5. **Listar Todos los Usuarios (Admin)**
   - GET: `/auth/users`
   - Headers: Authorization Bearer Token

6. **Obtener Perfil Actual**
   - GET: `/auth/me`
   - Headers: Authorization Bearer Token

7. **Actualizar Usuario**
   - PATCH: `/auth/users/{USER_ID}`
   - Headers: Authorization Bearer Token
   - Body: first_name, last_name, role

8. **Cambiar Contraseña**
   - POST: `/auth/change-password`
   - Headers: Authorization Bearer Token
   - Body: current_password, new_password, confirm_password

9. **Eliminar Usuario**
   - DELETE: `/auth/users/{USER_ID}`
   - Headers: Authorization Bearer Token

---

## 🔐 IDs de Tenants para Usar

**Para crear usuarios en la compañía:**
```
tenant_id: 96261def-bc6b-422a-9592-edaaa1874662
```

**Para crear restaurantes:**
```
tenant_id: cc74d75c-db7e-41c4-a0f4-c674c2a83843
```

---

## 🚀 Pasos para Probar

1. **Abre Postman**
2. **Importa**: `MesaPass_Usuarios.postman_collection.json`
3. **Registra un Admin**:
   - Usa el endpoint "1️⃣ Registrar Admin"
   - Cambia email si es necesario
4. **Registra un Employee**:
   - Usa el endpoint "2️⃣ Registrar Employee"
5. **Haz Login**:
   - Usa "3️⃣ Login Admin" o "4️⃣ Login Employee"
   - Copia el token del response
6. **Gestiona Usuarios**:
   - Usa los endpoints de gestión con el token

---

## ✅ Todo Completado

- ✅ PostgreSQL con todas las tablas creadas
- ✅ Schema UUID y multi-tenancy
- ✅ Tenants por defecto insertados
- ✅ Postman Collection lista
- ✅ Consultas SQL disponibles
- ✅ Endpoints de usuarios funcionando
