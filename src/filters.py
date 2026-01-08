"""
Módulo de filtros para fondos de inversión.
"""

import pandas as pd
import numpy as np


def get_filter_options(df):
    """
    Obtiene las opciones disponibles para cada filtro.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos de fondos
        
    Returns:
    --------
    dict
        Diccionario con las opciones para cada filtro
    """
    options = {
        'tipo_activo': sorted([x for x in df['Tipo de activo'].unique() if pd.notna(x) and x != 'N/D']),
        'region': sorted([x for x in df['Región'].unique() if pd.notna(x) and x != 'N/D']),
        'divisa': sorted([x for x in df['Divisa'].unique() if pd.notna(x) and x != 'N/D']),
        'nivel_riesgo': list(range(1, 8)),
        'rating_morningstar': [1, 2, 3, 4, 5],
        'gestoras': sorted([x for x in df['fund_manager'].unique() if pd.notna(x)])[:50],
        'beneficios': ['Acumulado', 'Distribuido'],
    }
    return options


def apply_filters(df, filters):
    """
    Aplica filtros al DataFrame de fondos.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos de fondos
    filters : dict
        Diccionario con los filtros a aplicar
        
    Returns:
    --------
    pd.DataFrame
        DataFrame filtrado
    """
    filtered = df.copy()
    
    # Filtro por tipo de activo
    if filters.get('tipo_activo'):
        filtered = filtered[filtered['Tipo de activo'].isin(filters['tipo_activo'])]
    
    # Filtro por región
    if filters.get('region'):
        filtered = filtered[filtered['Región'].isin(filters['region'])]
    
    # Filtro por divisa
    if filters.get('divisa'):
        filtered = filtered[filtered['Divisa'].isin(filters['divisa'])]
    
    # Filtro por nivel de riesgo
    if filters.get('nivel_riesgo_min') is not None:
        filtered = filtered[filtered['Nivel de riesgo_clean'] >= filters['nivel_riesgo_min']]
    if filters.get('nivel_riesgo_max') is not None:
        filtered = filtered[filtered['Nivel de riesgo_clean'] <= filters['nivel_riesgo_max']]
    
    # Filtro por rating Morningstar (solo si hay datos)
    if filters.get('rating_min') is not None:
        if filtered['Rating Morningstar'].notna().any():
            filtered = filtered[
                (filtered['Rating Morningstar'].isna()) |
                (filtered['Rating Morningstar'] >= filters['rating_min'])
            ]
    
    # Filtro por inversión mínima del cliente
    if filters.get('inversion_cliente') is not None:
        inversion = filters['inversion_cliente']
        tolerancia = filters.get('tolerancia_minimo', 0.1)
        umbral = inversion * (1 + tolerancia)
        filtered = filtered[
            (filtered['min_first_buy_clean'].isna()) | 
            (filtered['min_first_buy_clean'] <= umbral)
        ]
    
    # Filtro solo sostenibles
    if filters.get('solo_sostenibles'):
        filtered = filtered[filtered['es_sostenible'] == True]
    
    # Filtro por tipo de beneficio
    if filters.get('solo_acumulado'):
        filtered = filtered[filtered['Beneficios'] == 'Acumulado']
    if filters.get('solo_distribuido'):
        filtered = filtered[filtered['Beneficios'] == 'Distribuido']
    
    # Filtro por divisa cubierta
    if filters.get('divisa_cubierta'):
        filtered = filtered[filtered['divisa_cubierta'] == True]
    
    # Filtro por comisión TER máxima
    if filters.get('comision_ter_max') is not None:
        filtered = filtered[
            (filtered['Comisión TER_clean'].isna()) |
            (filtered['Comisión TER_clean'] <= filters['comision_ter_max'])
        ]
    
    # Filtro por rendimiento mínimo 12 meses
    if filters.get('rendimiento_12m_min') is not None:
        filtered = filtered[
            (filtered['Ren. últ. 12 meses_clean'].isna()) |
            (filtered['Ren. últ. 12 meses_clean'] >= filters['rendimiento_12m_min'])
        ]
    
    # Filtro por Sharpe ratio mínimo
    if filters.get('sharpe_min') is not None:
        filtered = filtered[
            (filtered['Sharpe Ratio_clean'].isna()) |
            (filtered['Sharpe Ratio_clean'] >= filters['sharpe_min'])
        ]
    
    # Filtro por gestoras
    if filters.get('gestoras'):
        filtered = filtered[filtered['fund_manager'].isin(filters['gestoras'])]
    
    # Filtro por patrimonio mínimo
    if filters.get('patrimonio_min') is not None:
        filtered = filtered[
            (filtered['Patrimonio (millones)_clean'].isna()) |
            (filtered['Patrimonio (millones)_clean'] >= filters['patrimonio_min'])
        ]
    
    return filtered


def filter_by_customer_profile(df, profile):
    """
    Filtra fondos según el perfil del cliente.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con los datos de fondos
    profile : dict
        Perfil del cliente
        
    Returns:
    --------
    pd.DataFrame
        DataFrame filtrado según perfil
    """
    filters = {}
    
    if profile.get('inversion'):
        filters['inversion_cliente'] = profile['inversion']
        filters['tolerancia_minimo'] = 0.1
    
    horizonte = profile.get('horizonte', 'medio')
    if horizonte == 'corto':
        filters['tipo_activo'] = ['Monetario', 'Renta fija']
        filters['nivel_riesgo_max'] = 3
    elif horizonte == 'medio':
        filters['tipo_activo'] = ['Renta fija', 'Mixtos', 'Renta variable']
        filters['nivel_riesgo_max'] = 5
    
    tolerancia = profile.get('tolerancia_riesgo', 'moderado')
    if tolerancia == 'conservador':
        filters['nivel_riesgo_max'] = 3
    elif tolerancia == 'moderado':
        filters['nivel_riesgo_min'] = 2
        filters['nivel_riesgo_max'] = 5
    elif tolerancia == 'agresivo':
        filters['nivel_riesgo_min'] = 4
    
    if profile.get('preferencia_esg'):
        filters['solo_sostenibles'] = True
    
    if profile.get('divisa_preferida'):
        filters['divisa'] = [profile['divisa_preferida']]
    
    return apply_filters(df, filters)
