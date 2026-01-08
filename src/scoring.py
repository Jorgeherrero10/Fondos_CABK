"""
Módulo de scoring para fondos de inversión.
Sistema de puntuación basado en múltiples criterios con pesos ajustables.
"""

import pandas as pd
import numpy as np


# Perfiles predefinidos con pesos para cada criterio
PRESET_PROFILES = {
    'conservador': {
        'nombre': '🛡️ Conservador',
        'descripcion': 'Bajo riesgo, rendimientos estables, comisiones bajas',
        'weights': {
            'rendimiento_12m': 0.10,
            'rendimiento_36m': 0.15,
            'rendimiento_60m': 0.10,
            'sharpe_ratio': 0.15,
            'riesgo_bajo': 0.25,
            'comisiones_bajas': 0.15,
            'rating_morningstar': 0.05,
            'rating_sostenibilidad': 0.05,
        }
    },
    'moderado': {
        'nombre': '⚖️ Moderado',
        'descripcion': 'Balance entre riesgo y rendimiento',
        'weights': {
            'rendimiento_12m': 0.15,
            'rendimiento_36m': 0.15,
            'rendimiento_60m': 0.10,
            'sharpe_ratio': 0.20,
            'riesgo_bajo': 0.10,
            'comisiones_bajas': 0.15,
            'rating_morningstar': 0.10,
            'rating_sostenibilidad': 0.05,
        }
    },
    'agresivo': {
        'nombre': '🚀 Agresivo',
        'descripcion': 'Maximizar rendimientos, acepta mayor riesgo',
        'weights': {
            'rendimiento_12m': 0.25,
            'rendimiento_36m': 0.20,
            'rendimiento_60m': 0.15,
            'sharpe_ratio': 0.15,
            'riesgo_bajo': 0.00,
            'comisiones_bajas': 0.10,
            'rating_morningstar': 0.10,
            'rating_sostenibilidad': 0.05,
        }
    },
    'esg': {
        'nombre': '🌱 ESG / Sostenible',
        'descripcion': 'Prioriza sostenibilidad y criterios ESG',
        'weights': {
            'rendimiento_12m': 0.10,
            'rendimiento_36m': 0.10,
            'rendimiento_60m': 0.10,
            'sharpe_ratio': 0.15,
            'riesgo_bajo': 0.10,
            'comisiones_bajas': 0.10,
            'rating_morningstar': 0.10,
            'rating_sostenibilidad': 0.25,
        }
    },
    'largo_plazo': {
        'nombre': '📈 Largo Plazo',
        'descripcion': 'Enfoque en rendimientos a largo plazo',
        'weights': {
            'rendimiento_12m': 0.05,
            'rendimiento_36m': 0.20,
            'rendimiento_60m': 0.30,
            'sharpe_ratio': 0.15,
            'riesgo_bajo': 0.05,
            'comisiones_bajas': 0.15,
            'rating_morningstar': 0.05,
            'rating_sostenibilidad': 0.05,
        }
    }
}


def get_preset_weights(profile_name):
    """Obtiene los pesos de un perfil predefinido."""
    if profile_name in PRESET_PROFILES:
        return PRESET_PROFILES[profile_name]['weights']
    return PRESET_PROFILES['moderado']['weights']


def normalize_column(series, higher_is_better=True):
    """
    Normaliza una serie a valores entre 0 y 1.
    
    Parameters:
    -----------
    series : pd.Series
        Serie a normalizar
    higher_is_better : bool
        Si True, valores altos obtienen puntuación alta
        Si False, valores bajos obtienen puntuación alta
    """
    min_val = series.min()
    max_val = series.max()
    
    if max_val == min_val:
        return pd.Series(0.5, index=series.index)
    
    normalized = (series - min_val) / (max_val - min_val)
    
    if not higher_is_better:
        normalized = 1 - normalized
    
    return normalized


