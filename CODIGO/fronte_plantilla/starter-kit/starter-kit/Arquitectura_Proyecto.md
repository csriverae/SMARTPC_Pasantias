# 📐 Arquitectura Proyecto MesaPass

## 1. Visión General

**MesaPass** es una aplicación web moderna con arquitectura **cliente-servidor** que implementa un sistema de gestión con panel administrativo. La aplicación está dividida en dos capas principales:

- **Frontend**: Interfaz web moderna con React/Next.js
- **Backend**: API REST con FastAPI
- **Database**: PostgreSQL

---

## 2. Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────┐
│           CLIENTE (Navegador)                   │
│  Next.js 16 + React 19 + Material-UI            │
│  ├─ Dashboard Administrativo                   │
│  ├─ Gestión de Usuarios                        │
│  └─ Sistema de Autenticación                   │
└──────────────────┬──────────────────────────────┘
                   │ (HTTP/JSON)
                   ↓
┌─────────────────────────────────────────────────┐
│         SERVIDOR API (FastAPI)                  │
│  http://localhost:8000                          │
│  ├─ /users (GET, POST)                         │
│  ├─ /health (GET)                              │
│  └─ Validaciones con Pydantic                  │
└──────────────────┬──────────────────────────────┘
                   │ (SQL)
                   ↓
┌─────────────────────────────────────────────────┐
│       BASE DE DATOS (PostgreSQL)                │
│  ├─ Host: localhost                            │
│  ├─ Puerto: 5434                               │
│  ├─ Database: mesa_db                          │
│  └─ Tablas: users, ...                         │
└─────────────────────────────────────────────────┘
```

---

## 3. Stack Tecnológico

### Backend
| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Framework | FastAPI | Latest |
| ORM | SQLAlchemy | Latest |
| Base de Datos | PostgreSQL | 12+ |
| Validación | Pydantic | v2 |
| Migraciones | Alembic | Latest |
| Python | Python | 3.9+ |

### Frontend
| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Framework | Next.js | 16.1.1 |
| Librería UI | React | 19.2.3 |
| Componentes | Material-UI (MUI) | 7.3.6 |
| Estilos | Emotion (CSS-in-JS) | 11.14.x |
| Package Manager | pnpm | Latest |

---

## 4. Estructura de Carpetas

### Backend (`/app`)

```
app/
├── main.py                 # Entrada principal de FastAPI
├── __init__.py
├── api/
│   └── routes/
│       ├── user.py        # Rutas de usuarios (GET /users, POST /users)
│       └── __pycache__/
├── core/
│   ├── config.py          # Configuración centralizada (Variables de entorno)
│   └── __pycache__/
├── crud/
│   ├── user.py            # Operaciones CRUD de usuarios
│   └── __pycache__/
├── db/
│   ├── base.py            # Configuración base de SQLAlchemy
│   ├── session.py         # Conexión a PostgreSQL (5434)
│   └── __pycache__/
├── models/
│   ├── user.py            # Modelo de datos User (SQLAlchemy)
│   └── __pycache__/
├── schemas/
│   ├── user.py            # Esquemas Pydantic (validación)
│   └── __pycache__/
└── __pycache__/
```

**Patrón de Datos en Backend:**
```
Cliente → Routes (user.py)
    ↓
Schemas (Pydantic - validación)
    ↓
CRUD Operations (user.py)
    ↓
Models (SQLAlchemy - ORM)
    ↓
Database (PostgreSQL)
```

### Frontend (`/src`)

```
src/
├── @core/                  # Core utilities y contextos
│   ├── components/         # Componentes reutilizables
│   ├── contexts/           # Contextos React (settings, auth)
│   ├── hooks/              # Hooks personalizados
│   ├── styles/             # Estilos globales y módulos CSS
│   ├── svg/                # Componentes SVG
│   ├── theme/              # Configuración de tema MUI
│   └── utils/              # Utilidades generales
│
├── @layouts/               # Layouts del sistema
│   ├── BlankLayout.jsx     # Layout sin navegación
│   ├── HorizontalLayout.jsx # Layout con menú horizontal
│   ├── VerticalLayout.jsx   # Layout con menú vertical
│   └── LayoutWrapper.jsx    # Wrapper principal
│
├── @menu/                  # Configuración de menú
│   ├── defaultConfigs.js   # Configuración por defecto
│   ├── horizontal-menu/    # Menú horizontal
│   ├── vertical-menu/      # Menú vertical
│   └── utils/              # Utilidades del menú
│
├── app/                    # App Router de Next.js 16
│   ├── globals.css         # Estilos globales
│   ├── layout.jsx          # Layout raíz
│   ├── (blank-layout-pages)/ # Páginas sin layout
│   ├── (dashboard)/        # Páginas del dashboard
│   └── [...not-found]/     # Página 404
│
├── assets/
│   └── iconify-icons/      # Iconos Iconify
│
├── components/
│   ├── GenerateMenu.jsx    # Generador de menú dinámico
│   ├── Providers.jsx       # Proveedores de React
│   ├── Link.jsx            # Componente de enlace
│   ├── layout/             # Componentes de layout
│   ├── theme/              # Componentes de tema
│   └── stepper-dot/        # Componentes auxiliares
│
├── configs/
│   ├── primaryColorConfig.js # Configuración de color primario
│   └── themeConfig.js       # Configuración general del tema
│
├── data/
│   └── navigation/         # Datos de navegación
│
├── utils/
│   ├── getInitials.js      # Obtener iniciales del nombre
│   └── string.js           # Utilidades de strings
│
└── views/
    ├── Login.jsx           # Página de login
    └── NotFound.jsx        # Página 404
