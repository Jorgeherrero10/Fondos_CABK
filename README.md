# 🏦 Selector de Fondos de Inversión

Herramienta interactiva desarrollada con Streamlit para filtrar, analizar y seleccionar los mejores fondos de inversión según el perfil y necesidades del cliente.

## 📋 Descripción

Esta aplicación permite a asesores financieros y clientes encontrar los fondos de inversión más adecuados mediante un sistema avanzado de filtrado y scoring personalizado. La herramienta procesa datos de fondos, aplica filtros múltiples y genera recomendaciones basadas en perfiles de inversión predefinidos o personalizados.

## ✨ Características Principales

### 🎯 Perfiles de Inversión
- **Conservador**: Prioriza seguridad y estabilidad
- **Moderado**: Balance entre riesgo y rendimiento
- **Agresivo**: Maximiza potencial de rendimiento
- **ESG**: Enfoque en sostenibilidad
- **Largo Plazo**: Optimizado para horizontes extendidos

### 🔍 Filtros Avanzados
- **Por activo**: Renta fija, renta variable, mixtos, etc.
- **Por geografía**: Europa, América, Asia, mercados emergentes
- **Por divisa**: EUR, USD, GBP, etc.
- **Por nivel de riesgo**: Escala del 1 al 7
- **Por rating**: Clasificación Morningstar (1-5 estrellas)
- **Por comisiones**: Filtro de TER máximo
- **Por sostenibilidad**: Fondos ESG certificados

### 📊 Sistema de Scoring Inteligente
El sistema evalúa cada fondo considerando:
- Rendimiento histórico (12, 36 y 60 meses)
- Ratio de Sharpe (rendimiento ajustado por riesgo)
- Nivel de riesgo
- Comisiones y gastos
- Rating Morningstar
- Certificación de sostenibilidad

### 📈 Visualizaciones Interactivas
- Gráfico de dispersión riesgo-rendimiento
- Comparativa del Top 10 de fondos
- Desglose detallado del score
- Análisis de comisiones
- Gráficos radar para perfiles de fondos
- Análisis por categorías y regiones

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**
   ```bash
   cd "Coding Interview"
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

   Si no existe `requirements.txt`, instalar manualmente:
   ```bash
   pip install streamlit pandas numpy plotly openpyxl ipywidgets
   ```

4. **Verificar estructura de datos**
   Asegúrate de tener el archivo `funds.xlsx` en el directorio raíz del proyecto.

## 📁 Estructura del Proyecto

```
Coding Interview/
│
├── app.py                          # Aplicación principal de Streamlit
├── funds.xlsx                      # Base de datos de fondos
├── README.md                       # Este archivo
│
├── src/                            # Módulos del proyecto
│   ├── __init__.py
│   ├── data_processing.py         # Carga y limpieza de datos
│   ├── filters.py                 # Sistema de filtros
│   ├── scoring.py                 # Algoritmo de scoring
│   └── visualizations.py          # Gráficos y visualizaciones
│
├── fund_selector.ipynb            # Versión Jupyter Notebook
└── InterviewPractice.ipynb        # Cuaderno de práctica
```

## 🎮 Uso de la Aplicación

### Iniciar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Flujo de Trabajo

1. **Configurar Perfil del Cliente** (Barra lateral izquierda)
   - Inversión disponible
   - Horizonte temporal
   - Tolerancia al riesgo
   - Preferencias de sostenibilidad

2. **Aplicar Filtros Avanzados**
   - Selecciona tipos de activo
   - Elige regiones geográficas
   - Define rangos de riesgo
   - Establece límites de comisiones

3. **Seleccionar Perfil de Scoring**
   - Usa perfiles predefinidos
   - O crea pesos personalizados

4. **Explorar Resultados**
   - **Top 10 Fondos**: Tabla con los mejores fondos
   - **Visualizaciones**: Gráficos interactivos
   - **Detalle de Fondo**: Análisis individual completo
   - **Análisis General**: Estadísticas del universo de fondos

5. **Exportar Resultados**
   - Descarga el Top 10 en formato CSV

## 📊 Interpretación de Resultados

### Score de Fondos
- **80-100**: Excelente - Altamente recomendado
- **60-79**: Bueno - Recomendado
- **40-59**: Aceptable - Considerar con cautela
- **<40**: Bajo - No recomendado

### Nivel de Riesgo (SRRI)
- **1-2**: Muy bajo riesgo
- **3-4**: Riesgo bajo a medio
- **5**: Riesgo medio
- **6-7**: Riesgo alto a muy alto

### Rating Morningstar
- ⭐⭐⭐⭐⭐ (5): Excepcional
- ⭐⭐⭐⭐ (4): Por encima del promedio
- ⭐⭐⭐ (3): Promedio
- ⭐⭐ (2): Por debajo del promedio
- ⭐ (1): Bajo rendimiento

## 🛠️ Módulos del Sistema

### `data_processing.py`
Gestiona la carga y limpieza de datos:
- Lectura del archivo Excel
- Normalización de columnas
- Limpieza de valores numéricos
- Creación de variables derivadas

### `filters.py`
Implementa el sistema de filtrado:
- Filtros por inversión mínima
- Filtros por características del fondo
- Filtros por perfil de cliente
- Validación de criterios

### `scoring.py`
Calcula el score de cada fondo:
- Perfiles predefinidos
- Pesos personalizables
- Normalización de métricas
- Explicación del score

### `visualizations.py`
Genera visualizaciones con Plotly:
- Gráficos de dispersión
- Gráficos de barras comparativos
- Gráficos radar
- Tablas interactivas

## 🌐 Despliegue en Producción

### Opción 1: Streamlit Cloud (Recomendado)

Streamlit Cloud es la plataforma nativa y gratuita para desplegar aplicaciones Streamlit:

1. **Sube tu código a GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/tu-usuario/tu-repositorio.git
   git push -u origin main
   ```

