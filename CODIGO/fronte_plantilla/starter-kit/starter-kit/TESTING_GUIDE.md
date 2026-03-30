# Testing Guide - Mesapass Auth System

## 📋 Overview

Este documento proporciona instrucciones para probar el sistema de autenticación con validaciones implementadas.

---

## 🔧 Requisitos Previos

- ✅ API FastAPI ejecutándose en `http://localhost:8000`
- ✅ PostgreSQL corriendo y base de datos inicializada
- ✅ Frontend Next.js en `http://localhost:3000`
- ✅ Postman instalado

---

## 🧪 Test Cases

### 1. **Register - Validaciones de Email**

#### Test 1.1: Email válido, nuevo usuario
```json
POST http://localhost:8000/auth/register
Content-Type: application/json

{
  "email": "user1@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "employee"
}
```

**Respuesta Esperada:**
```json
{
  "message": "User registered successfully",
  "status": 201,
  "error": false,
  "data": {
    "id": 1,
    "email": "user1@example.com",
    "full_name": "John Doe",
    "role": "employee"
  }
}
```

---

#### Test 1.2: Email duplicado ❌
```json
POST http://localhost:8000/auth/register
Content-Type: application/json

{
  "email": "user1@example.com",
  "password": "password123",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "employee"
}
```

**Respuesta Esperada (Error):**
```json
{
  "detail": "Email already registered"
}
```

**En Frontend:** Se muestra mensaje: ⚠️ "Este email ya está registrado"

---

#### Test 1.3: Email inválido ❌
```json
POST http://localhost:8000/auth/register
Content-Type: application/json

{
  "email": "invalidemail",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "employee"
}
```

**En Frontend:** Se valida localmente: ⚠️ "Please enter a valid email"

---

#### Test 1.4: Contraseña muy corta ❌
```json
POST http://localhost:8000/auth/register
Content-Type: application/json

{
  "email": "user2@example.com",
  "password": "123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "employee"
}
```

**En Frontend:** Se valida localmente: ⚠️ "Password must be at least 6 characters"

---

#### Test 1.5: Campo requerido faltante ❌
```json
POST http://localhost:8000/auth/register
Content-Type: application/json

{
  "email": "user3@example.com",
  "password": "password123",
  "first_name": "John",
  "role": "employee"
}
```

**En Frontend:** Se valida localmente: ⚠️ "Last name is required"

---

### 2. **Login - Validaciones**

#### Test 2.1: Login exitoso ✅
```json
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "user1@example.com",
  "password": "password123"
}
```

**Respuesta Esperada:**
```json
{
  "message": "Login successful",
  "status": 200,
  "error": false,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

**En Frontend:** 
- ✅ Guarda `access_token` y `refresh_token` en localStorage
- ✅ Redirige a `/profile`
- ✅ Muestra mensaje: "✓ Login exitoso"

---

#### Test 2.2: Contraseña incorrecta ❌
```json
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "user1@example.com",
  "password": "wrongpassword"
}
```

**Respuesta Esperada (Error):**
```json
{
  "detail": "Incorrect email or password"
}
```

**En Frontend:** Se muestra: ⚠️ "Email o contraseña incorrectos"

---

#### Test 2.3: Email no existe ❌
```json
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "nonexistent@example.com",
  "password": "password123"
}
```

**Respuesta Esperada (Error):**
```json
{
  "detail": "Incorrect email or password"
}
```

**En Frontend:** Se muestra: ⚠️ "Email o contraseña incorrectos"

---

#### Test 2.4: Email faltante ❌
```json
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "password": "password123"
}
```

**En Frontend:** Se valida localmente: ⚠️ "Email is required"

---

### 3. **Get Current User**

#### Test 3.1: Con token válido ✅
```json
GET http://localhost:8000/auth/me
Authorization: Bearer {{access_token}}
```

**Respuesta Esperada:**
```json
{
  "message": "Current user retrieved",
  "status": 200,
  "error": false,
  "data": {
    "id": 1,
    "email": "user1@example.com",
    "full_name": "John Doe",
    "role": "employee"
  }
}
```

---

#### Test 3.2: Sin token ❌
```json
GET http://localhost:8000/auth/me
```

**Respuesta Esperada (Error):**
```json
{
  "detail": "Not authenticated"
}
```

---

### 4. **Refresh Token**

#### Test 4.1: Refresh con token válido ✅
```json
POST http://localhost:8000/auth/refresh
Content-Type: application/json