```

---

## 5. Flujo de Datos

### Flujo de Autenticación (Login)
```
1. Usuario ingresa credenciales en Login.jsx
2. Frontend → POST /users (Backend)
3. Backend:
   - Valida con Pydantic (UserCreate schema)
   - CRUD Layer → create_user()
   - ORM → INSERT en tabla users
   - Retorna UserResponse (JSON)
4. Frontend → Almacena sesión/token
5. Redirección al Dashboard
```

### Flujo de Obtención de Usuarios
```
1. Dashboard solicita lista de usuarios
2. Frontend → GET /users (Backend)
3. Backend:
   - CRUD Layer → get_users()
   - ORM → SELECT * FROM users
   - Retorna List[UserResponse]
4. Frontend → Renderiza en tabla/lista
```

---

## 6. Endpoints de API

### Usuarios
| Método | Endpoint | Descripción | Request | Response |
|--------|----------|-------------|---------|----------|
| POST | `/users` | Crear usuario | UserCreate | UserResponse |
| GET | `/users` | Listar usuarios | - | List[UserResponse] |

### Sistema
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Verificar estado del servidor |

---

## 7. Base de Datos

### Configuración de Conexión
```
Host: localhost
Puerto: 5434
Base de Datos: mesa_db
Usuario: postgres
Password: 1234
```

### Modelos de Datos
#### Tabla: users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    -- Campos adicionales según schema
);
```

### Migraciones
- **Tool**: Alembic
- **Ubicación**: `/migrations`
- **Archivos**:
  - `env.py` - Configuración de Alembic
  - `versions/` - Historial de migraciones

---

## 8. Variables de Entorno

### Backend (`.env`)
```env
DB_USER=postgres
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5434
DB_NAME=mesa_db
```

### Frontend (`.env.local`)
```env
BASEPATH=/                 # Ruta base de la aplicación
NEXT_PUBLIC_API_URL=http://localhost:8000  # URL del backend
```

---

## 9. Configuración de Temas

### Material-UI (MUI)
- **Ubicación**: `src/configs/themeConfig.js`
- **Color Primario**: Configurable en `primaryColorConfig.js`
- **Layouts**: 3 opciones
  - Vertical Layout (menú lateral)
  - Horizontal Layout (menú superior)
  - Blank Layout (sin menú)

---

## 10. Proceso de Desarrollo

### Iniciar Backend
```bash
cd app/
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
# Server: http://localhost:8000
```

### Iniciar Frontend
```bash
pnpm install
pnpm dev
# Server: http://localhost:3000
```

---

## 11. Redirecciones y Ruteo

### Next.js Routes
- `/` → Redirección permanente a `/home`
- `/home` → Dashboard principal
- Páginas protegidas según layout
- `[...not-found]` → Página 404 personalizada

---

## 12. Componentes Principales

### Core Components
- **settingsContext.jsx**: Contexto global de configuración
- **useSettings.jsx**: Hook para acceder a configuración
- **useLayoutInit.js**: Inicialización de layout
- **Logo.jsx**: Componente del logo

### Layouts
- **VerticalLayout.jsx**: Layout con navegación vertical
- **HorizontalLayout.jsx**: Layout con navegación horizontal
- **BlankLayout.jsx**: Layout sin navegación (para login, etc.)

### Utilidades
- **GenerateMenu.jsx**: Genera dinámicamente el menú
- **Providers.jsx**: Proveedores de React (Theme, Settings, etc.)

---

## 13. Próximas Mejoras

- [ ] Implementar autenticación JWT
- [ ] Agregar más modelos (Mesas, Pedidos, etc.)
- [ ] Sistema de roles y permisos
- [ ] Validaciones mejoradas
- [ ] Documentación automática de API (Swagger)
- [ ] Tests unitarios y E2E
- [ ] Containerización (Docker)
- [ ] CI/CD Pipeline

---

## 14. Contacto y Documentación Adicional

- **Documentación Backend**: Ver `mesapass-api.md`
- **Framework Backend**: [FastAPI Docs](https://fastapi.tiangolo.com/)
- **Framework Frontend**: [Next.js Docs](https://nextjs.org/docs)
- **Componentes UI**: [Material-UI Docs](https://mui.com/)

---

**Última actualización**: 21 de Marzo, 2026
**Versión del Proyecto**: 5.0.1