def calculate_fund_score(df, weights=None, custom_weights=None):
    """
    Calcula la puntuación de cada fondo basándose en múltiples criterios.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos de fondos (ya limpio)
    weights : str
        Nombre del perfil predefinido ('conservador', 'moderado', 'agresivo', 'esg', 'largo_plazo')
    custom_weights : dict
        Pesos personalizados (sobreescribe el perfil si se proporciona)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame con columna 'score' añadida y ordenado por puntuación
    """
    scored = df.copy()
    
    # Obtener pesos
    if custom_weights:
        w = custom_weights
    elif weights:
        w = get_preset_weights(weights)
    else:
        w = get_preset_weights('moderado')
    
    # Calcular scores individuales normalizados
    scores = pd.DataFrame(index=scored.index)
    
    # Rendimientos (higher is better)
    if w.get('rendimiento_12m', 0) > 0:
        scores['rendimiento_12m'] = normalize_column(
            scored['Ren. últ. 12 meses_clean'].fillna(scored['Ren. últ. 12 meses_clean'].median()),
            higher_is_better=True
        ) * w['rendimiento_12m']
    
    if w.get('rendimiento_36m', 0) > 0:
        scores['rendimiento_36m'] = normalize_column(
            scored['Ren. últ. 36 meses_clean'].fillna(scored['Ren. últ. 36 meses_clean'].median()),
            higher_is_better=True
        ) * w['rendimiento_36m']
    
    if w.get('rendimiento_60m', 0) > 0:
        scores['rendimiento_60m'] = normalize_column(
            scored['Ren. últ. 60 meses_clean'].fillna(scored['Ren. últ. 60 meses_clean'].median()),
            higher_is_better=True
        ) * w['rendimiento_60m']
    
    # Sharpe Ratio (higher is better)
    if w.get('sharpe_ratio', 0) > 0:
        scores['sharpe_ratio'] = normalize_column(
            scored['Sharpe Ratio_clean'].fillna(scored['Sharpe Ratio_clean'].median()),
            higher_is_better=True
        ) * w['sharpe_ratio']
    
    # Riesgo bajo (lower risk = higher score)
    if w.get('riesgo_bajo', 0) > 0:
        scores['riesgo_bajo'] = normalize_column(
            scored['Nivel de riesgo_clean'].fillna(4),  # Asume riesgo medio si no hay dato
            higher_is_better=False
        ) * w['riesgo_bajo']
    
    # Comisiones bajas (lower is better)
    if w.get('comisiones_bajas', 0) > 0:
        scores['comisiones_bajas'] = normalize_column(
            scored['Comisión TER_clean'].fillna(scored['Comisión TER_clean'].median()),
            higher_is_better=False
        ) * w['comisiones_bajas']
    
    # Rating Morningstar (higher is better) - solo si hay datos
    if w.get('rating_morningstar', 0) > 0:
        if scored['Rating Morningstar'].notna().any():
            scores['rating_morningstar'] = normalize_column(
                scored['Rating Morningstar'].fillna(3),
                higher_is_better=True
            ) * w['rating_morningstar']
        else:
            # Si no hay datos, dar puntuación neutral
            scores['rating_morningstar'] = 0.5 * w['rating_morningstar']
    
    # Rating Sostenibilidad (higher is better) - usar es_sostenible como proxy si no hay datos
    if w.get('rating_sostenibilidad', 0) > 0:
        if scored['R. Morningstar Sostenibilidad'].notna().any():
            scores['rating_sostenibilidad'] = normalize_column(
                scored['R. Morningstar Sostenibilidad'].fillna(scored['R. Morningstar Sostenibilidad'].median()),
                higher_is_better=True
            ) * w['rating_sostenibilidad']
        else:
            # Usar es_sostenible como proxy
            scores['rating_sostenibilidad'] = scored['es_sostenible'].astype(float) * w['rating_sostenibilidad']
    
    # Calcular score total
    scored['score'] = scores.sum(axis=1)
    
    # Normalizar score final a 0-100
    scored['score'] = (scored['score'] / scored['score'].max()) * 100
    
    # Añadir scores individuales para transparencia
    for col in scores.columns:
        scored[f'score_{col}'] = scores[col]
    
    return scored.sort_values('score', ascending=False)


def get_top_funds(df, n=10, weights='moderado', custom_weights=None):
    """
    Obtiene los top N fondos según el sistema de scoring.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos de fondos
    n : int
        Número de fondos a devolver
    weights : str
        Perfil de pesos predefinido
    custom_weights : dict
        Pesos personalizados
        
    Returns:
    --------
    pd.DataFrame
        Top N fondos ordenados por puntuación
    """
    scored = calculate_fund_score(df, weights=weights, custom_weights=custom_weights)
    return scored.head(n)


def explain_score(fund_row, weights='moderado'):
    """
    Genera una explicación del score de un fondo específico.
    
    Parameters:
    -----------
    fund_row : pd.Series
        Fila del DataFrame con datos del fondo
    weights : str
        Perfil usado para el scoring
        
    Returns:
    --------
    dict
        Diccionario con la explicación del score
    """
    w = get_preset_weights(weights)
    
    explanation = {
        'fondo': fund_row.get('fund_name', 'N/A'),
        'score_total': round(fund_row.get('score', 0), 2),
        'componentes': {}
    }
    
    component_names = {
        'rendimiento_12m': 'Rendimiento 12 meses',
        'rendimiento_36m': 'Rendimiento 36 meses',
        'rendimiento_60m': 'Rendimiento 60 meses',
        'sharpe_ratio': 'Ratio de Sharpe',
        'riesgo_bajo': 'Nivel de Riesgo',
        'comisiones_bajas': 'Comisiones',
        'rating_morningstar': 'Rating Morningstar',
        'rating_sostenibilidad': 'Sostenibilidad'
    }
    
    for key, name in component_names.items():
        score_col = f'score_{key}'
        if score_col in fund_row.index and w.get(key, 0) > 0:
            explanation['componentes'][name] = {
                'peso': f"{w[key]*100:.0f}%",
                'contribucion': round(fund_row[score_col] * 100, 2)
            }
    
    return explanation
