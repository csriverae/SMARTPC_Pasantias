# 🚀 Guía de Ejecución - Mesapass Auth System

## Sistema Completo: Frontend + Backend + Base de Datos

---

## 📋 Checklist Previo

- [ ] PostgreSQL instalado y corriendo
- [ ] Python 3.9+ instalado
- [ ] Node.js 18+ instalado
- [ ] Virtual environment creado

---

## 1️⃣ Setup Base de Datos (PostgreSQL)

### Paso 1: Crear Base de Datos

```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE mesapass;

# Crear usuario (opcional)
CREATE USER mesapass_user WITH PASSWORD 'password123';
ALTER ROLE mesapass_user SET client_encoding TO 'utf8';
ALTER ROLE mesapass_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE mesapass_user SET default_transaction_deferrable TO on;
ALTER ROLE mesapass_user SET default_timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mesapass TO mesapass_user;

# Salir
\q
```

### Paso 2: Configurar Variables de Entorno

Crear archivo `.env` en `starter-kit/starter-kit/`:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/mesapass

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000

# Server
DEBUG=True
```

---

## 2️⃣ Backend (FastAPI + PostgreSQL)

### Terminal 1: Backend API

```bash
# Navegar al proyecto
cd starter-kit/starter-kit

# Activar virtual environment
# En Windows:
.venv\Scripts\activate
# En Mac/Linux:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones (Alembic)
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Esperado:**
```
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
INFO:     Uvicorn reloading...
```

---

## 3️⃣ Frontend (Next.js)

### Terminal 2: Frontend

```bash
# Navegar al proyecto (desde raíz)
cd starter-kit/starter-kit

# Instalar dependencias
pnpm install
# O con npm:
npm install

# Ejecutar en desarrollo
pnpm dev
# O con npm:
npm run dev
```

**Esperado:**
```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
```

---

## 4️⃣ Acceder a la Aplicación

1. Abrir navegador: **http://localhost:3000**
2. Automáticamente redirige a: **http://localhost:3000/login**
3. Ver página de login con opciones "Login" y "Register"

---

## ✨ Funcionalidades Implementadas

### 🔐 Registro

```
1. Click en "Create an account"
2. Rellenar:
   - First Name: ej. "Juan"
   - Last Name: ej. "Pérez"
   - Email: ej. "juan@example.com"
   - Password: ej. "password123" (mínimo 6 caracteres)
   - Role: "employee", "restaurant_admin", "company_admin", o "admin"
3. Click "Register"

✅ Si es exitoso:
   - Muestra: "✓ Usuario creado con éxito"
   - Cambia automáticamente a Login
   - Datos guardados en PostgreSQL

❌ Si falla:
   - Email duplicado: "Este email ya está registrado"
   - Formato inválido: Mensajes específicos
   - Todos los errores se muestran en rojo debajo del campo
```

### 🔓 Login

```
1. Rellenar:
   - Email: ej. "juan@example.com"
   - Password: ej. "password123"
2. Click "Login"

✅ Si es exitoso:
   - Muestra: "✓ Login exitoso"
   - Guarda tokens en localStorage
   - Redirige a /profile

❌ Si falla:
   - "Email o contraseña incorrectos"
   - Error se muestra en rojo
```

### 👤 Profile Page

```
Muestra:
- Avatar con inicial del nombre
- Nombre completo
- Email
- Rol (badge con color)
- Información de la cuenta
- Estado (Active)

En la barra lateral:
- Settings
- Logout
```

---

## 🧪 Pruebas Rápidas

### Test 1: Registro Exitoso
```
Email: test1@example.com
First Name: Carlos
Last Name: García
Password: password123
Role: employee

Resultado esperado: ✅ "Usuario creado con éxito"
```

### Test 2: Email Duplicado
```
Intentar registrar con test1@example.com nuevamente

Resultado esperado: ❌ "Este email ya está registrado"
```

### Test 3: Login
```
Email: test1@example.com
Password: password123

Resultado esperado: ✅ Redirige a /profile
```

### Test 4: Verificar en Base de Datos
```bash
# Terminal 3: Conectarse a PostgreSQL
psql -U postgres -d mesapass

# Ver todos los usuarios
SELECT id, email, full_name, role FROM users;

# Salir
\q
```

