"""
Módulo de visualizaciones para fondos de inversión.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Configuración de estilo
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ffbb33',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

RISK_COLORS = {
    1: '#2ca02c',  # Verde - muy bajo riesgo
    2: '#98df8a',  # Verde claro
    3: '#ffbb33',  # Amarillo
    4: '#ff7f0e',  # Naranja
    5: '#ff6b6b',  # Rojo claro
    6: '#d62728',  # Rojo
    7: '#8b0000',  # Rojo oscuro - muy alto riesgo
}


def plot_risk_return_scatter(df, x_col='Nivel de riesgo_clean', y_col='Ren. últ. 12 meses_clean',
                              color_col='Tipo de activo', size_col=None, title=None,
                              highlight_funds=None, interactive=True):
    """
    Crea un gráfico de dispersión riesgo vs rendimiento.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos
    x_col : str
        Columna para el eje X (riesgo)
    y_col : str
        Columna para el eje Y (rendimiento)
    color_col : str
        Columna para colorear puntos
    size_col : str
        Columna para tamaño de puntos
    title : str
        Título del gráfico
    highlight_funds : list
        Lista de fund_ids a destacar
    interactive : bool
        Si True, usa Plotly; si False, usa Matplotlib
    """
    plot_df = df.dropna(subset=[x_col, y_col]).copy()
    
    if plot_df.empty:
        print("No hay datos suficientes para el gráfico")
        return None
    
    # Convertir rendimiento a porcentaje para visualización
    plot_df['y_pct'] = plot_df[y_col] * 100
    
    if title is None:
        title = 'Relación Riesgo - Rendimiento'
    
    if interactive:
        fig = px.scatter(
            plot_df,
            x=x_col,
            y='y_pct',
            color=color_col,
            hover_name='fund_name',
            hover_data={
                'fund_manager': True,
                'Rating Morningstar': True,
                'Comisión TER': True,
                x_col: False,
                'y_pct': ':.2f'
            },
            title=title,
            labels={
                x_col: 'Nivel de Riesgo',
                'y_pct': 'Rendimiento (%)',
                color_col: 'Tipo de Activo'
            }
        )
        
        if highlight_funds:
            highlighted = plot_df[plot_df['fund_id'].isin(highlight_funds)]
            fig.add_trace(go.Scatter(
                x=highlighted[x_col],
                y=highlighted['y_pct'],
                mode='markers',
                marker=dict(size=15, color='red', symbol='star'),
                name='Seleccionados',
                hoverinfo='text',
                text=highlighted['fund_name']
            ))
        
        fig.update_layout(
            xaxis=dict(tickmode='linear', tick0=1, dtick=1),
            height=500
        )
        return fig
    else:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for tipo in plot_df[color_col].unique():
            mask = plot_df[color_col] == tipo
            ax.scatter(
                plot_df.loc[mask, x_col],
                plot_df.loc[mask, 'y_pct'],
                label=tipo,
                alpha=0.6
            )
        
        ax.set_xlabel('Nivel de Riesgo')
        ax.set_ylabel('Rendimiento (%)')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig


def plot_top_funds_comparison(df, n=10, metrics=None, title=None):
    """
    Crea un gráfico de barras comparando los top fondos.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame ya ordenado por score
    n : int
        Número de fondos a mostrar
    metrics : list
        Lista de métricas a comparar
    title : str
        Título del gráfico
    """
    if metrics is None:
        metrics = ['score', 'Ren. últ. 12 meses_clean', 'Sharpe Ratio_clean']
    
    top_df = df.head(n).copy()
    
    if title is None:
        title = f'Top {n} Fondos - Comparación'
    
    # Crear nombres cortos para el gráfico
    top_df['short_name'] = top_df['fund_name'].str[:25] + '...'
    
    fig = make_subplots(
        rows=1, cols=len(metrics),
        subplot_titles=['Score', 'Rendimiento 12M (%)', 'Sharpe Ratio'][:len(metrics)]
    )
    
    for i, metric in enumerate(metrics, 1):
        values = top_df[metric].fillna(0)
        if 'Ren.' in metric or metric.endswith('_clean'):
            values = values * 100  # Convertir a porcentaje
        
        fig.add_trace(
            go.Bar(
                y=top_df['short_name'],
                x=values,
                orientation='h',
                name=metric,
                marker_color=list(COLORS.values())[i-1]
            ),
            row=1, col=i
        )
    
    fig.update_layout(
        title=title,
        height=400 + n * 25,
        showlegend=False
    )
    
    return fig


def plot_fund_radar(fund_row, weights='moderado'):
    """
    Crea un gráfico radar para un fondo específico.
    
    Parameters:
    -----------
    fund_row : pd.Series
        Datos del fondo
    weights : str
        Perfil de pesos usado
    """
    categories = ['Rend. 12M', 'Rend. 36M', 'Sharpe', 'Bajo Riesgo', 'Bajas Comisiones', 'Rating']
    
    # Obtener valores normalizados (asumiendo que ya están calculados)
    values = [
        fund_row.get('score_rendimiento_12m', 0) * 100 / 0.25,  # Normalizar
        fund_row.get('score_rendimiento_36m', 0) * 100 / 0.20,
        fund_row.get('score_sharpe_ratio', 0) * 100 / 0.20,
        fund_row.get('score_riesgo_bajo', 0) * 100 / 0.25,
        fund_row.get('score_comisiones_bajas', 0) * 100 / 0.15,
        fund_row.get('score_rating_morningstar', 0) * 100 / 0.10,
    ]
    
    # Cerrar el polígono
    values.append(values[0])
    categories.append(categories[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=fund_row.get('fund_name', 'Fondo')[:30]
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title=f"Perfil del Fondo: {fund_row.get('fund_name', 'N/A')[:40]}"
    )
    
    return fig


def plot_fees_comparison(df, n=20, title=None):
    """
    Crea un gráfico comparando las comisiones de los fondos.
    """
    plot_df = df.head(n).copy()
    plot_df['short_name'] = plot_df['fund_name'].str[:20]
    
    if title is None:
        title = 'Comparación de Comisiones'
    
    fig = go.Figure()
    
    # TER
    fig.add_trace(go.Bar(
        name='Comisión TER',
        y=plot_df['short_name'],
        x=plot_df['Comisión TER_clean'].fillna(0) * 100,
        orientation='h',
        marker_color=COLORS['primary']
    ))
    
    # Gestión
    fig.add_trace(go.Bar(
        name='Comisión Gestión',
        y=plot_df['short_name'],
        x=plot_df['Comisión gestión_clean'].fillna(0) * 100,
        orientation='h',
        marker_color=COLORS['secondary']
    ))
    
    fig.update_layout(
        title=title,
        barmode='group',
        xaxis_title='Comisión (%)',
        height=400 + n * 20
    )
    
    return fig


def plot_distribution(df, column, title=None, bins=30):
    """
    Crea un histograma de distribución de una variable.
    """
    if title is None:
        title = f'Distribución de {column}'
    
    fig = px.histogram(
        df,
        x=column,
        nbins=bins,
        title=title,
        color_discrete_sequence=[COLORS['primary']]
    )
    
    fig.update_layout(
        xaxis_title=column,
        yaxis_title='Frecuencia'
    )
    
    return fig


def plot_by_category(df, category_col, value_col, agg='mean', title=None):
    """
    Crea un gráfico de barras agrupado por categoría.
    """
    if agg == 'mean':
        grouped = df.groupby(category_col)[value_col].mean()
    elif agg == 'median':
        grouped = df.groupby(category_col)[value_col].median()
    elif agg == 'count':
        grouped = df.groupby(category_col)[value_col].count()
    else:
        grouped = df.groupby(category_col)[value_col].sum()
    
    grouped = grouped.sort_values(ascending=False)
    
    if title is None:
        title = f'{value_col} por {category_col}'
    
    fig = px.bar(
        x=grouped.index,
        y=grouped.values * 100 if 'Ren.' in value_col else grouped.values,
        title=title,
        labels={'x': category_col, 'y': value_col}
    )
    
    return fig


def create_fund_summary_table(df, columns=None):
    """
    Crea una tabla resumen de fondos formateada.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los fondos
    columns : list
        Columnas a incluir
        
    Returns:
    --------
    pd.DataFrame
        DataFrame formateado para display
    """
    if columns is None:
        columns = [
            'fund_name', 'fund_manager', 'score', 'Tipo de activo', 'Región',
            'Nivel de riesgo_clean', 'Rating Morningstar',
            'Ren. últ. 12 meses_clean', 'Comisión TER_clean', 'min_first_buy_clean'
        ]
    
    # Filtrar columnas existentes
    available_cols = [c for c in columns if c in df.columns]
    summary = df[available_cols].copy()
    
    # Renombrar columnas para display
    rename_map = {
        'fund_name': 'Nombre',
        'fund_manager': 'Gestora',
        'score': 'Score',
        'Tipo de activo': 'Tipo',
        'Región': 'Región',
        'Nivel de riesgo_clean': 'Riesgo',
        'Rating Morningstar': 'Rating ⭐',
        'Ren. últ. 12 meses_clean': 'Rend. 12M',
        'Comisión TER_clean': 'TER',
        'min_first_buy_clean': 'Mín. Inversión'
    }
    
    summary = summary.rename(columns={k: v for k, v in rename_map.items() if k in summary.columns})
    
    # Formatear valores
    if 'Score' in summary.columns:
        summary['Score'] = summary['Score'].round(1)
    if 'Rend. 12M' in summary.columns:
        summary['Rend. 12M'] = (summary['Rend. 12M'] * 100).round(2).astype(str) + '%'
    if 'TER' in summary.columns:
        summary['TER'] = (summary['TER'] * 100).round(2).astype(str) + '%'
    if 'Mín. Inversión' in summary.columns:
        summary['Mín. Inversión'] = summary['Mín. Inversión'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else 'N/D'
        )
    
    return summary


def plot_score_breakdown(df, n=10):
    """
    Muestra el desglose del score para los top N fondos.
    """
    top_df = df.head(n).copy()
    
    score_cols = [c for c in top_df.columns if c.startswith('score_') and c != 'score']
    
    if not score_cols:
        return None
    
    fig = go.Figure()
    
    # Nombres de componentes más legibles
    component_names = {
        'score_rendimiento_12m': 'Rend. 12M',
        'score_rendimiento_36m': 'Rend. 36M',
        'score_rendimiento_60m': 'Rend. 60M',
        'score_sharpe_ratio': 'Sharpe',
        'score_riesgo_bajo': 'Bajo Riesgo',
        'score_comisiones_bajas': 'Bajas Comisiones',
        'score_rating_morningstar': 'Rating',
        'score_rating_sostenibilidad': 'ESG'
    }
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    
    for i, col in enumerate(score_cols):
        fig.add_trace(go.Bar(
            name=component_names.get(col, col),
            y=top_df['fund_name'].str[:25],
            x=top_df[col] * 100,
            orientation='h',
            marker_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        barmode='stack',
        title='Desglose del Score por Componente',
        xaxis_title='Contribución al Score',
        height=400 + n * 25,
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    
    return fig