2. **Despliega en Streamlit Cloud**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Conecta tu cuenta de GitHub
   - Selecciona tu repositorio
   - Especifica `app.py` como archivo principal
   - ¡Despliega!

3. **Configura secretos (si es necesario)**
   - En el dashboard de Streamlit Cloud, ve a Settings > Secrets
   - Añade variables de entorno sensibles

### Opción 2: Heroku

1. **Instala Heroku CLI**
   ```bash
   # Descarga desde https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Crea una app en Heroku**
   ```bash
   heroku login
   heroku create nombre-de-tu-app
   ```

3. **Despliega**
   ```bash
   git push heroku main
   ```

4. **Abre tu aplicación**
   ```bash
   heroku open
   ```

### Opción 3: Docker

1. **Crea un Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Construye y ejecuta**
   ```bash
   docker build -t fund-selector .
   docker run -p 8501:8501 fund-selector
   ```

### ⚠️ Nota sobre Vercel

Vercel está optimizado para aplicaciones frontend estáticas y Next.js. **Streamlit NO es compatible nativamente con Vercel** ya que requiere un servidor Python persistente.

**Alternativas recomendadas:**
- **Streamlit Cloud** (gratuito, más fácil, nativo)
- **Heroku** (fácil configuración con Procfile incluido)
- **Google Cloud Run** (escalable, pago por uso)
- **Railway** (alternativa moderna a Heroku)
- **AWS EC2/ECS** (mayor control)

Si necesitas frontend en Vercel, considera arquitectura híbrida:
- Frontend (React/Next.js) en Vercel
- Backend/Streamlit en Streamlit Cloud o Heroku
- Comunicación via API

### Archivos de Configuración Incluidos

Este proyecto incluye:
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `.streamlit/config.toml` - Configuración de Streamlit
- ✅ `Procfile` - Para despliegue en Heroku
- ✅ `runtime.txt` - Especifica versión de Python
- ✅ `setup.sh` - Script de configuración
- ✅ `.gitignore` - Archivos a ignorar en Git

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Realiza un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso educativo y profesional.

## 👤 Autor

Jorge

## 📞 Soporte

Para preguntas o problemas, contacta al equipo de desarrollo o abre un issue en el repositorio.

---

**Última actualización**: Enero 2026

¡Buena suerte con tus inversiones! 🚀📈
