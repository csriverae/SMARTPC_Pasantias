# 📨 Guía Completa: Setup Postman MesaPass

## ✅ PASO 1: Importar Archivos en Postman

### 1.1 Importar Colección
- Abre **Postman** (Desktop App)
- Click en **Import** (arriba izquierda)
- Arrastra o selecciona: `MesaPass_Complete.postman_collection.json`
- Verás 4 carpetas: Auth, Tenants, Restaurants, Quick Test

### 1.2 Importar Environment
- Click en **Environments** (arriba derecha)
- Click en **Import**
- Selecciona: `MesaPass_Environment.postman_environment.json`
- Selecciona el environment de la lista desplegable (arriba derecha)

---

## 🔑 PASO 2: Configurar Variables

Haz click en el icono de **ojos** → **Edit** para ver/modificar:

| Variable | Valor Defecto | Qué es |
|----------|---------------|--------|
| `base_url` | http://127.0.0.1:8000 | URL del backend |
| `email` | admin@mesapass.com | Email para login |
| `email_nueva` | user@mesapass.com | Para registrar nuevos usuarios |
| `password` | Password123! | Contraseña |
| `tenant_name` | Mi Primer Tenant | Nombre del tenant a crear |
| `restaurant_name` | El Restaurante del Gordo | Nombre del restaurante |
| `restaurant_*` | Precompletados | Otros datos del restaurante |

---

## 🚀 PASO 3: FLUJO CORRECTO (Por Orden)

### **Fase 1: Autenticación**

#### 1️⃣ **1.2 - Login**
```
POST http://127.0.0.1:8000/auth/login

Body:
{
  "email": "{{email}}",
  "password": "{{password}}"
}

Response (si todo bien):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "refresh_token": "..."
}
```

✅ **Automáticamente**: El test script guarda el `token` en variable

---

### **Fase 2: Crear Tenant (Solo Admin)**

#### 2️⃣ **2.2 - Crear Tenant**
```
POST http://127.0.0.1:8000/tenants/

Headers:
- Authorization: Bearer {{token}}
- Content-Type: application/json

Body:
{
  "name": "{{tenant_name}}"
}

Response:
{
  "id": "uuid-aqui",
  "name": "Mi Primer Tenant",
  "created_at": "2026-03-31T..."
}
```

✅ **Automáticamente**: Guarda el `tenant_id` en variable

---

### **Fase 3: Crear Restaurante**

#### 3️⃣ **3.2 - Crear Restaurante**
```
POST http://127.0.0.1:8000/restaurants/

Headers:
- Authorization: Bearer {{token}}
- Content-Type: application/json

Body:
{
  "name": "El Restaurante del Gordo",
  "description": "Comida deliciosa y ambiente acogedor",
  "address": "Calle El Gordo 123, Madrid",
  "phone": "+34 912 345 678",
  "email": "gordo@mesapass.com"
}

Response:
{
  "id": "uuid-aqui",
  "name": "El Restaurante del Gordo",
  "description": "Comida deliciosa...",
  "address": "Calle El Gordo 123, Madrid",
  "phone": "+34 912 345 678",
  "email": "gordo@mesapass.com",
  "tenant_id": "{{tenant_id}}",
  "status": "active"
}
```

✅ **Automáticamente**: Guarda el `restaurant_id` en variable

---

### **Fase 4: Listar**

#### 4️⃣ **2.1 - Listar Tenants**
```
GET http://127.0.0.1:8000/tenants/?skip=0&limit=10

Headers:
- Authorization: Bearer {{token}}

Response:
[
  {
    "id": "uuid",
    "name": "Mi Primer Tenant",
    "created_at": "2026-03-31T..."
  }
]
```

#### 5️⃣ **3.1 - Listar Restaurantes**
```
GET http://127.0.0.1:8000/restaurants/?skip=0&limit=10

Headers:
- Authorization: Bearer {{token}}

Response:
[
  {
    "id": "uuid",
    "name": "El Restaurante del Gordo",
    "description": "...",
    "address": "...",
    "phone": "...",
    "email": "...",
    "tenant_id": "{{tenant_id}}",
    "status": "active"
  }
]
```

---

## 🧪 OPCIÓN RÁPIDA: Quick Test (Todo en 5 requests)

Usa la carpeta **🧪 QUICK TEST** que ejecuta:
1. Registrar Admin
2. Login
3. Crear Tenant
4. Crear Restaurante
5. Listar Restaurantes

Solo ejecuta uno por uno en orden ⬇️

---

## ⚠️ ERRORES COMUNES Y SOLUCIONES

### Error: `401 Could not validate credentials`
**Problema**: No tiene token o token expirado  
**Solución**: 
1. Ejecuta **1.2 - Login** primero
2. Verifica que `{{token}}` esté guardado (icono de ojos)

### Error: `404 Not Found` en Tenants
**Problema**: No es admin o tenant_id incorrecto  
**Solución**:
1. Verifica que estés logueado como admin
2. Usa el `tenant_id` correcto de otro request

### Error: `403 Forbidden` en Restaurantes
**Problema**: Intentas acceder a restaurante de otro tenant  
**Solución**:
- El backend filtra automáticamente (solo ves tus restaurantes)
- Intenta crear uno primero con **3.2**

---

## 📋 CHECKLIST: Qué Hacer Ahora

- [ ] Importar `MesaPass_Complete.postman_collection.json`
- [ ] Importar `MesaPass_Environment.postman_environment.json`
- [ ] Activar el environment en Postman
- [ ] Ejecutar **1.2 - Login** (debe guardar token)
- [ ] Ejecutar **2.2 - Crear Tenant** (debe guardar tenant_id)
- [ ] Ejecutar **3.2 - Crear Restaurante** (debe guardar restaurant_id)
- [ ] Ejecutar **3.1 - Listar Restaurantes** (debe mostrar lo que creaste)
- [ ] ✅ ¡Sistema completo funcionando!

---

## 🔄 Workflow Típico

```
LOGIN → GUARDAR TOKEN
   ↓
CREAR TENANT → GUARDAR TENANT_ID
   ↓
CREAR RESTAURANTE → GUARDAR RESTAURANT_ID
   ↓
LISTAR RESTAURANTES
   ↓
ACTUALIZAR RESTAURANTE
   ↓
ELIMINAR RESTAURANTE (opcional)
```

---

## 💡 Pro Tips

### Usar Postman Collections Runner
1. Click en **🔄 Run** (en la colección)
2. Selecciona los requests en orden
3. Click **Run MesaPass Collection**
4. Ejecuta todo automáticamente

### Variables en Tiempo Real
Después de cada request, las variables se actualizan automáticamente si el test script está bien. Verifica con el icono de **ojos**.

### Copiar Response Completo
Click derecho en respuesta → **Copy as JSON** para usar datos en otra request

---

## 📞 ¿Qué hacer si algo falla?

1. Verifica que el backend está corriendo: `http://127.0.0.1:8000/`
2. Revisa la respuesta exacta en Postman
3. Mira la variable `{{token}}` tiene contenido
4. Intenta refrescar el environment (F5 en Postman)

¡Listo! 🎉
