# 🚀 RAILWAY - COMANDOS RÁPIDOS

## 1️⃣ PREPARAR CÓDIGO (En tu terminal local)

```bash
# Ve a la raíz del proyecto
cd backend_plantilla

# Agrega Pillow a requirements.txt (HECHO ✓)
pip install Pillow

# Verifica que todo funciona localmente
python .\starter-kit\starter-kit\run_server.py
# Deberías ver: INFO:     Uvicorn running on http://127.0.0.1:8000

# Prueba en navegador: http://127.0.0.1:8000/docs
```

## 2️⃣ PUSH A GITHUB

```bash
# Desde la raíz del proyecto
cd backend_plantilla

# Agrega todos los cambios
git add .

# Commit
git commit -m "Ready for Railway deployment - Added Dockerfile and configs"

# Push
git push
```

Si tienes error de permisos:
```bash
# Primera vez
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

## 3️⃣ RAILWAY - CREAR PROYECTO (En el navegador)

**URL:** https://railway.app

1. Login con GitHub
2. Dashboard → "New Project"
3. "Deploy from GitHub"
4. Busca tu repositorio
5. Selecciona la rama `main`
6. ⏳ Espera a que compile (5-10 min)

## 4️⃣ RAILWAY - AGREGAR BD

1. En tu proyecto → "Add Service"
2. Busca "PostgreSQL"
3. "Provision PostgreSQL"
4. ⏳ Espera a que se cree (2 min)

## 5️⃣ RAILWAY - CONFIGURAR VARIABLES

En el servicio Backend (tu app FastAPI):

1. Click en "Variables"
2. Agrega estas:

```
DEBUG=false
ENVIRONMENT=production
SECRET_KEY=my-super-secret-key-min-32-chars
ALLOWED_ORIGINS=https://tuapp-prod-xxxx.railway.app
```

⚠️ **Railway crea automáticamente:**
- `DATABASE_URL` (del servicio PostgreSQL)
- `PORT` (del servicio)

NO las toques.

## 6️⃣ RAILWAY - EJECUTAR MIGRACIONES

**Opción A: Manual (en Railway Dashboard)**
1. Tu servicio → "Execute Command"
2. Copia-pega:
```bash
cd starter-kit && alembic upgrade head
```

**Opción B: Automático (recomendado)**
El Dockerfile ya está preparado. Las migraciones se ejecutan al iniciar.

## 7️⃣ OBTENER TU URL

1. En Railway → tu servicio
2. Busca "Domains" o "Deployment"
3. Verás algo como:
```
https://backend-prod-xxxxx.railway.app
```

4. Prueba:
```
https://backend-prod-xxxxx.railway.app/docs
```

Deberías ver Swagger UI ✓

## 8️⃣ ACTUALIZAR FRONTEND (Si tienes Next.js)

En tu proyecto Next.js:

**`.env.local`:**
```
NEXT_PUBLIC_API_URL=https://backend-prod-xxxxx.railway.app
```

**En tus componentes:**
```javascript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Ejemplo:
const response = await fetch(`${API_URL}/api/users`);
```

## 📊 COMANDOS ÚTILES

### Ver logs en vivo
```bash
# En Railway Dashboard → Tu servicio → Logs
# O en terminal (si tienes CLI de Railway):
railway logs --follow
```

### Redeployar
```bash
# En Railway Dashboard:
# Tu servicio → Redeploy

# O simplemente hacer push a GitHub (auto-redeploya):
git push
```

### Ver estado de BD
```bash
# En Railway → PostgreSQL servicio → Logs
# Deberías ver: "accepting connections"
```

---

## ⚠️ PROBLEMAS COMUNES

### ❌ "ModuleNotFoundError: No module named 'PIL'"
```bash
# Ya está resuelto, Pillow está en requirements.txt
```

### ❌ "Database connection refused"
1. Verifica que PostgreSQL esté "running" en Railway
2. Confirma que `DATABASE_URL` esté en Variables
3. Ejecuta migraciones (paso 6️⃣)

### ❌ "No such file or directory: app/main.py"
1. El Dockerfile está buscando en `starter-kit/starter-kit/`
2. Si la estructura cambió, actualiza el Dockerfile

### ❌ App reinicia constantemente
1. Revisa los logs en Railway
2. Busca errores de importación
3. Verifica que todas las dependencias estén en `requirements.txt`

---

## ✅ CHECKLIST FINAL

- [ ] Código pusheado a GitHub
- [ ] Proyecto creado en Railway
- [ ] PostgreSQL agregado
- [ ] Variables de entorno configuradas
- [ ] Migraciones ejecutadas
- [ ] URL funciona en navegador
- [ ] Swagger UI visible en `/docs`
- [ ] Puedes probar endpoints desde Swagger

---

¿Necesitas ayuda? Revisa los logs en Railway o preguntame 🚀
