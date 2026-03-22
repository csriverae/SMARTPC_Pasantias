# Estructura del Proyecto MesaPass

## Descripción General

El proyecto MesaPass está organizado en una arquitectura de **dos capas principales**:

- **Backend**: API REST desarrollada con FastAPI (Python)
- **Frontend**: Interfaz web moderna desarrollada con Next.js (React)

Cada capa tiene su propia estructura de carpetas y responsabilidades claramente definidas.

---

## Backend (FastAPI)

### Ubicación: `/app`

La carpeta `app/` contiene toda la lógica del servidor API desarrollado con FastAPI. Está organizada siguiendo el patrón de arquitectura en capas, lo que facilita el mantenimiento y escalabilidad del proyecto.

### Estructura de Carpetas

```
app/
├── main.py                  # Punto de entrada principal de la aplicación FastAPI
├── __init__.py             # Inicializador del paquete Python
│
├── api/                    # Rutas y endpoints de la API
│   ├── routes/
│   │   ├── user.py        # Endpoints relacionados con usuarios (GET, POST)
│   │   └── __pycache__/
│   └── __pycache__/
│
├── models/                 # Modelos de datos (SQLAlchemy ORM)
│   ├── user.py            # Definición del modelo User para la tabla users
│   └── __pycache__/
│
├── schemas/                # Esquemas de validación (Pydantic)
│   ├── user.py            # Esquemas UserCreate y UserResponse para validar datos
│   └── __pycache__/
│
├── crud/                   # Operaciones CRUD (Lógica de negocio)
│   ├── user.py            # Funciones para crear, leer, actualizar y eliminar usuarios
│   └── __pycache__/
│
├── db/                     # Configuración de base de datos
│   ├── base.py            # Configuración base de SQLAlchemy
│   ├── session.py         # Conexión y sesión con PostgreSQL
│   └── __pycache__/
│
├── core/                   # Configuración centralizada del proyecto
│   ├── config.py          # Variables de configuración y variables de entorno
│   └── __pycache__/
│
└── __pycache__/           # Caché de Python (se genera automáticamente)
```

### Descripción de Carpetas del Backend

#### **main.py**
- Archivo principal de la aplicación FastAPI
- Define la instancia de la aplicación
- Incluye los routers (rutas) de la API
- Maneja eventos de inicio/apagado
- Endpoints de sistema como `/health`

#### **api/routes/**
- Contiene todos los routers y endpoints de la API
- Cada archivo representa un recurso (usuarios, productos, etc.)
- **user.py**: Define los endpoints para gestión de usuarios
  - `POST /users` - Crear nuevo usuario
  - `GET /users` - Listar todos los usuarios

#### **models/**
- Contiene los modelos de datos (ORM de SQLAlchemy)
- Define la estructura de las tablas en la base de datos
- **user.py**: Modelo User que mapea a la tabla `users`
  - Atributos: id, nombre, email, etc.

#### **schemas/**
- Contiene esquemas de validación con Pydantic
- Valida datos entrantes y salientes
- **user.py**: Define dos esquemas
  - `UserCreate`: Para validar datos al crear usuario
  - `UserResponse`: Para serializar datos al responder

#### **crud/**
- Contiene la lógica de negocio
- Operaciones CRUD (Create, Read, Update, Delete)
- **user.py**: Funciones como:
  - `create_user()` - Crear usuario en base de datos
  - `get_users()` - Obtener lista de usuarios
  - `get_user_by_id()` - Obtener usuario específico

#### **db/**
- Configuración y gestión de la base de datos
- **session.py**: 
  - Conexión a PostgreSQL
  - Host: localhost, Puerto: 5434
  - Base de datos: mesa_db
- **base.py**: Configuración base del ORM

#### **core/**
- Configuración centralizada del proyecto
- **config.py**: 
  - Lee variables de entorno (.env)
  - Credenciales de base de datos
  - Otros parámetros de configuración

---

## Frontend (Next.js)

### Ubicación: `/src`

La carpeta `src/` contiene toda la interfaz de usuario desarrollada con Next.js 16 y React 19. Está organizada modularmente para facilitar el desarrollo y mantenimiento de componentes.

### Estructura de Carpetas

