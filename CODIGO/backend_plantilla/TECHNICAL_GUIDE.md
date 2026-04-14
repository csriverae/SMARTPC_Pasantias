# MesaPass - Guía Técnica y Requisitos

## 📋 Requisitos del Sistema

### Backend (Python/FastAPI)
- **Python**: 3.9+
- **PostgreSQL**: 13+
- **Redis**: Para cache (opcional)
- **Docker**: Para despliegue en contenedores

### Frontend (Next.js)
- **Node.js**: 18+
- **npm/yarn/pnpm**: Gestor de paquetes
- **TypeScript**: 5.0+

### Infraestructura
- **Servidor**: Linux/Windows con 4GB RAM mínimo
- **Almacenamiento**: 10GB para base de datos y logs
- **Backup**: Sistema automático de respaldos

## 🛠️ Instalación y Configuración

### 1. Clonación del Repositorio
```bash
git clone <repository-url>
cd backend_plantilla
```

### 2. Configuración del Backend
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
cp .env.example .env
# Editar .env con tus credenciales de PostgreSQL
```

### 3. Configuración de la Base de Datos
```bash
# Crear base de datos PostgreSQL
createdb mesa_db

# Ejecutar migraciones
alembic upgrade head

# Cargar datos iniciales
python setup_db.py
python setup_tenants.py
```

### 4. Configuración del Frontend
```bash
cd starter-kit/starter-kit
npm install
# o
yarn install
# o
pnpm install
```

### 5. Ejecutar la Aplicación
```bash
# Backend
python run_server.py

# Frontend (en otra terminal)
npm run dev
```

## 🔧 Arquitectura del Sistema

### Backend Architecture
```
app/
├── api/
│   ├── routers/          # Endpoints REST API
│   │   ├── auth.py       # Autenticación JWT
│   │   ├── companies.py  # Gestión de empresas
│   │   ├── restaurants.py # Gestión de restaurantes
│   │   ├── meal_logs.py  # Registros de consumo
│   │   ├── qr.py         # Generación y validación QR
│   │   └── invitations.py # Sistema de invitaciones
│   └── main.py           # Configuración FastAPI
├── core/
│   ├── config.py         # Configuraciones globales
│   └── security.py       # Utilidades de seguridad
├── crud/                 # Operaciones CRUD
├── db/                   # Configuración de base de datos
├── models/               # Modelos SQLAlchemy
├── schemas/              # Esquemas Pydantic
└── services/             # Lógica de negocio
```

### Base de Datos
- **Multi-tenant**: Aislamiento por empresa (tenant_id)
- **Tablas principales**:
  - `companies`: Empresas registradas
  - `employees`: Empleados de cada empresa
  - `restaurants`: Proveedores de comida
  - `meal_logs`: Registros de consumo
  - `agreements`: Acuerdos comerciales
  - `user_invitations`: Sistema de invitaciones

## 🔐 Seguridad

### Autenticación
- **JWT Tokens**: Expiración configurable
- **Hashing**: bcrypt para contraseñas
- **Headers**: X-Tenant-ID para multi-tenant

### Autorización
- **RBAC**: Role-Based Access Control
- **Permisos**: Granulares por módulo
- **Validaciones**: Tenant isolation automático

## 📡 API Endpoints

### Autenticación
- `POST /api/auth/login` - Inicio de sesión
- `POST /api/auth/register` - Registro de usuarios

### Empresas
- `GET /api/companies` - Listar empresas
- `POST /api/companies` - Crear empresa
- `PUT /api/companies/{id}` - Actualizar empresa

### Restaurantes
- `GET /api/restaurants` - Listar restaurantes
- `POST /api/restaurants` - Crear restaurante

### Registros de Consumo
- `POST /api/meal-logs` - Registrar consumo
- `GET /api/meal-logs/employee/{id}/consumption` - Reporte de consumo

### QR Codes
- `GET /api/qr/generate/{employee_id}` - Generar QR
- `POST /api/qr/validate` - Validar QR

## 🧪 Testing

### Backend Tests
```bash
# Ejecutar tests
python -m pytest

# Tests específicos
python test_auth.py
python test_multitenant.py
python test_create_company.py
```

### API Testing
- **Postman Collection**: `Proyecto_MESAPASS_COMPLETE.json`
- **Swagger UI**: `http://localhost:8000/docs`

## 🚀 Despliegue

### Docker
```bash
# Construir imagen
docker build -t mesapass .

# Ejecutar contenedor
docker run -p 8000:8000 mesapass
```

### Producción
- **WSGI Server**: Gunicorn + Uvicorn workers
- **Reverse Proxy**: Nginx
- **SSL**: Certificados Let's Encrypt
- **Monitoring**: Logs centralizados

## 📊 Monitoreo y Logs

### Logs del Sistema
- **FastAPI**: Logs automáticos de requests/responses
- **SQLAlchemy**: Queries y conexiones
- **Errores**: Stack traces detallados

### Métricas
- **Performance**: Tiempo de respuesta de endpoints
- **Uso**: Consumo de recursos del servidor
- **Errores**: Tasa de error por endpoint

## 🔄 Mantenimiento

### Tareas Periódicas
- **Backup**: Diario de base de datos
- **Limpieza**: Logs antiguos (>30 días)
- **Updates**: Dependencias de seguridad

### Actualizaciones
- **Migraciones**: Alembic para cambios de schema
- **Deploy**: Zero-downtime con rolling updates
- **Rollback**: Estrategia de reversión automática

## 🆘 Solución de Problemas

### Problemas Comunes

**Error de conexión a BD**
```bash
# Verificar PostgreSQL
sudo systemctl status postgresql

# Verificar credenciales en .env
cat .env | grep DATABASE_URL
```

**Error de dependencias**
```bash
# Reinstalar entorno virtual
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Error de CORS**
```bash
# Verificar configuración en main.py
# origins = ["http://localhost:3000"]
```

## 📚 Recursos Adicionales

- **Documentación API**: `/docs` (Swagger UI)
- **Base de datos**: Scripts en `migrations/`
- **Configuración**: `.env.example`
- **Tests**: Directorio raíz con archivos `test_*.py`

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

*Para soporte técnico: soporte@mesapass.com*</content>
<parameter name="filePath">c:\Users\Lenovo\Downloads\SMARTPC_Pasantias\CODIGO\backend_plantilla\TECHNICAL_GUIDE.md