**Resultado esperado:**
```
 id |      email       | full_name  |   role
----+------------------+------------+----------
  1 | test1@example.com| Carlos García| employee
(1 row)
```

---

## 📊 Endpoints del API (Postman)

Importar archivo: `../Mesapass_Postman_Collection_StandardResponse.json`

### Endpoints Disponibles:

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registrar nuevo usuario |
| POST | `/auth/login` | Login y obtener tokens |
| POST | `/auth/refresh` | Refrescar access token |
| GET | `/auth/me` | Obtener usuario actual |
| GET | `/auth/users` | Listar todos (admin only) |
| DELETE | `/auth/users/{id}` | Eliminar usuario (admin only) |

---

## 🗂️ Estructura de Datos en localStorage

```javascript
// Tokens
localStorage.getItem('token')           // access_token JWT
localStorage.getItem('refresh_token')   // refresh_token JWT

// Usuario
localStorage.getItem('user')            // user object
// Contiene:
{
  id: 1,
  email: "test@example.com",
  full_name: "Carlos García",
  role: "employee"
}
```

---

## 🔍 Verificar Logs

### Backend (FastAPI)
```
Terminal 1 mostrará:
- Requests recibidos
- Errores de validación
- SQL queries (si DEBUG=True)
```

### Frontend (Next.js)
```
Terminal 2 mostrará:
- Build warnings
- Client-side errors
- Network requests en DevTools (F12)
```

### Base de Datos (PostgreSQL)
```
Ver logs en pgAdmin o terminal de PostgreSQL
```

---

## 🐛 Problemas Comunes

### ❌ Error: "Connection refused" en Backend
```bash
# Verificar que PostgreSQL está corriendo
# Verificar DATABASE_URL en .env
# Reiniciar ambos servicios
```

### ❌ Error: "Module not found" en Frontend
```bash
# Ejecutar en Terminal 2:
pnpm install
# O:
npm install
```

### ❌ Error: "CORS" en Frontend
```bash
# Verificar que el Backend tiene CORS habilitado para localhost:3000
# Ver en: app/main.py -> CORSMiddleware
```

### ❌ Page no redirige a /login
```bash
# Verificar que next.config.mjs tiene el redirect configurado
# Limpiar cache: rm -rf .next
# Reiniciar servidor: pnpm dev
```

---

## 📝 Archivos Importantes

```
starter-kit/starter-kit/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── api/
│   │   └── routes/
│   │       └── user.py         # Auth endpoints
│   ├── crud/
│   │   └── user.py             # Database operations
│   ├── models/
│   │   └── user.py             # User model
│   ├── schemas/
│   │   └── user.py             # Pydantic schemas
│   └── core/
│       ├── security.py         # JWT, bcrypt
│       └── config.py           # Settings
│
├── src/
│   ├── views/
│   │   └── Login.jsx           # Login/Register page
│   ├── @core/
│   │   └── hooks/
│   │       └── useAuthUser.ts  # Auth hook
│   └── components/
│       └── dashboard/          # UI components
│
├── app/
│   ├── login/page.tsx          # /login route
│   ├── profile/page.tsx        # /profile route
│   └── settings/page.tsx       # /settings route
│
├── next.config.mjs             # Redirect config
├── requirements.txt            # Python deps
│
└── TESTING_GUIDE.md           # Este archivo
```

---

## ✅ Checklist Final

- [ ] PostgreSQL corriendo
- [ ] Backend iniciado en localhost:8000
- [ ] Frontend iniciado en localhost:3000
- [ ] /login se muestra al abrir la app
- [ ] Se puede registrar nuevo usuario
- [ ] Email duplicado muestra error
- [ ] Se puede hacer login
- [ ] Se redirige a /profile después del login
- [ ] Usuario se muestra correctamente en /profile
- [ ] Datos están en PostgreSQL
- [ ] Se puede hacer logout
- [ ] Se puede hacer login nuevamente

---

## 🎉 ¡Listo!

Todo el sistema está configurado y funcionando. Prueba el flujo completo:

1. Abrir http://localhost:3000
2. Registrar nuevo usuario
3. Intentar registrar con email duplicado (debe fallar)
4. Hacer login
5. Ver perfil con datos del usuario
6. Logout y repetir

¡Éxito! 🚀
