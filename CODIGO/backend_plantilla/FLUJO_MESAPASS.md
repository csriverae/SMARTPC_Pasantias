# FLUJO_MESAPASS

## 📋 Descripción General del Proyecto

MesaPass es una plataforma SaaS para gestión de servicios de alimentación empresarial. Implementa arquitectura multi-tenant con autenticación JWT, sistema de QR para validación de comidas, y gestión completa de empleados, restaurantes y convenios comerciales.

### 🏗️ Arquitectura Técnica
- **Backend**: FastAPI (Python) + PostgreSQL + SQLAlchemy
- **Frontend**: Next.js 14 + TypeScript
- **Autenticación**: JWT con refresh tokens
- **Multi-tenancy**: Isolación por tenant con headers `X-Tenant-ID`
- **Seguridad**: bcrypt para passwords, validaciones RUC ecuatoriano

---

## 🔄 Flujo de Funcionamiento del Sistema

### 1. **Registro Inicial**
- Usuario registra empresa → Se crea tenant automáticamente
- Usuario admin creado como propietario del tenant
- Token JWT generado para autenticación

### 2. **Configuración del Tenant**
- Crear empresas adicionales (validación RUC 13 dígitos)
- Invitar usuarios al tenant (auto-genera passwords)
- Crear empleados (solo company_admin)
- Configurar restaurantes
- Establecer convenios (Prepago/Postpago/Mixto)

### 3. **Operación Diaria**
- Empleado escanea QR → Validación token
- Registro automático de consumo
- Control de presupuestos y límites
- Reportes en tiempo real

### 4. **Reportes y Facturación**
- Consumo por empleado
- Facturación por empresa/restaurante
- Analytics de tendencias

---

## 🧪 Flujo de Pruebas en Postman

### 📋 Preparación Inicial

1. **Importar Colección**
   - Archivo: `Proyecto_MESAPASS_COMPLETE.json`
   - Variables de entorno configuradas automáticamente

2. **Configurar Variables**
   ```
   base_url: http://localhost:8000
   token: (se setea automáticamente)
   tenant_id: (se setea automáticamente)
   ```

3. **Ejecutar Servidor**
   ```bash
   cd starter-kit/starter-kit
   python run_server.py
   ```

### 🔐 Flujo de Autenticación (Ejecutar en Orden)

#### 1️⃣ **Registro Inicial**
- **Request**: `1️⃣ Registrar - Crear Empresa y Admin`
- **Resultado**: Crea tenant + usuario admin + token JWT
- **Variables**: `token`, `tenant_id`, `user_id` se setean automáticamente

#### 2️⃣ **Login**
- **Request**: `2️⃣ Login - Por Email y Contraseña`
- **Credenciales**: `admin@mesapass.com` / `Admin123`
- **Resultado**: Nuevo token JWT

#### 3️⃣ **Verificar Usuario**
- **Request**: `3️⃣ Obtener Usuario Actual`
- **Headers**: `Authorization: Bearer {{token}}`
- **Resultado**: Datos del usuario autenticado

### 👥 Gestión de Usuarios

#### 4️⃣ **Invitar Usuario**
- **Request**: `Invitar Usuario (Auto-genera Contraseña)`
- **Headers**: `Authorization: Bearer {{token}}`, `X-Tenant-ID: {{tenant_id}}`
- **Body**: Email del nuevo usuario
- **Resultado**: Código de invitación generado

#### 5️⃣ **Aceptar Invitación**
- **Request**: `Aceptar Invitación`
- **Body**: `invitation_code` + nueva password
- **Resultado**: Usuario registrado en el tenant

### 🏢 Gestión de Empresas

#### 6️⃣ **Crear Empresa**
- **Request**: `Crear Empresa (RUC válido - 13 dígitos)`
- **Headers**: `Authorization: Bearer {{token}}`, `X-Tenant-ID: {{tenant_id}}`
- **Validación**: RUC debe tener exactamente 13 dígitos
- **Resultado**: Empresa creada, `company_id` se setea

### 👨‍💼 Gestión de Empleados

#### 7️⃣ **Crear Empleado**
- **Request**: `Crear Empleado (Solo Company Admin)`
- **Headers**: `Authorization: Bearer {{token}}`, `X-Tenant-ID: {{tenant_id}}`
- **Permisos**: Solo usuarios con rol `company_admin`
- **Resultado**: Empleado creado con `qr_token` único

### 🍽️ Gestión de Restaurantes

#### 8️⃣ **Crear Restaurante**
- **Request**: `Crear Restaurante`
- **Headers**: `Authorization: Bearer {{token}}`, `X-Tenant-ID: {{tenant_id}}`
- **Resultado**: Restaurante creado, `restaurant_id` se setea