```
src/
├── @core/                  # Utilidades y contextos centrales
│   ├── components/        # Componentes reutilizables internos
│   ├── contexts/          # Contextos de React (configración, autenticación)
│   │   └── settingsContext.jsx  # Contexto global de configuración
│   ├── hooks/             # Hooks personalizados de React
│   │   ├── useImageVariant.js
│   │   ├── useLayoutInit.js
│   │   ├── useSettings.jsx
│   │   └── useObjectCookie.js
│   ├── styles/            # Estilos y módulos CSS
│   ├── svg/               # Componentes SVG reutilizables
│   ├── theme/             # Configuración de tema Material-UI
│   └── utils/             # Funciones utilitarias
│
├── @layouts/              # Layouts de la aplicación
│   ├── BlankLayout.jsx    # Layout sin navegación (login, error)
│   ├── HorizontalLayout.jsx # Layout con menú horizontal
│   ├── VerticalLayout.jsx  # Layout con menú vertical
│   ├── LayoutWrapper.jsx   # Wrapper/contenedor de layouts
│   ├── components/        # Componentes específicos de layouts
│   ├── styles/            # Estilos de layouts
│   └── utils/             # Utilidades de layouts
│
├── @menu/                 # Configuración del menú de navegación
│   ├── defaultConfigs.js  # Configuración por defecto del menú
│   ├── components/        # Componentes del menú
│   ├── contexts/          # Contextos del menú
│   ├── hooks/             # Hooks del menú
│   ├── horizontal-menu/   # Componentes menú horizontal
│   ├── vertical-menu/     # Componentes menú vertical
│   ├── styles/            # Estilos del menú
│   ├── svg/               # Iconos del menú
│   └── utils/             # Utilidades del menú
│
├── app/                   # App Router de Next.js 16 (rutas)
│   ├── globals.css        # Estilos globales de la aplicación
│   ├── layout.jsx         # Layout raíz de todos los archivos
│   ├── (blank-layout-pages)/   # Páginas sin layout (login, signup)
│   ├── (dashboard)/            # Páginas del dashboard con layout
│   └── [...not-found]/         # Página 404 personalizada
│
├── assets/                # Archivos estáticos
│   └── iconify-icons/    # Conjunto de iconos Iconify
│
├── components/            # Componentes generales de la aplicación
│   ├── GenerateMenu.jsx   # Componente generador de menú dinámico
│   ├── Providers.jsx      # Proveedores de contextos (Theme, Settings)
│   ├── Link.jsx           # Componente de enlace personalizado
│   ├── layout/            # Componentes de layout general
│   ├── theme/             # Componentes relacionados con tema
│   └── stepper-dot/       # Componentes auxiliares
│
├── configs/               # Configuración general
│   ├── primaryColorConfig.js   # Configuración de color primario
│   └── themeConfig.js          # Configuración general del tema
│
├── data/                  # Datos estáticos
│   └── navigation/        # Datos de navegación y menús
│
├── utils/                 # Funciones utilitarias generales
│   ├── getInitials.js     # Obtener iniciales del nombre
│   └── string.js          # Utilidades de manipulación de strings
│
└── views/                 # Vistas/Páginas específicas
    ├── Login.jsx          # Página de login
    └── NotFound.jsx       # Página no encontrada
```

### Descripción de Carpetas del Frontend

#### **@core/**
- Carpeta con prefijo `@` (alias de ruta en Next.js)
- Contiene utilidades y contextos centrales del proyecto
- **contexts/**: Contextos globales como configuración y autenticación
- **hooks/**: Hooks personalizados reutilizables
- **theme/**: Configuración de Material-UI
- **utils/**: Funciones utilitarias generales

#### **@layouts/**
- Carpeta con prefijo `@` (alias de ruta)
- Contiene los diferentes layouts/plantillas de la aplicación
- **BlankLayout.jsx**: Sin navegación (usado en login)
- **VerticalLayout.jsx**: Con menú lateral
- **HorizontalLayout.jsx**: Con menú superior
- LayoutWrapper.jsx: Wrapper que rodea todos los layouts

#### **@menu/**
- Carpeta con prefijo `@` (alias de ruta)
- Gestiona la navegación y menú de la aplicación
- **defaultConfigs.js**: Configuración por defecto
- **horizontal-menu/**: Componentes del menú horizontal
- **vertical-menu/**: Componentes del menú vertical
- Separación clara entre menú horizontal y vertical

#### **app/**
- Carpeta especial de Next.js App Router (versión 16)
- Define todas las rutas de la aplicación
- **layout.jsx**: Layout raíz, común para todas las páginas
- **(blank-layout-pages)/**: Grupo de rutas sin layout (login)
- **(dashboard)/**: Grupo de rutas con layout dashboard
- **[...not-found]/**: Manejo de rutas no encontradas (404)

#### **components/**
- Componentes generales reutilizables
- **GenerateMenu.jsx**: Genera dinámicamente el menú
- **Providers.jsx**: Agrupa proveedores de contextos
- **layout/**: Componentes de estructura del layout
- **theme/**: Componentes relacionados con el tema

#### **configs/**
- Configuración general de la aplicación
- **themeConfig.js**: Colores, tipografía, estilos globales
- **primaryColorConfig.js**: Colores primarios personalizables

#### **data/**
- Datos y rutas estáticas
- **navigation/**: Datos que definen el menú y navegación

#### **utils/**
- Funciones utilitarias reutilizables
- **getInitials.js**: Extrae iniciales de nombres
- **string.js**: Manipulación de strings

#### **views/**
- Vistas/Páginas específicas de la aplicación
- **Login.jsx**: Página de inicio de sesión
- **NotFound.jsx**: Página de error 404

---

## Flujo de Integración

El proyecto conecta el Backend y Frontend de la siguiente manera:

1. **Usuario interactúa** con el Frontend (Next.js)
2. **Frontend hace peticiones** al Backend (API FastAPI)
3. **Backend procesa** la petición en las siguientes capas:
   - Routes (api/routes/)
   - Schemas (validación)
   - CRUD (lógica de negocio)
   - Models (acceso a datos)
4. **Base de Datos** (PostgreSQL) almacena/recupera información
5. **Backend retorna** respuesta JSON
6. **Frontend procesa** y renderiza los datos

---

## Puntos Importantes

- **Separación de responsabilidades**: Cada carpeta tiene un propósito específico
- **Modularidad**: Fácil de escalar y mantener
- **Reutilización**: Componentes, hooks y utilidades reutilizables
- **Configuración centralizada**: Temas y configuraciones en carpetas específicas
- **Rutas organizadas**: Grouping de rutas por contexto en Next.js

---

**Última actualización**: 21 de Marzo, 2026
