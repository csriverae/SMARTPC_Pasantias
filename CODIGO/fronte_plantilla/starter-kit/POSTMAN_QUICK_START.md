# 🎯 INSTRUCCIONES RÁPIDAS - IMPORTAR Y USAR

## 📥 QUÉ IMPORTAR EN POSTMAN

Encontrarás 2 archivos en: `starter-kit/`

```
✅ MesaPass_Complete.postman_collection.json    ← COLECCIÓN (todos los endpoints)
✅ MesaPass_Environment.postman_environment.json ← ENVIRONMENT (variables)
```

---

## 🚀 EN 3 PASOS: Start

### **PASO 1: Importar Colección**
```
Postman → Import → Arrastra "MesaPass_Complete.postman_collection.json"
```
Verás 4 carpetas:
- 1️⃣ AUTH (3 requests)
- 2️⃣ TENANTS (5 requests)
- 3️⃣ RESTAURANTS (5 requests)
- 🧪 QUICK TEST (5 requests - el flujo completo)

---

### **PASO 2: Importar Environment**
```
Postman → Environments → Import → "MesaPass_Environment.postman_environment.json"
```

Luego ACTIVA el environment en el dropdown de arriba a la derecha donde dice **"No environment"**

---

### **PASO 3: EJECUTA EN ESTE ORDEN**

**📋 Secuencia Correcta:**

1. **1.2 - Login** → Obtiene token
2. **2.2 - Crear Tenant** → Obtiene tenant_id
3. **3.2 - Crear Restaurante** → Obtiene restaurant_id
4. **3.1 - Listar Restaurantes** → Ve lo que creaste ✅

---

## 🔥 OPCIÓN RÁPIDA: Todo en 5 clicks

Usa la carpeta **🧪 QUICK TEST**:
1. Click en **TEST 1 - Registrar Admin**
2. Click en **TEST 2 - Login Admin**
3. Click en **TEST 3 - Crear Tenant**
4. Click en **TEST 4 - Crear Restaurante**
5. Click en **TEST 5 - Listar Restaurantes**

Ejecuta cada uno ⬇️ Listo. El flujo completo funciona.

---

## 📝 VARIABLES PRE-GUARDADAS

El environment tiene TODO precargado:

```
email           = admin@mesapass.com
password        = Password123!
tenant_name     = Mi Primer Tenant
restaurant_name = El Restaurante del Gordo
restaurant_*    = Todos los otros datos del restaurante
```

Para registrar un NUEVO usuario: Cambia `{{email}}` a otra en variables

---

## 🔑 CÓMO COPIA EL JSON

En cada carpeta/request hay un **Body** con el JSON ya listo.

Ejemplo - **3.2 - Crear Restaurante**:
```json
{
  "name": "{{restaurant_name}}",
  "description": "{{restaurant_description}}",
  "address": "{{restaurant_address}}",
  "phone": "{{restaurant_phone}}",
  "email": "{{restaurant_email}}"
}
```

Las variables `{{}}` se reemplazan automáticamente.

---

## 📚 DOCUMENTACIÓN COMPLETA

3 archivos con toda la info:

| Archivo | Para qué |
|---------|----------|
| **POSTMAN_SETUP_GUIA.md** | Setup paso a paso + solucionar errores |
| **JSON_BODY_EJEMPLOS.md** | Ejemplos JSON con responses exactas |
| **Este archivo** | Quick start |

---

## ⚠️ ANTES DE EMPEZAR

✅ Backend corriendo en http://127.0.0.1:8000
```powershell
cd .\starter-kit\starter-kit\
python -m uvicorn app.main:app --reload
```

✅ Postman importa los 2 archivos
✅ Environment activo

---

## ✅ LISTO PARA TESTEAR

Ahora:
1. Abre Postman
2. Importa los 2 archivos
3. Ejecuta **QUICK TEST** uno por uno
4. ¡Ves todos los datos en la respuesta!

🎉 **Sistema multi-tenant completamente testeable**

---

## 🆘 Si Falla Algo

**❌ Error 401 - Unauthorized**
→ Ejecuta primero "1.2 - Login"

**❌ Error 404 - Not Found**
→ Verifica que tenant_id existe (copia del response de crear tenant)

**❌ El token no se guarda**
→ Mira en el tab "Tests" de Postman → El script copia al environment

**❌ Backend no responde**
→ Verifica http://127.0.0.1:8000 está corriendo

---

¿Listo? ¡Adelante! 🚀

