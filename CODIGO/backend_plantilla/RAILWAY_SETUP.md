# 🚀 GUÍA RAILWAY - PASO A PASO

## PASO 1: Preparar GitHub
```bash
# 1. Sube todo tu código a GitHub
git add .
git commit -m "Railway deployment ready"
git push
```

## PASO 2: Crear cuenta en Railway
1. Ve a https://railway.app
2. Haz clic en "Start Project"
3. Login con GitHub (authorize la app)

## PASO 3: Crear el proyecto en Railway

### A. Crear nuevo proyecto
1. En el dashboard → "New Project"
2. Selecciona "Deploy from GitHub"
3. Busca tu repositorio
4. Selecciona la rama `main` o `master`
5. Railway empezará a leer el Dockerfile

### B. Agregar PostgreSQL
1. En el proyecto → "Add Service"
2. Busca "PostgreSQL"
3. Selecciona la versión más reciente
4. Railway creará automáticamente la BD

## PASO 4: Configurar Variables de Entorno

En Railway dashboard:

1. Selecciona tu servicio (la app FastAPI)
2. Busca la sección "Variables"
3. Agrega estas variables:

```
DATABASE_URL=postgresql://postgres:[DB_PASSWORD]@[DB_HOST]:5432/[DB_NAME]
DEBUG=false
ENVIRONMENT=production
SECRET_KEY=tu-clave-super-secreta-de-32-caracteres
ALLOWED_ORIGINS=https://tu-dominio.railway.app
PORT=8000
```

⚠️ **IMPORTANTE**: Railway te proporciona automáticamente:
- `DATABASE_URL` (si agregas PostgreSQL)
- `PORT`

Solo configura las demás variables.

## PASO 5: Variables de PostgreSQL

Cuando agregues PostgreSQL, Railway crea automáticamente:
- `DATABASE_URL` - usa ESTA variable
- `PGPASSWORD`
- `PGUSER`
- `PGHOST`
- `PGPORT`
- `PGDATABASE`

En tu `app/core/config.py`, asegúrate que uses:
```python
from app.core.config import settings
database_url = settings.DATABASE_URL
```

## PASO 6: Ejecutar Migraciones (IMPORTANTE)

Las migraciones se hacen en Railway antes de que la app inicie.

**Opción A: En Railway (Recomendado)**
1. En tu servicio → "Deploy" → "Run Command"
2. Ejecuta:
```bash
alembic upgrade head
```

**Opción B: Automático (crear script de inicio)**
Modifica tu `Dockerfile`:
```dockerfile
# ... resto del Dockerfile ...
RUN pip install --no-cache-dir -r requirements.txt

COPY starter-kit/starter-kit/ .

# Ejecutar migraciones al iniciar
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

## PASO 7: Obtener la URL

Cuando se despliegue exitosamente:
1. En Railway → tu servicio
2. Busca la sección "Domains"
3. Verás una URL como: `https://proyecto-prod-xxxx.railway.app`
4. Tu API estará en: `https://proyecto-prod-xxxx.railway.app/api`
5. Docs en: `https://proyecto-prod-xxxx.railway.app/docs`

## PASO 8: Actualizar Frontend

Si tienes un frontend en Next.js:
1. Actualiza la URL base en tus llamadas a API:
```javascript
// En tus componentes Next.js
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://proyecto-prod-xxxx.railway.app';
```

2. Agrega a tu `.env.local`:
```
NEXT_PUBLIC_API_URL=https://proyecto-prod-xxxx.railway.app
```

## TROUBLESHOOTING

### ❌ Error: "Port already in use"
Railway automáticamente usa variables `$PORT`. Asegúrate en el Dockerfile:
```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### ❌ Error: "Database connection refused"
1. Verifica que `DATABASE_URL` esté correctamente configurada
2. En Railway, la BD debe estar en el mismo proyecto
3. Ejecuta las migraciones primero

### ❌ Error: "ModuleNotFoundError: No module named 'PIL'"
Asegúrate que `requirements.txt` incluya:
```
Pillow==10.2.0
```

### ❌ App se reinicia constantemente
1. Revisa los logs: Dashboard → tu servicio → "Logs"
2. Busca errores de importación o configuración
3. Verifica variables de entorno

## VERIFICAR QUE FUNCIONA

Una vez desplegado:
1. Abre en navegador: `https://tu-url-railway.railway.app/docs`
2. Deberías ver Swagger UI con tus endpoints
3. Prueba un endpoint sencillo desde Swagger

## PRÓXIMOS PASOS

- ✅ Agrega tu dominio personalizado (en Railway)
- ✅ Configura auto-deploy (cada push a GitHub se deploya automáticamente)
- ✅ Habilita backups automáticos de BD
- ✅ Configura CI/CD si quieres más control

¿Necesitas ayuda con algún paso específico? 🚀
