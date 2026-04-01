# Configuración Postman para Registrar Usuarios

## Base de Datos Configurada ✅
- **Host**: localhost
- **Puerto**: 5434
- **Base de Datos**: mesa_db
- **Usuario**: postgres
- **Contraseña**: 1324

## Pasos para Usar la Colección Postman

### 1️⃣ Importar la Colección
1. Abre Postman
2. Click en `Import` 
3. Selecciona el archivo `Mesapass_Postman_Collection.json` (en la raíz del proyecto)
4. Haz click en `Import`

### 2️⃣ Asegurate que el Backend esté Corriendo
```bash
# En la carpeta starter-kit/starter-kit
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3️⃣ Usar la Colección - Flujo Recomendado

#### **A. Registrar un nuevo usuario**
1. Abre el request **"Register User"**
2. Modifica el body con los datos que desees:
```json
{
  "email": "tuusuario@example.com",
  "password": "TuContraseña123",
  "first_name": "Tu",
  "last_name": "Nombre",
  "full_name": "Tu Nombre Completo",
  "role": "employee"  // pode rser: admin, restaurant_admin, company_admin, employee
}
```
3. Haz click en **Send**
4. ✅ El usuario se registrará en la BD PostgreSQL

#### **B. Iniciar Sesión**
1. Abre el request **"Login User"**
2. Modifica el email y contraseña con los que registraste
3. Haz click en **Send**
4. ✅ Los tokens se guardarán automáticamente en las variables (access_token y refresh_token)

#### **C. Verificar Usuario Actual**
1. Abre el request **"Get Current User"**
2. Haz click en **Send**
3. ✅ Verás los datos del usuario conectado

### 4️⃣ Variables Automáticas
Después de Login, estas variables se guardan automáticamente:
- `{{base_url}}` - localhost:8000
- `{{access_token}}` - Tu token de acceso
- `{{refresh_token}}` - Tu token de refresco

### 5️⃣ Endpoints Disponibles

| Método | Endpoint | Descripción | Requiere Auth |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Registrar nuevo usuario | ❌ No |
| POST | `/auth/login` | Iniciar sesión | ❌ No |
| POST | `/auth/refresh` | Refrescar token | ❌ No |
| GET | `/auth/me` | Obtener usuario actual | ✅ Sí |
| GET | `/auth/users` | Listar todos los usuarios | ✅ Sí (Admin) |
| DELETE | `/auth/users/{id}` | Eliminar usuario | ✅ Sí (Admin) |
| GET | `/health` | Health check | ❌ No |

## 🔍 Verificar en PostgreSQL

Para ver que los datos se guardaron en la BD:

```bash
# Conectarte a la BD
psql -h localhost -p 5434 -U postgres -d mesa_db

# Dentro de psql, verifica los usuarios registrados:
SELECT id, email, full_name, role FROM users;
```

## 📌 Notas Importantes

1. ⚠️ La contraseña debe tener al menos 6 caracteres
2. ⚠️ El email debe ser único
3. ⚠️ Después de registrar, debes hacer Login para obtener tokens
4. ✅ Los tokens se guardan automáticamente en variables de Postman
5. ✅ Los tokens expiran después de 30 minutos (access_token)

## 🆘 Troubleshooting

### Error: "Connection refused" o "Network error"
```
❌ El backend no está corriendo
✅ Asegurate de ejecutar: uvicorn app.main:app --reload --port 8000
```

### Error: "Email already registered"
```
❌ El email ya existe en la base de datos
✅ Usa un email diferente o elimina el usuario de la BD
```

### Error: "Incorrect email or password"
```
❌ Las credenciales son incorrectas
✅ Verifica que escribiste correctamente el email y contraseña
```

### Error: "Invalid token" en otros endpoints
```
❌ El token expiró o no es válido
✅ Haz login nuevamente para obtener un nuevo token
```
