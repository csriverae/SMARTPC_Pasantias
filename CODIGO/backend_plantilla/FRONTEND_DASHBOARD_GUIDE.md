# Frontend Dashboard - Guía de Uso

## 🚀 Resumen

El dashboard del frontend ahora está completamente integrado con el backend. Puedes gestionar empresas, restaurantes, acuerdos, empleados, validar QR, registrar consumos y ver reportes.

## 📋 Flujo Principal de Uso

### 1️⃣ **Autenticación** (Ya existe)
- Ve a `/login`
- Ingresa credenciales:
  - Email: `admin@example.com`
  - Contraseña: `admin123`
- Se guardan automáticamente: `token` y `tenant_id` en localStorage

### 2️⃣ **Crear Empresas**
**Ruta:** `/companies`

**Acciones:**
- Click en "Nueva Empresa"
- Ingresa:
  - Nombre: Ej. "Restaurant ABC"
  - RUC: Ej. "12345678901"
- Click en "Crear Empresa"

**Resultado:** La empresa se crea y aparece en la lista

### 3️⃣ **Crear Restaurantes**
**Ruta:** `/restaurants`

**Acciones:**
- Click en "Nuevo Restaurante"
- Ingresa:
  - Nombre del Restaurante: Ej. "Mi Restaurante Favorito"
- Click en "Crear Restaurante"

**Resultado:** El restaurante se crea y aparece en la lista

### 4️⃣ **Crear Acuerdos**
**Ruta:** `/agreements`

**Acciones:**
- Click en "Nuevo Acuerdo"
- Selecciona:
  - Empresa (creada en paso 2)
  - Restaurante (creado en paso 3)
  - Fecha de inicio
  - Fecha de fin
- Click en "Crear Acuerdo"

**Resultado:** El acuerdo se crea y aparece en la tabla

### 5️⃣ **Crear Empleados**
**Ruta:** `/employees`

**Acciones:**
- Click en "Nuevo Empleado"
- Ingresa:
  - Nombre: Ej. "Juan Pérez"
  - Email: Ej. "juan@example.com"
  - Empresa: Selecciona la empresa creada
- Click en "Crear Empleado"

**Resultado:** El empleado se crea con un **Token QR único**
- El token aparece en una tarjeta debajo del empleado
- Puedes hacer click en "Copiar" para copiar el token

### 6️⃣ **Validar QR**
**Ruta:** `/qr-validator`

**Acciones:**
- Ingresa o pega el Token QR del empleado
- Click en "Validar QR" o presiona Enter
- Verás los datos del empleado validado:
  - Nombre
  - Email
  - ID del Empleado
  - Token QR
  - ID de la Empresa

**Resultado:** Se muestra "✅ QR Válido" con información del empleado

### 7️⃣ **Registrar Consumos**
**Ruta:** `/meal-logs`

**Acciones:**
- Click en "Nuevo Consumo"
- Selecciona/ingresa:
  - Empleado (validado anteriormente)
  - Acuerdo (creado en paso 4)
  - Tipo de Comida: desayuno/almuerzo/merienda/cena
  - Fecha de Consumo
  - Cantidad
- Click en "Registrar Consumo"

**Resultado:** El consumo se registra y aparece en la tabla

### 8️⃣ **Ver Reportes**
**Ruta:** `/reportes`

**Acciones:**
- Click en "Reporte de Consumo" o "Reporte de Facturación"
- Se genera y muestra automáticamente en una tabla
- Datos mostrados:
  - Empleado
  - Total de Consumos/Monto

## 🧭 Navegación

El menú lateral muestra todos los apartados:

```
📊 Dashboard          → /home
🏢 Empresas          → /companies
🍽️ Restaurantes      → /restaurants
📋 Acuerdos          → /agreements
👥 Empleados         → /employees
📱 Validar QR        → /qr-validator
🥘 Consumos          → /meal-logs
📊 Reportes          → /reports
👤 Profile           → /profile
⚙️ Settings          → /settings
🚪 Exit Dashboard    → /
```

## 💡 Características del Dashboard

### ✅ Validación de Formularios
- Todos los campos requeridos están marcados
- Mensajes de error claros cuando falla algo

### ✅ Carga de Datos
- Las listas se cargan automáticamente
- Los selectos se rellenan con datos de la BD

### ✅ Copiar Token QR
- Botón "Copiar" para copiar el token del empleado
- Cambio visual para confirmar la copia

### ✅ Tablas de Datos
- Visualización clara de información
- Hover effects para mejor UX

### ✅ Integración con Headers
- El token JWT se envía automáticamente
- El X-Tenant-ID se envía con cada request

## 🔄 Flujo Completo Paso a Paso

```
1. Login (auth)
   ↓
2. Crear Empresa
   ↓
3. Crear Restaurante
   ↓
4. Crear Acuerdo (vincula empresa + restaurante)
   ↓
5. Crear Empleado (genera token QR)
   ↓
6. Validar QR (verifica el empleado)
   ↓
7. Registrar Consumo (guarda consumo del empleado)
   ↓
8. Ver Reportes (analiza datos de consumo)
```

## 🐛 Solución de Problemas

### ❌ "Error loading companies..."
- Verifica que el backend esté corriendo
- Comprueba que el token sea válido
- Revisa la consola para más detalles

### ❌ "User does not belong to tenant"
- Haz login nuevamente
- Los tokens JWT expiran después de 30 minutos

### ❌ "Foreign key violation"
- Asegúrate de seguir el orden:
  1. Empresa
  2. Restaurante
  3. Acuerdo
  4. Empleado
  5. Consumo

### ❌ Token QR no válido
- Revisa que el token sea exacto
- Copia desde la tarjeta del empleado
- Asegúrate de usar el token del empleado correcto

## 📱 Dispositivos

El dashboard es **responsive** y funciona en:
- ✅ Desktop (1920px+)
- ✅ Tablet (768px - 1024px)
- ✅ Mobile (< 768px)

## 🎨 Estilos

- **Colores principales:** Indigo (menú), Verde (crear), Rojo (eliminar)
- **Tema:** Light mode con bordes sutiles
- **Fuente:** Sistema de fuentes del navegador

## 📞 Endpoints utilizados

| Método | Endpoint | Página |
|--------|----------|--------|
| GET/POST | /api/companies | Companies |
| GET/POST | /api/restaurants | Restaurants |
| GET/POST | /api/agreements | Agreements |
| GET/POST | /api/employees | Employees |
| POST | /api/validate-qr | QR Validator |
| GET/POST | /api/meal-logs | Meal Logs |
| GET | /api/reports/consumption | Reports |
| GET | /api/reports/billing | Reports |

## 🚀 Desarrollo Futuro

Mejoras posibles:
- [ ] Editar/Eliminar entidades
- [ ] Búsqueda y filtros avanzados
- [ ] Exportar reportes a PDF/Excel
- [ ] Gráficos de consumo
- [ ] Historial de cambios
- [ ] Autenticación con roles
- [ ] Dark mode
