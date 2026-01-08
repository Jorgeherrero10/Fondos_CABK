# ✅ Checklist de Despliegue

## Pre-Deployment

### 1. Verificar Archivos Necesarios
- [ ] `app.py` existe y funciona localmente
- [ ] `requirements.txt` está actualizado
- [ ] `funds.xlsx` está presente (< 50MB)
- [ ] `src/` directory con todos los módulos
- [ ] `.streamlit/config.toml` está configurado

### 2. Pruebas Locales
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar localmente
streamlit run app.py
```

- [ ] La aplicación carga sin errores
- [ ] Los datos se cargan correctamente
- [ ] Los filtros funcionan
- [ ] Las visualizaciones se muestran
- [ ] El scoring calcula correctamente

### 3. Control de Versiones
```bash
# Inicializar Git (si no está inicializado)
git init

# Agregar archivos
git add .

# Commit
git commit -m "Preparar para deployment"

# Agregar remote (GitHub)
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git

# Push
git push -u origin main
```

## Deployment en Streamlit Cloud (⭐ Recomendado)

### Pasos:
1. [ ] Subir código a GitHub
2. [ ] Ir a [share.streamlit.io](https://share.streamlit.io)
3. [ ] Conectar cuenta de GitHub
4. [ ] Seleccionar repositorio
5. [ ] Configurar:
   - Branch: `main`
   - Main file: `app.py`
   - Python version: 3.11
6. [ ] Hacer click en "Deploy"
7. [ ] Esperar a que termine el deployment (2-5 minutos)
8. [ ] Probar la URL generada

### Secrets (si es necesario):
```toml
# En share.streamlit.io > Settings > Secrets
[general]
API_KEY = "tu_api_key"
```

## Deployment en Railway

### Pasos:
1. [ ] Instalar Railway CLI: `npm install -g @railway/cli`
2. [ ] Login: `railway login`
3. [ ] Crear proyecto: `railway init`
4. [ ] Configurar:
   ```bash
   railway add --service streamlit-app
   ```
5. [ ] Desplegar: `railway up`
6. [ ] Configurar variables de entorno en dashboard
7. [ ] Obtener URL pública

## Deployment en Render

### Pasos:
1. [ ] Ir a [render.com](https://render.com)
2. [ ] Conectar repositorio de GitHub
3. [ ] Seleccionar "New Web Service"
4. [ ] Configurar:
   - Name: `fund-selector`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. [ ] Configurar variables de entorno:
   ```
   STREAMLIT_SERVER_HEADLESS=true
   ```
6. [ ] Hacer click en "Create Web Service"
7. [ ] Esperar deployment (5-10 minutos)

## Deployment en Vercel (⚠️ Experimental)

### Pasos:
1. [ ] Verificar que `vercel.json` existe
2. [ ] Verificar que `.vercelignore` existe
3. [ ] Instalar Vercel CLI: `npm install -g vercel`
4. [ ] Login: `vercel login`
5. [ ] Deployment de prueba: `vercel`
6. [ ] Si funciona, deployment de producción: `vercel --prod`

### Configuración manual (si usas GitHub):
1. [ ] Ir a [vercel.com/new](https://vercel.com/new)
2. [ ] Importar repositorio
3. [ ] Configurar:
   - Framework Preset: `Other`
   - Build Command: `chmod +x build.sh && ./build.sh`
   - Output Directory: `.`
   - Install Command: `pip install -r requirements.txt`
4. [ ] Variables de entorno:
   ```
   STREAMLIT_SERVER_HEADLESS=true
   STREAMLIT_SERVER_PORT=8501
   ```
5. [ ] Desplegar

### ⚠️ Pruebas post-deployment en Vercel:
- [ ] La aplicación carga
- [ ] Los datos se cargan
- [ ] NO hay timeouts frecuentes
- [ ] Las interacciones funcionan
- [ ] Los gráficos se renderizan

**Si hay problemas**: Migrar a Streamlit Cloud o Railway

## Deployment en Heroku

### Pasos:
1. [ ] Instalar Heroku CLI
2. [ ] Login: `heroku login`
3. [ ] Crear app: `heroku create nombre-app`
4. [ ] Verificar que `Procfile` existe
5. [ ] Verificar que `runtime.txt` existe
6. [ ] Verificar que `setup.sh` existe
7. [ ] Desplegar:
   ```bash
   git push heroku main
   ```
8. [ ] Abrir: `heroku open`
9. [ ] Ver logs: `heroku logs --tail`

## Post-Deployment

### Verificaciones:
- [ ] La URL funciona
- [ ] Los datos se cargan correctamente
- [ ] Todas las funcionalidades operan
- [ ] Los gráficos se renderizan
- [ ] No hay errores en consola
- [ ] El rendimiento es aceptable
- [ ] Los filtros aplican correctamente
- [ ] El scoring calcula bien

### Performance:
- [ ] Tiempo de carga inicial < 10 segundos
- [ ] Interacciones responden < 2 segundos
- [ ] Sin timeouts frecuentes
- [ ] Gráficos se cargan rápidamente

### Documentación:
- [ ] Actualizar README con URL de producción
- [ ] Documentar cualquier configuración especial
- [ ] Agregar badges de status (opcional)
- [ ] Crear guía de uso para usuarios finales

## Troubleshooting Común

### Error: "Application Error"
**Causa**: Error en el código o dependencias
**Solución**: 
```bash
# Ver logs
streamlit run app.py --logger.level=debug
```

### Error: "Module not found"
**Causa**: Falta en requirements.txt
**Solución**: 
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Error: "FileNotFoundError: funds.xlsx"
**Causa**: Archivo no incluido en deployment
**Solución**: Verificar que funds.xlsx no está en .gitignore

### Performance lento
**Causa**: Datos grandes o procesamiento pesado
**Solución**:
- Optimizar carga de datos con @st.cache_data
- Reducir tamaño de funds.xlsx si es posible
- Considerar plan pago de la plataforma

## Monitoreo

### Métricas a seguir:
- [ ] Uptime (debe ser > 99%)
- [ ] Response time (debe ser < 5s)
- [ ] Error rate (debe ser < 1%)
- [ ] User sessions

### Herramientas:
- Streamlit Cloud: Built-in analytics
- Railway: Métricas en dashboard
- Render: Logs y métricas
- Heroku: `heroku logs --tail`
- Vercel: Analytics dashboard

## Mantenimiento

### Actualizaciones regulares:
- [ ] Actualizar dependencias mensualmente
- [ ] Revisar logs semanalmente
- [ ] Backup de datos (funds.xlsx)
- [ ] Probar funcionalidad después de cambios

### Proceso de actualización:
```bash
# 1. Hacer cambios localmente
# 2. Probar localmente
streamlit run app.py

# 3. Commit y push
git add .
git commit -m "Descripción del cambio"
git push origin main

# 4. Verificar deployment automático
# 5. Probar en producción
```

## Rollback (si algo sale mal)

### Streamlit Cloud:
1. Ir a Manage App
2. Ver deployments anteriores
3. Revert a versión anterior

### Railway/Render:
1. Ir a Deployments
2. Seleccionar deployment anterior
3. Redeploy

### Vercel:
```bash
vercel rollback
```

### Heroku:
```bash
heroku rollback
```

## Soporte y Recursos

### Documentación oficial:
- [Streamlit Docs](https://docs.streamlit.io)
- [Streamlit Community Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)

### Comunidad:
- [Streamlit Forum](https://discuss.streamlit.io)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/streamlit)

---

**Última actualización**: Enero 2026

✅ **Checklist completado**: ¡Tu aplicación está lista para deployment!