{
  "refresh_token": "{{refresh_token}}"
}
```

**Respuesta Esperada:**
```json
{
  "message": "Token refreshed",
  "status": 200,
  "error": false,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

---

## 📊 Validaciones Implementadas

### Frontend (Login.jsx)
- ✅ Email requerido y válido
- ✅ Contraseña requerida (mínimo 6 caracteres en registro)
- ✅ Nombre requerido
- ✅ Apellido requerido
- ✅ Rol requerido
- ✅ Mensajes de error específicos por campo
- ✅ Spinner de carga durante peticiones

### Backend (app/api/routes/user.py)
- ✅ Email único (no duplicados)
- ✅ Validación de contraseña en login
- ✅ Respuestas unificadas con formato StandardResponse
- ✅ Mensajes de error específicos

### Base de Datos (PostgreSQL)
- ✅ Constraint UNIQUE en email
- ✅ Contraseña con hash bcrypt
- ✅ Full_name almacenado correctamente
- ✅ Role asignado correctamente

---

## 🔄 Flujo Completo

```
1. Usuario accede a http://localhost:3000
   ↓
2. Redirige a /login (no a /home)
   ↓
3. Usuario elige Registrarse o Iniciar Sesión
   ↓
4. Validaciones locales en frontend
   ↓
5. Petición POST al backend
   ↓
6. Validaciones en backend (especialmente email único)
   ↓
7. Si es registro exitoso → Muestra mensaje y cambia a login
   ↓
8. Si es login exitoso:
   - Guarda tokens en localStorage
   - Obtiene datos del usuario (/auth/me)
   - Guarda usuario en localStorage
   - Redirige a /profile
   ↓
9. En /profile:
   - useAuthUser hook obtiene usuario del localStorage
   - Muestra nombre, email, rol, avatar
```

---

## 🔑 Variables de Postman (Configurar después de login)

```json
{
  "access_token": "{{pegue aquí el access_token del login}}",
  "refresh_token": "{{pegue aquí el refresh_token del login}}",
  "user_id": "1"
}
```

---

## 📝 Notas Importantes

1. **Email Duplicado:** El sistema rechaza automáticamente registros con email ya existente
2. **Contraseñas:** Se hashean con bcrypt (no se almacenan en texto plano)
3. **Tokens:** Expiran después del tiempo configurado (default 30 min para access, 7 días para refresh)
4. **localStorage:** Los datos están disponibles en la consola del navegador
5. **Persistencia:** All data persists in PostgreSQL

---

## 🐛 Troubleshooting

### Error: "Email already registered"
- ✅ Solución: Usar un email diferente

### Error: "Incorrect email or password"
- ✅ Verificar que el usuario estén registrado primero
- ✅ Verificar la ortografía del email y contraseña

### Profile page no carga
- ✅ Verificar que el `access_token` esté en localStorage
- ✅ Hacer logout y login nuevamente

### Base de datos vacía
- ✅ Ejecutar: `python setup_db.py`
- ✅ O usar alembic: `alembic upgrade head`

---

## ✅ Checklist de Prueba

- [ ] Registrar usuario nuevo (email válido)
- [ ] Intentar registrar con email duplicado (debe fallar)
- [ ] Registrar con email inválido (debe fallar en frontend)
- [ ] Registrar con contraseña corta (debe fallar en frontend)
- [ ] Registrar sin nombre (debe fallar en frontend)
- [ ] Login con credenciales correctas
- [ ] Login con contraseña incorrecta (debe fallar)
- [ ] Login con email no existente (debe fallar)
- [ ] Verificar que los datos estén en PostgreSQL (SELECT * FROM users)
- [ ] Verificar que el usuario se redirige a /profile después del login
- [ ] Verificar que el perfil muestra la información correcta del usuario
- [ ] Refresh token funciona correctamente
- [ ] Logout y login nuevamente (reutiliza email anterior)
