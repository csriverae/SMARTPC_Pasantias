# ✅ Configuración Completada - Registro de Usuarios en Postman

## 🎯 Cambios Realizados

### 1. **Configuración de Base de Datos** ✅
- **Archivo actualizado**: `.env`
- Contraseña: `1324` ✓
- Host: `localhost` ✓
- Puerto: `5434` ✓
- Base de datos: `mesa_db` ✓

### 2. **Recreación de Tablas** ✅
- Ejecutado: `rebuild_db.py`
- ✅ Tabla `users` creada con columnas:
  - `id` (PRIMARY KEY)
  - `email` (UNIQUE)
  - `password`
  - `full_name`
  - `role` (admin, restaurant_admin, company_admin, employee)

### 3. **Actualización de Endpoints** ✅
- **Formato de Respuesta Nuevo**:
  ```json
  {
    "message": "Descripción del resultado",
    "status": 200,
    "error": false,
    "data": {
      "data": [
        {
          "id": 1,
          "email": "user@example.com",
          "full_name": "User Name",
          "role": "employee"
        }
      ]
    }
  }
  ```

### 4. **Endpoints Actualizados**
1. **POST `/auth/register`** - Registrar usuario
   - Status: 201 (éxito)
   - Status: 400 (email ya registrado)

2. **POST `/auth/login`** - Iniciar sesión
   - Captura tokens automáticamente en Postman
   - Status: 200 (éxito)
   - Status: 401 (credenciales incorrectas)

3. **GET `/auth/me`** - Obtener usuario actual
   - Requiere token

4. **POST `/auth/refresh`** - Refrescar token
   - Genera nuevo access token

5. **GET `/auth/users`** - Listar usuarios (Admin)
   - Requiere admin role

6. **DELETE `/auth/users/{id}`** - Eliminar usuario (Admin)

7. **POST `/auth/change-password`** - Cambiar contraseña

### 5. **Colección Postman Mejorada** ✅
- Scripts de test que capturan tokens automáticamente
- Validación de respuestas
- Variables globales: `{{base_url}}`, `{{access_token}}`, `{{refresh_token}}`

---

## 🚀 Flujo de Uso - Postman

### Paso 1: Importar Colección
1. Abre Postman
2. Click en `File` → `Import`
3. Selecciona: `Mesapass_Postman_Collection.json`
4. Click en `Import`

### Paso 2: Registrar Usuario

**Request**: `Register User`

```json
{
  "email": "miusuario@example.com",
  "password": "MiContraseña123",
  "first_name": "Mi",
  "last_name": "Nombre",
  "full_name": "Mi Nombre Completo",
  "role": "employee"
}
```

**Response exitosa (201)**:
```json
{
  "message": "Usuario registrado exitosamente",
  "status": 201,
  "error": false,
  "data": {
    "data": [
      {
        "id": 1,
        "email": "miusuario@example.com",
        "full_name": "Mi Nombre Completo",
        "role": "employee"
      }
    ]
  }
}
```

### Paso 3: Iniciar Sesión

**Request**: `Login User`

```json
{
  "email": "miusuario@example.com",
  "password": "MiContraseña123"
}
```

**Response exitosa (200)**:
```json
{
  "message": "Inicio de sesión exitoso",
  "status": 200,
  "error": false,
  "data": {
    "data": [
      {
        "access_token": "eyJhbGc...",
        "refresh_token": "eyJhbGc...",
        "token_type": "bearer"
      }
    ]
  }
}
```

✅ **Los tokens se guardan automáticamente en las variables de Postman**

### Paso 4: Verificar Usuario

**Request**: `Get Current User`
- Los tokens se usan automáticamente del header `Authorization: Bearer {{access_token}}`

---

## 🔍 Verificar en PostgreSQL

```bash
# Conectarse a la BD
psql -h localhost -p 5434 -U postgres -d mesa_db

# Ver usuarios registrados
SELECT id, email, full_name, role FROM users;
```

---

## 📝 Mensajes de Error Mejorados

### Email ya registrado
```json
{
  "message": "El email ya está registrado",
  "status": 400,
  "error": true,
  "data": {"data": []}
}
```

### Credenciales incorrectas
```json
{
  "message": "El email o la contraseña no coinciden con nuestros registros",
  "status": 401,
  "error": true,
  "data": {"data": []}
}
```

### Error en la base de datos
```json
{
  "message": "Error al registrar el usuario",
  "status": 500,
  "error": true,
  "data": {
    "data": [],
    "error": "Descripción detallada del error"
  }
}
```

---

## ✨ Características Implementadas

✅ Registro de usuarios con validación  
✅ Login con tokens JWT (access + refresh)  
✅ Captura automática de tokens en Postman  
✅ Respuestas en formato estándar (message, status, error, data)  
✅ Base de datos PostgreSQL sincronizada  
✅ Scripts de test en cada petición  
✅ Endpoints protegidos con roles  
✅ Cambio de contraseña seguro  

---

## 🆘 Troubleshooting

### Error: "Connection refused"
```
❌ PostgreSQL no está corriendo en puerto 5434
✅ Inicia PostgreSQL o verifica la conexión
```

### Error: "ModuleNotFoundError: No module named 'app'"
```
❌ No estás en el directorio correcto
✅ Ejecuta desde: starter-kit/starter-kit
```

### El servidor se detiene
```
❌ Acceso a puerto 8000 denegado
✅ Usa otro puerto o libera el 8000
```

---

## 📌 Archivo de Configuración

`.env`:
```
DB_USER=postgres
DB_PASSWORD=1324
DB_HOST=localhost
DB_PORT=5434
DB_NAME=mesa_db
```

---

**¡Todo está listo para usar! 🎉**