### 📋 Configuración de Convenios

#### 9️⃣ **Crear Convenio**
- **Request**: Uno de los 3 tipos:
  - `Crear Convenio - PREPAGO (con descuento)`
  - `Crear Convenio - POSTPAGO (normal o descuento)`
  - `Crear Convenio - PAGO MIXTO (% empresa/empleado)`
- **Headers**: `Authorization: Bearer {{token}}`, `X-Tenant-ID: {{tenant_id}}`
- **Campos**: `company_id`, `restaurant_id`, fechas, tipo de pago
- **Resultado**: Convenio establecido, `agreement_id` se setea

### 📱 Sistema QR

#### 🔟 **Generar/Obtener QR**
- **Request**: `Obtener QR del Empleado` o `Generar QR Code (Base64 + Texto)`
- **Headers**: `Authorization: Bearer {{token}}`, `X-Tenant-ID: {{tenant_id}}`
- **URL**: `/api/employees/{{employee_id}}/qr`
- **Resultado**: Imagen QR en base64 + texto legible

#### 1️⃣1️⃣ **Validar QR**
- **Request**: `Leer QR (Validar Token)` o `Validar QR + Generar Código`
- **Headers**: `Authorization: Bearer {{token}}`, `X-Tenant-ID: {{tenant_id}}`
- **Body**: `{"qr_token": "{{qr_token}}"}`
- **Resultado**: Datos del empleado si token válido

### 🍽️ Registros de Comidas

#### 1️⃣2️⃣ **Registrar Comida**
- **Request**: `Registrar Comida`
- **Headers**: `Authorization: Bearer {{token}}`, `X-Tenant-ID: {{tenant_id}}`
- **Body**:
  ```json
  {
    "employee_id": "{{employee_id}}",
    "agreement_id": "{{agreement_id}}",
    "meal_type": "Lunch",
    "total_amount": 7.50
  }
  ```
- **Resultado**: Comida registrada en el sistema

### 📊 Reportes

#### 1️⃣3️⃣ **Ver Reportes**
- **Request**: `Reporte de Consumo (Por QR)` o `Reporte de Facturación`
- **Headers**: `Authorization: Bearer {{token}}`, `X-Tenant-ID: {{tenant_id}}`
- **Resultado**: Datos de consumo y facturación

---

## 🧪 Flujo de Pruebas Automatizadas (pytest)

### Ejecutar Todas las Pruebas
```bash
# Activar entorno virtual
.venv\Scripts\activate.ps1

# Instalar dependencias de testing
pip install -r requirements-dev.txt

# Ejecutar tests con cobertura
pytest tests/ -v --cov=app --cov-report=html
```

### Tipos de Pruebas
- **Unitarias**: `pytest tests/unit/` - Funciones individuales
- **Integración**: `pytest tests/integration/` - Flujos completos
- **Seguridad**: `pytest tests/security/` - Auth y permisos

### Análisis de Seguridad
```bash
# Bandit (vulnerabilidades código)
bandit -r app/ -v

# Safety (dependencias)
safety check

# Pylint (calidad código)
pylint app/
```

---

## 🔧 Comandos Útiles

### Backend
```bash
# Ejecutar servidor
python run_server.py

# Ejecutar tests
python run_tests.py --all

# Ver documentación API
# Abrir: http://localhost:8000/docs
```

### Base de Datos
```bash
# Crear/resetear DB
python setup_db.py
python setup_tenants.py

# Ejecutar migraciones
alembic upgrade head
```

### Frontend
```bash
cd starter-kit/starter-kit
npm run dev
```

---

## 📚 Documentación Adicional

- **README.md**: Visión general del proyecto
- **TECHNICAL_GUIDE.md**: Detalles técnicos de implementación
- **TESTING_GUIDE.md**: Guía completa de testing
- **QUICK_COMMANDS.md**: Referencia rápida de comandos
- **README_TESTS.md**: Resumen de suite de pruebas

---

## 🚨 Notas Importantes

- **Multi-tenancy**: Siempre incluir header `X-Tenant-ID` en requests autenticados
- **Tokens**: Access tokens expiran en 30 min, refresh en 7 días
- **Permisos**: Solo `company_admin` puede crear empleados
- **RUC**: Validación estricta de 13 dígitos para empresas ecuatorianas
- **QR**: Tokens únicos por empleado, válidos indefinidamente

---

*Desarrollado para optimizar la gestión de servicios de alimentación empresarial* 🍽️</content>
<parameter name="filePath">c:\Users\Lenovo\Downloads\SMARTPC_Pasantias\CODIGO\backend_plantilla\FLUJO_MESAPASS.md