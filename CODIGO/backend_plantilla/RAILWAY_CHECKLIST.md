# ✅ CHECKLIST DEPLOYMENT RAILWAY

## PRE-DEPLOYMENT (Local)
- [ ] Pillow está en `requirements.txt` ✓
- [ ] Todas las dependencias están en `requirements.txt`
- [ ] Variables de entorno configuradas en `.env`
- [ ] `app/main.py` está bien estructurado
- [ ] Migraciones funcionan localmente: `alembic upgrade head`
- [ ] Servidor funciona localmente: `python run_server.py`

## GITHUB
- [ ] Tienes cuenta en GitHub
- [ ] Tu repositorio está en GitHub
- [ ] Repositorio es público (o private con acceso a Railway)
- [ ] Todos los cambios están committed y pusheados
```bash
git add .
git commit -m "Railway ready deployment"
git push
```

## RAILWAY SETUP

### Crear Cuenta
- [ ] Ir a https://railway.app
- [ ] Crear cuenta con GitHub
- [ ] Autorizar Railway en GitHub

### Crear Proyecto
- [ ] Click "New Project"
- [ ] "Deploy from GitHub"
- [ ] Seleccionar tu repositorio
- [ ] Seleccionar rama: `main` o `master`

### Agregar PostgreSQL
- [ ] En el proyecto, click "Add Service"
- [ ] Buscar y seleccionar "PostgreSQL"
- [ ] Railway automáticamente crea la BD

### Variables de Entorno
- [ ] En tu servicio Backend, ir a "Variables"
- [ ] Verificar que `DATABASE_URL` esté (Railway la crea automáticamente)
- [ ] Agregar `DEBUG=false`
- [ ] Agregar `ENVIRONMENT=production`
- [ ] Agregar `SECRET_KEY` (mínimo 32 caracteres)
- [ ] Agregar `ALLOWED_ORIGINS=https://tu-url-railway.railway.app`

### Despliegue Inicial
- [ ] El Dockerfile empieza a compilarse automáticamente
- [ ] Esperar a que termine (5-10 minutos)
- [ ] Revisar logs si hay error

### Migraciones
- [ ] Después del primer deploy, ejecutar migraciones:
  - Opción 1: Dashboard → tu servicio → "Execute Command" → `alembic upgrade head`
  - Opción 2: Modificar Dockerfile para que se ejecuten automáticamente

### Verificación
- [ ] Obtener URL del proyecto en Railway
- [ ] Abrir en navegador: `https://tu-url/docs`
- [ ] Deberías ver Swagger UI
- [ ] Probar un endpoint desde Swagger

## POST-DEPLOYMENT

### Configuración Final
- [ ] Agregar dominio personalizado (opcional)
- [ ] Habilitar auto-deploy desde GitHub
- [ ] Configurar backups automáticos
- [ ] Revisar logs regularmente

### Actualizar Frontend
- [ ] Actualizar URL base de API en Next.js
- [ ] Agregar `NEXT_PUBLIC_API_URL` en `.env`
- [ ] Desplegar frontend (Vercel, Netlify, Railway, etc)

## TROUBLESHOOTING

Si algo no funciona:

1. **Revisar Logs**
   - Railway Dashboard → Tu servicio → "Logs"
   - Buscar líneas rojo (errores)

2. **Errores comunes:**
   - `ModuleNotFoundError: PIL` → Agregar `Pillow==10.2.0` a requirements.txt
   - `Database connection refused` → Verificar `DATABASE_URL`
   - `Port already in use` → Railway maneja el puerto automáticamente
   - `Failed to start app` → Revisar `app/main.py` y `Dockerfile`

3. **Redeployar**
   - Si cambias code en GitHub → Railway automáticamente redeploya
   - O en Railway Dashboard → click el botón "Redeploy"

## URLs ÚTILES
- Railway Docs: https://docs.railway.app
- Tu Dashboard: https://railway.app/dashboard
- Logs en vivo: https://railway.app/dashboard/[project-id]/logs
- Configuración: https://railway.app/dashboard/[project-id]/settings

---

¿Necesitas ayuda con algo específico? 🚀
