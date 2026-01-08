# 🚀 Comandos Rápidos para Deployment

## Vercel

```bash
# Instalar CLI
npm install -g vercel

# Login
vercel login

# Deploy (desarrollo)
vercel

# Deploy (producción)
vercel --prod

# Ver logs
vercel logs

# Información del proyecto
vercel inspect

# Listar deployments
vercel ls

# Eliminar deployment
vercel remove [deployment-url]

# Configurar variables de entorno
vercel env add VARIABLE_NAME
vercel env ls

# Rollback
vercel rollback
```

## Streamlit Cloud

```bash
# No requiere CLI - todo es vía web
# 1. Ir a https://share.streamlit.io
# 2. Conectar GitHub
# 3. Seleccionar repo
# 4. Deploy

# Para actualizar: solo hacer push a GitHub
git push origin main
```

## Railway

```bash
# Instalar CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Deploy
railway up

# Ver logs
railway logs

# Abrir en navegador
railway open

# Configurar variables
railway variables set KEY=value
```

## Render

```bash
# No hay CLI oficial - deployment vía web o Git push
# 1. Conectar repo en https://render.com
# 2. Push a GitHub deploya automáticamente

# Ver logs (vía dashboard o API)
```

## Heroku

```bash
# Instalar CLI (Windows)
# Descargar desde https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Crear app
heroku create nombre-app

# Deploy
git push heroku main

# Ver logs
heroku logs --tail

# Abrir app
heroku open

# Escalar dynos
heroku ps:scale web=1

# Configurar variables
heroku config:set KEY=value
heroku config:get KEY
heroku config

# Reiniciar
heroku restart

# Ejecutar comando
heroku run python --version
```

## Docker

```bash
# Construir imagen
docker build -t fund-selector .

# Ejecutar contenedor
docker run -p 8501:8501 fund-selector

# Ejecutar con variables de entorno
docker run -p 8501:8501 -e VAR=value fund-selector

# Ver logs
docker logs [container-id]

# Detener contenedor
docker stop [container-id]

# Listar contenedores
docker ps

# Eliminar contenedor
docker rm [container-id]

# Push a Docker Hub
docker tag fund-selector username/fund-selector:latest
docker push username/fund-selector:latest
```

## Git (básico)

```bash
# Inicializar repositorio
git init

# Agregar archivos
git add .

# Commit
git commit -m "Mensaje descriptivo"

# Ver status
git status

# Ver historial
git log --oneline

# Crear rama
git branch nueva-rama
git checkout nueva-rama
# o
git checkout -b nueva-rama

# Cambiar de rama
git checkout main

# Merge
git checkout main
git merge nueva-rama

# Agregar remote
git remote add origin https://github.com/usuario/repo.git

# Push
git push -u origin main

# Pull
git pull origin main

# Ver remotes
git remote -v

# Deshacer cambios
git restore archivo.py
git restore .

# Ver diferencias
git diff
```

## Testing Local

```bash
# Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar Streamlit localmente
streamlit run app.py

# Con configuración específica
streamlit run app.py --server.port=8502

# Con debug
streamlit run app.py --logger.level=debug

# Ejecutar tests (si existen)
pytest

# Verificar código
pylint src/
black src/
flake8 src/
```

## Utilities

```bash
# Ver versión de Python
python --version

# Ver pip packages instalados
pip list
pip freeze

# Actualizar package específico
pip install --upgrade streamlit

# Crear requirements.txt
pip freeze > requirements.txt

# Instalar desde requirements.txt
pip install -r requirements.txt

# Limpiar cache de Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete

# Ver tamaño de archivos
du -sh *
ls -lh

# Comprimir proyecto
tar -czf backup.tar.gz .

# Descomprimir
tar -xzf backup.tar.gz
```

## Monitoreo

```bash
# Vercel
vercel logs [deployment-url]

# Railway
railway logs --tail

# Heroku
heroku logs --tail
heroku logs --tail --app nombre-app

# Ver uso de recursos (local)
htop  # Linux/Mac
# o
python -m memory_profiler script.py
```

## Troubleshooting

```bash
# Limpiar cache de npm
npm cache clean --force

# Limpiar cache de pip
pip cache purge

# Reinstalar todo
rm -rf venv/
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt

# Verificar puertos en uso
# Windows
netstat -ano | findstr :8501
# Linux/Mac
lsof -i :8501

# Matar proceso en puerto
# Windows
taskkill /PID [PID] /F
# Linux/Mac
kill -9 [PID]
```

## Variables de Entorno

```bash
# Crear archivo .env (local)
echo "API_KEY=tu_clave" > .env
echo "DEBUG=True" >> .env

# Cargar variables (en Python)
# pip install python-dotenv
# En tu código:
# from dotenv import load_dotenv
# load_dotenv()

# Variables en diferentes plataformas:

# Vercel
vercel env add API_KEY
vercel env pull .env.local

# Heroku
heroku config:set API_KEY=valor

# Railway (vía CLI)
railway variables set API_KEY=valor

# Streamlit Cloud
# Vía web interface: Settings > Secrets
```

## Backups

```bash
# Backup de código
git push origin main

# Backup de base de datos (si aplica)
# PostgreSQL
pg_dump dbname > backup.sql
# MySQL
mysqldump -u user -p database > backup.sql

# Backup de archivos
cp funds.xlsx funds_backup_$(date +%Y%m%d).xlsx

# Backup completo del proyecto
tar -czf ../backup_$(date +%Y%m%d).tar.gz .
```

## Shortcuts útiles

```bash
# Alias para Git (agregar a ~/.bashrc o ~/.zshrc)
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline'

# Alias para desarrollo
alias runapp='streamlit run app.py'
alias install='pip install -r requirements.txt'
alias freeze='pip freeze > requirements.txt'

# Uso después de configurar:
gs          # En lugar de git status
ga          # En lugar de git add .
gc "msg"    # En lugar de git commit -m "msg"
```

---

**Tip**: Guarda este archivo como referencia rápida. Puedes imprimirlo o tenerlo abierto mientras trabajas con deployments.
