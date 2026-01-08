"""
🏦 Selector de Fondos de Inversión - Streamlit App
Herramienta interactiva para filtrar y seleccionar los mejores fondos de inversión.
"""

import streamlit as st
import pandas as pd
import numpy as np

# Importar módulos del proyecto
from src.data_processing import load_and_clean_data, get_column_descriptions
from src.filters import apply_filters, get_filter_options
from src.scoring import calculate_fund_score, get_top_funds, PRESET_PROFILES, explain_score
from src.visualizations import (
    plot_risk_return_scatter,
    plot_top_funds_comparison,
    plot_fund_radar,
    plot_fees_comparison,
    create_fund_summary_table,
    plot_score_breakdown,
    plot_by_category
)

# Configuración de la página
st.set_page_config(
    page_title="Selector de Fondos",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .fund-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_datos():
    """Carga y cachea los datos de fondos."""
    return load_and_clean_data('funds.xlsx')


def main():
    # Header
    st.markdown('<h1 class="main-header">🏦 Selector de Fondos de Inversión</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Cargar datos
    try:
        df = cargar_datos()
        filter_options = get_filter_options(df)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        st.stop()
    
    # Sidebar - Configuración
    with st.sidebar:
        st.header("👤 Perfil del Cliente")
        
        # Inversión disponible
        inversion = st.number_input(
            "💰 Inversión disponible (€)",
            min_value=100,
            max_value=1000000,
            value=5000,
            step=500
        )
        
        # Horizonte temporal
        horizonte = st.selectbox(
            "⏱️ Horizonte temporal",
            options=['corto', 'medio', 'largo'],
            format_func=lambda x: {
                'corto': 'Corto plazo (< 2 años)',
                'medio': 'Medio plazo (2-5 años)',
                'largo': 'Largo plazo (> 5 años)'
            }[x],
            index=1
        )
        
        # Tolerancia al riesgo
        tolerancia = st.selectbox(
            "📊 Tolerancia al riesgo",
            options=['conservador', 'moderado', 'agresivo'],
            format_func=lambda x: {
                'conservador': '🛡️ Conservador',
                'moderado': '⚖️ Moderado',
                'agresivo': '🚀 Agresivo'
            }[x],
            index=1
        )
        
        # Preferencia ESG
        solo_esg = st.checkbox("🌱 Solo fondos sostenibles (ESG)")
        
        st.markdown("---")
        st.header("🔍 Filtros Avanzados")
        
        # Tipo de activo
        tipos_activo = st.multiselect(
            "🏛️ Tipo de activo",
            options=filter_options['tipo_activo'],
            default=[]
        )
        
        # Región
        regiones = st.multiselect(
            "🌍 Región geográfica",
            options=filter_options['region'],
            default=[]
        )
        
        # Divisa
        divisas = st.multiselect(
            "💱 Divisa",
            options=filter_options['divisa'],
            default=[]
        )
        
        # Nivel de riesgo
        riesgo_min, riesgo_max = st.slider(
            "⚠️ Nivel de riesgo",
            min_value=1,
            max_value=7,
            value=(1, 7)
        )
        
        # Rating Morningstar
        rating_min = st.slider(
            "⭐ Rating Morningstar mínimo",
            min_value=1,
            max_value=5,
            value=1
        )
        
        # Comisión TER máxima
        ter_max = st.slider(
            "💸 Comisión TER máxima (%)",
            min_value=0.0,
            max_value=5.0,
            value=3.0,
            step=0.1
        )
        
        # Tipo de beneficio
        beneficio = st.selectbox(
            "📈 Tipo de beneficio",
            options=['todos', 'acumulado', 'distribuido'],
            format_func=lambda x: {
                'todos': 'Todos',
                'acumulado': 'Solo Acumulado',
                'distribuido': 'Solo Distribuido'
            }[x]
        )
        
        st.markdown("---")
        st.header("🎯 Perfil de Scoring")
        
        # Perfil predefinido
        perfil_scoring = st.selectbox(
            "Selecciona un perfil",
            options=list(PRESET_PROFILES.keys()),
            format_func=lambda x: PRESET_PROFILES[x]['nombre'],
            index=1
        )
        
        # Mostrar descripción del perfil
        st.caption(PRESET_PROFILES[perfil_scoring]['descripcion'])
        
        # Pesos personalizados
        usar_custom = st.checkbox("⚖️ Usar pesos personalizados")
        
        if usar_custom:
            st.markdown("##### Ajusta los pesos (deben sumar 1.0):")
            col1, col2 = st.columns(2)
            with col1:
                peso_rend12 = st.slider("Rend. 12M", 0.0, 0.5, 0.15, 0.05)
                peso_rend36 = st.slider("Rend. 36M", 0.0, 0.5, 0.15, 0.05)
                peso_rend60 = st.slider("Rend. 60M", 0.0, 0.5, 0.10, 0.05)
                peso_sharpe = st.slider("Sharpe", 0.0, 0.5, 0.20, 0.05)
            with col2:
                peso_riesgo = st.slider("Bajo Riesgo", 0.0, 0.5, 0.10, 0.05)
                peso_comision = st.slider("Bajas Comisiones", 0.0, 0.5, 0.15, 0.05)
                peso_rating = st.slider("Rating", 0.0, 0.5, 0.10, 0.05)
                peso_esg = st.slider("ESG", 0.0, 0.5, 0.05, 0.05)
            
            suma = peso_rend12 + peso_rend36 + peso_rend60 + peso_sharpe + peso_riesgo + peso_comision + peso_rating + peso_esg
            if abs(suma - 1.0) > 0.01:
                st.warning(f"⚠️ Suma de pesos: {suma:.2f} (debe ser 1.0)")
            else:
                st.success(f"✅ Suma de pesos: {suma:.2f}")
    
    # Construir filtros
    filters = {
        'inversion_cliente': inversion,
        'tolerancia_minimo': 0.1,
        'nivel_riesgo_min': riesgo_min,
        'nivel_riesgo_max': riesgo_max,
        'rating_min': rating_min,
        'comision_ter_max': ter_max / 100,
    }
    
    if tipos_activo:
        filters['tipo_activo'] = tipos_activo
    if regiones:
        filters['region'] = regiones
    if divisas:
        filters['divisa'] = divisas
    if solo_esg:
        filters['solo_sostenibles'] = True
    if beneficio == 'acumulado':
        filters['solo_acumulado'] = True
    elif beneficio == 'distribuido':
        filters['solo_distribuido'] = True
    
    # Aplicar filtros
    filtered_df = apply_filters(df, filters)
    
    # Calcular scores
    if usar_custom:
        custom_weights = {
            'rendimiento_12m': peso_rend12,
            'rendimiento_36m': peso_rend36,
            'rendimiento_60m': peso_rend60,
            'sharpe_ratio': peso_sharpe,
            'riesgo_bajo': peso_riesgo,
            'comisiones_bajas': peso_comision,
            'rating_morningstar': peso_rating,
            'rating_sostenibilidad': peso_esg,
        }
        scored_df = calculate_fund_score(filtered_df, custom_weights=custom_weights)
    else:
        scored_df = calculate_fund_score(filtered_df, weights=perfil_scoring)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Fondos", len(df))
    with col2:
        st.metric("🔍 Fondos Filtrados", len(filtered_df))
    with col3:
        if len(scored_df) > 0:
            st.metric("🏆 Mejor Score", f"{scored_df['score'].max():.1f}")
        else:
            st.metric("🏆 Mejor Score", "N/A")
    with col4:
        st.metric("💰 Tu Inversión", f"€{inversion:,.0f}")
    
    st.markdown("---")
    
    # Verificar si hay resultados
    if len(filtered_df) == 0:
        st.warning("⚠️ No se encontraron fondos con estos criterios. Intenta relajar los filtros.")
        st.stop()
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Top 10 Fondos", "📊 Visualizaciones", "🔎 Detalle de Fondo", "📈 Análisis General"])
    
    with tab1:
        st.header("🏆 Top 10 Fondos Recomendados")
        
        top_10 = scored_df.head(10)
        
        # Tabla resumen
        tabla = create_fund_summary_table(top_10)
        st.dataframe(tabla, use_container_width=True, hide_index=True)
        
        # Exportar
        col1, col2 = st.columns([3, 1])
        with col2:
            csv = top_10.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="💾 Descargar Top 10 (CSV)",
                data=csv,
                file_name="top_10_fondos.csv",
                mime="text/csv"
            )
    
    with tab2:
        st.header("📊 Visualizaciones")
        
        viz_option = st.selectbox(
            "Selecciona visualización:",
            options=[
                "Riesgo vs Rendimiento",
                "Comparación Top 10",
                "Desglose del Score",
                "Comparación de Comisiones"
            ]
        )
        
        if viz_option == "Riesgo vs Rendimiento":
            fig = plot_risk_return_scatter(
                scored_df,
                title='Relación Riesgo - Rendimiento',
                highlight_funds=scored_df.head(10)['fund_id'].tolist()
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_option == "Comparación Top 10":
            fig = plot_top_funds_comparison(scored_df, n=10)
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_option == "Desglose del Score":
            fig = plot_score_breakdown(scored_df, n=10)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos suficientes para mostrar el desglose")
                
        elif viz_option == "Comparación de Comisiones":
            fig = plot_fees_comparison(scored_df, n=10)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("🔎 Detalle de Fondo")
        
        # Selector de fondo
        top_10_nombres = scored_df.head(10)['fund_name'].tolist()
        fondo_seleccionado = st.selectbox(
            "Selecciona un fondo del Top 10:",
            options=range(len(top_10_nombres)),
            format_func=lambda x: f"#{x+1} - {top_10_nombres[x][:50]}..."
        )
        
        fondo = scored_df.iloc[fondo_seleccionado]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {fondo['fund_name']}")
            st.markdown(f"**Gestora:** {fondo['fund_manager']}")
            st.markdown(f"**ISIN:** `{fondo['isin']}`")
            
            st.markdown("#### 📊 Características")
            char_col1, char_col2 = st.columns(2)
            with char_col1:
                st.markdown(f"- **Tipo:** {fondo['Tipo de activo']}")
                st.markdown(f"- **Región:** {fondo['Región']}")
                st.markdown(f"- **Divisa:** {fondo['Divisa']}")
            with char_col2:
                st.markdown(f"- **Riesgo:** {fondo['Nivel de riesgo_clean']}/7")
                st.markdown(f"- **Rating:** {fondo['Rating Morningstar']} ⭐")
                st.markdown(f"- **ESG:** {'✅ Sí' if fondo['es_sostenible'] else '❌ No'}")
            
            st.markdown("#### 💰 Rendimientos")
            rend_col1, rend_col2 = st.columns(2)
            with rend_col1:
                st.markdown(f"- **Año actual:** {fondo['Ren. año actual']}")
                st.markdown(f"- **12 meses:** {fondo['Ren. últ. 12 meses']}")
            with rend_col2:
                st.markdown(f"- **36 meses:** {fondo['Ren. últ. 36 meses']}")
                st.markdown(f"- **60 meses:** {fondo['Ren. últ. 60 meses']}")
            
            st.markdown("#### 💸 Comisiones")
            com_col1, com_col2 = st.columns(2)
            with com_col1:
                st.markdown(f"- **TER:** {fondo['Comisión TER']}")
                st.markdown(f"- **Gestión:** {fondo['Comisión gestión']}")
            with com_col2:
                st.markdown(f"- **Suscripción:** {fondo['Comisión suscripción']}")
                st.markdown(f"- **Reembolso:** {fondo['Comisión reembolso']}")
            
            st.markdown(f"#### 📈 Métricas de Riesgo")
            st.markdown(f"- **Sharpe Ratio:** {fondo['Sharpe Ratio']}")
            st.markdown(f"- **Beta:** {fondo['Beta']}")
            st.markdown(f"- **Máxima caída:** {fondo['Máxima caída del fondo']}")
            
            st.markdown(f"#### 💵 Inversión Mínima: {fondo['min_first_buy']}")
        
        with col2:
            st.metric("🎯 Score", f"{fondo['score']:.1f}/100")
            
            # Radar chart
            try:
                fig = plot_fund_radar(fondo, weights=perfil_scoring)
                st.plotly_chart(fig, use_container_width=True)
            except:
                pass
    
    with tab4:
        st.header("📈 Análisis General del Universo de Fondos")
        
        analisis_option = st.selectbox(
            "Selecciona análisis:",
            options=[
                "Rendimiento por Tipo de Activo",
                "Rendimiento por Región",
                "Distribución de Riesgo",
                "Scatter General"
            ]
        )
        
        if analisis_option == "Rendimiento por Tipo de Activo":
            fig = plot_by_category(df, 'Tipo de activo', 'Ren. últ. 12 meses_clean', 
                                   agg='mean', title='Rendimiento Promedio 12M por Tipo de Activo (%)')
            st.plotly_chart(fig, use_container_width=True)
            
        elif analisis_option == "Rendimiento por Región":
            fig = plot_by_category(df, 'Región', 'Ren. últ. 12 meses_clean', 
                                   agg='mean', title='Rendimiento Promedio 12M por Región (%)')
            st.plotly_chart(fig, use_container_width=True)
            
        elif analisis_option == "Distribución de Riesgo":
            import plotly.express as px
            risk_counts = df['Nivel de riesgo_clean'].value_counts().sort_index()
            fig = px.bar(x=risk_counts.index, y=risk_counts.values, 
                         title='Distribución de Fondos por Nivel de Riesgo',
                         labels={'x': 'Nivel de Riesgo', 'y': 'Número de Fondos'})
            st.plotly_chart(fig, use_container_width=True)
            
        elif analisis_option == "Scatter General":
            fig = plot_risk_return_scatter(df, title='Universo Completo: Riesgo vs Rendimiento 12M')
            st.plotly_chart(fig, use_container_width=True)
        
        # Estadísticas generales
        st.markdown("### 📊 Estadísticas del Universo")
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            st.markdown("**Por Tipo de Activo:**")
            tipo_counts = df['Tipo de activo'].value_counts()
            st.dataframe(tipo_counts, use_container_width=True)
        
        with stat_col2:
            st.markdown("**Por Divisa:**")
            divisa_counts = df['Divisa'].value_counts()
            st.dataframe(divisa_counts, use_container_width=True)
        
        with stat_col3:
            st.markdown("**Fondos ESG:**")
            esg_counts = df['es_sostenible'].value_counts()
            st.markdown(f"- Sostenibles: {esg_counts.get(True, 0)}")
            st.markdown(f"- No sostenibles: {esg_counts.get(False, 0)}")


if __name__ == "__main__":
    main()
