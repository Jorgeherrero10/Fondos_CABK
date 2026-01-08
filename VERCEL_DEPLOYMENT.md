# 🚀 Guía de Despliegue en Vercel

## ⚠️ IMPORTANTE: Leer antes de desplegar

Streamlit es una aplicación que requiere un servidor WebSocket persistente, lo cual **no es totalmente compatible** con la arquitectura serverless de Vercel. Esta configuración es **experimental** y puede tener limitaciones.

## 📋 Requisitos Previos

1. Cuenta en [Vercel](https://vercel.com)
2. [Vercel CLI](https://vercel.com/cli) instalado
3. Git instalado y repositorio inicializado
4. Cuenta de GitHub (opcional pero recomendado)

## 🔧 Configuración Incluida

El proyecto ya incluye los archivos necesarios:

- `vercel.json` - Configuración principal de Vercel
- `.vercelignore` - Archivos excluidos del deployment
- `.streamlit/config.toml` - Configuración de Streamlit optimizada
- `requirements.txt` - Dependencias de Python
- `build.sh` - Script de build

## 📦 Pasos para Desplegar

### Opción 1: Desde la línea de comandos

1. **Instalar Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login en Vercel**
   ```bash
   vercel login
   ```

3. **Desplegar**
   ```bash
   # Deployment de prueba
   vercel
   
   # Deployment de producción
   vercel --prod
   ```

4. **Configurar variables de entorno (si es necesario)**
   ```bash
   vercel env add VARIABLE_NAME
   ```

### Opción 2: Desde GitHub (Recomendado)

1. **Sube tu código a GitHub**
   ```bash
   git init
   git add .
   git commit -m "Deploy to Vercel"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/tu-repo.git
   git push -u origin main
   ```

2. **Conecta con Vercel**
   - Ve a [vercel.com/new](https://vercel.com/new)
   - Importa tu repositorio de GitHub
   - Vercel detectará automáticamente la configuración

3. **Configura el proyecto**
   - Framework Preset: **Other**
   - Root Directory: `./`
   - Build Command: `chmod +x build.sh && ./build.sh`
   - Output Directory: `./`
   - Install Command: `pip install -r requirements.txt`

4. **Variables de entorno**
   - `STREAMLIT_SERVER_HEADLESS=true`
   - `STREAMLIT_SERVER_PORT=8501`
   - Cualquier otra variable necesaria

5. **Despliega**
   - Click en "Deploy"
   - Espera a que se complete el build

## ⚙️ Configuración del vercel.json

```json
{
  "version": 2,
  "framework": null,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1",
    "STREAMLIT_SERVER_HEADLESS": "true",
    "STREAMLIT_SERVER_PORT": "8501"
  }
}
```

## 🚨 Limitaciones Conocidas

### Problemas potenciales:

1. **Timeout de funciones serverless**
   - Vercel Hobby: 10 segundos
   - Vercel Pro: 60 segundos
   - Streamlit puede necesitar más tiempo

2. **WebSocket no persistente**
   - Puede causar desconexiones frecuentes
   - Funcionalidad interactiva limitada

3. **Tamaño de deployment**
   - Límite de 50MB por función
   - `funds.xlsx` debe ser < 50MB

4. **Cold starts**
   - Primera carga puede ser muy lenta
   - Subsecuentes cargas también afectadas

## ✅ Alternativas Recomendadas

Si encuentras problemas, considera estas plataformas más adecuadas para Streamlit:

### 1. Streamlit Cloud (⭐ RECOMENDADO)
- **Precio**: Gratis
- **Setup**: 2 minutos
- **Compatibilidad**: 100%
- **URL**: [share.streamlit.io](https://share.streamlit.io)

```bash
# Solo necesitas:
1. Subir a GitHub
2. Conectar en share.streamlit.io
3. ¡Listo!
```

### 2. Railway
- **Precio**: $5/mes (incluye $5 de crédito gratis)
- **Setup**: 5 minutos
- **Compatibilidad**: 100%
- **URL**: [railway.app](https://railway.app)

```bash
# Deployment:
railway login
railway init
railway up
```

### 3. Render
- **Precio**: Plan gratuito disponible
- **Setup**: 5 minutos
- **Compatibilidad**: 100%
- **URL**: [render.com](https://render.com)

### 4. Google Cloud Run
- **Precio**: Pago por uso (muy económico)
- **Setup**: 10 minutos
- **Compatibilidad**: 100%

```bash
gcloud run deploy fund-selector \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔍 Troubleshooting

### Error: "Function timeout"
**Solución**: Streamlit necesita más tiempo. Usa Streamlit Cloud o Railway.

### Error: "Build failed"
**Solución**: 
```bash
# Verifica requirements.txt localmente
pip install -r requirements.txt

# Asegúrate de que funds.xlsx existe
ls -la funds.xlsx
```

### Error: "Application not responding"
**Solución**: La arquitectura serverless de Vercel no mantiene el servidor Streamlit activo. Usa una plataforma con servidores persistentes.

### La aplicación se carga pero no responde
**Solución**: WebSockets no funcionan correctamente. Considera migrar a Streamlit Cloud.

## 📊 Comparación de Plataformas

| Plataforma | Precio | Setup | Compatibilidad | WebSocket | Recomendado |
|------------|--------|-------|----------------|-----------|-------------|
| Streamlit Cloud | Gratis | ⭐⭐⭐⭐⭐ | ✅ 100% | ✅ | ⭐⭐⭐⭐⭐ |
| Railway | $5/mes | ⭐⭐⭐⭐⭐ | ✅ 100% | ✅ | ⭐⭐⭐⭐⭐ |
| Render | Gratis/Pago | ⭐⭐⭐⭐ | ✅ 100% | ✅ | ⭐⭐⭐⭐ |
| Heroku | $7/mes | ⭐⭐⭐⭐ | ✅ 100% | ✅ | ⭐⭐⭐⭐ |
| Vercel | Gratis/Pago | ⭐⭐⭐ | ⚠️ Limitado | ⚠️ | ⭐⭐ |
| Google Cloud Run | Pago por uso | ⭐⭐⭐ | ✅ 100% | ✅ | ⭐⭐⭐⭐ |

## 🎯 Recomendación Final

**Para este proyecto específico:**

1. **Primera opción**: Streamlit Cloud
   - Gratis
   - Configuración más sencilla
   - 100% compatible
   - Diseñado específicamente para Streamlit

2. **Segunda opción**: Railway
   - $5/mes con créditos incluidos
   - Muy fácil de configurar
   - Excelente rendimiento

3. **Tercera opción**: Render
   - Plan gratuito disponible
   - Buena documentación
   - Confiable

**Vercel**: Solo para experimentación o si tienes un plan Pro y aceptas las limitaciones.

## 📚 Recursos Adicionales

- [Documentación Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Documentación Vercel Python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)

## 💬 Soporte

Si tienes problemas con el deployment:

1. Revisa los logs de Vercel
2. Consulta la sección de troubleshooting
3. Considera usar Streamlit Cloud como alternativa
4. Abre un issue en el repositorio

---

**Nota**: Estos archivos de configuración para Vercel se proporcionan "as-is" para experimentación. Para producción, se recomienda fuertemente usar Streamlit Cloud u otra plataforma más adecuada.
