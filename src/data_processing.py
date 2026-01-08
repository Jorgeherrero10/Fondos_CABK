"""
Módulo de procesamiento y limpieza de datos de fondos de inversión.
"""

import pandas as pd
import numpy as np
import re


def clean_percentage(value):
    """Convierte strings de porcentaje a float (ej: '1,41%' -> 0.0141)"""
    if pd.isna(value) or value == 'N/D':
        return np.nan
    if isinstance(value, (int, float)):
        return value
    try:
        cleaned = str(value).replace('%', '').replace(',', '.').strip()
        return float(cleaned) / 100
    except (ValueError, AttributeError):
        return np.nan


def clean_currency(value):
    """Extrae el valor numérico de strings de moneda (ej: '600,00€ ISIN' -> 600.0)"""
    if pd.isna(value) or value == 'N/D':
        return np.nan
    if isinstance(value, (int, float)):
        return value
    try:
        # Extraer número con posibles decimales usando coma
        match = re.search(r'([\d.]+),(\d+)', str(value))
        if match:
            integer_part = match.group(1).replace('.', '')
            decimal_part = match.group(2)
            return float(f"{integer_part}.{decimal_part}")
        # Intentar extraer solo número
        match = re.search(r'[\d.]+', str(value).replace(',', '.'))
        if match:
            return float(match.group())
        return np.nan
    except (ValueError, AttributeError):
        return np.nan


def clean_numeric_spanish(value):
    """Limpia valores numéricos en formato español (ej: '1.234,56' -> 1234.56)"""
    if pd.isna(value) or value == 'N/D':
        return np.nan
    if isinstance(value, (int, float)):
        return value
    try:
        cleaned = str(value).replace('.', '').replace(',', '.').strip()
        return float(cleaned)
    except (ValueError, AttributeError):
        return np.nan


def clean_risk_level(value):
    """Convierte nivel de riesgo a entero (1-7)"""
    if pd.isna(value) or value == 'N/D':
        return np.nan
    try:
        return int(value)
    except (ValueError, TypeError):
        return np.nan


def load_and_clean_data(filepath='funds.xlsx'):
    """
    Carga y limpia el archivo de fondos.
    
    Parameters:
    -----------
    filepath : str
        Ruta al archivo Excel con los datos de fondos
        
    Returns:
    --------
    pd.DataFrame
        DataFrame limpio con columnas numéricas procesadas
    """
    df = pd.read_excel(filepath)
    
    # Columnas de porcentaje a limpiar
    percentage_cols = [
        'Ren. año actual', 'Ren. últ. 12 meses', 'Ren. últ. 36 meses', 
        'Ren. últ. 60 meses', 'Ren. 2025', 'Ren. 2024', 'Ren. 2023', 'Ren. 2022',
        'Comisión TER', 'Comisión gestión', 'Comisión suscripción', 'Comisión reembolso',
        'Taxonomía de la UE', 'Reglamento de Divulgación',
        'Sharpe Ratio', 'Beta', 'Jensen Alpha', 'Aplha', 'Máxima caída del fondo'
    ]
    
    for col in percentage_cols:
        if col in df.columns:
            df[col + '_clean'] = df[col].apply(clean_percentage)
    
    # Columnas de moneda
    currency_cols = ['Valor liquidativo', 'Patrimonio (millones)', 'Importe mínimo primera compra']
    for col in currency_cols:
        if col in df.columns:
            df[col + '_clean'] = df[col].apply(clean_currency)
    
    # min_first_buy especial (tiene 'ISIN' en el string)
    df['min_first_buy_clean'] = df['min_first_buy'].apply(clean_currency)
    
    # Nivel de riesgo
    df['Nivel de riesgo_clean'] = df['Nivel de riesgo'].apply(clean_risk_level)
    
    # Participes
    df['Participes_clean'] = df['Participes'].apply(clean_numeric_spanish)
    
    # Crear columnas auxiliares útiles
    df['es_sostenible'] = df['Pref. Sostenibilidad'] == 'Sí'
    df['es_acumulado'] = df['Beneficios'] == 'Acumulado'
    df['divisa_cubierta'] = df['Divisa cubierta'] == 'Sí'
    
    # Extraer moneda del min_first_buy
    df['moneda_minimo'] = df['min_first_buy'].apply(
        lambda x: 'EUR' if '€' in str(x) else ('USD' if '$' in str(x) else 'Otra')
    )
    
    return df


def get_column_descriptions():
    """Devuelve diccionario con descripciones de columnas en español"""
    return {
        'fund_name': 'Nombre del Fondo',
        'fund_manager': 'Gestora',
        'isin': 'Código ISIN',
        'Nivel de riesgo_clean': 'Nivel de Riesgo (1-7)',
        'Rating Morningstar': 'Rating Morningstar (1-5)',
        'R. Morningstar Sostenibilidad': 'Rating Sostenibilidad',
        'Ren. año actual_clean': 'Rendimiento Año Actual',
        'Ren. últ. 12 meses_clean': 'Rendimiento 12 Meses',
        'Ren. últ. 36 meses_clean': 'Rendimiento 36 Meses',
        'Ren. últ. 60 meses_clean': 'Rendimiento 60 Meses',
        'Comisión TER_clean': 'Comisión TER',
        'Comisión gestión_clean': 'Comisión de Gestión',
        'Sharpe Ratio_clean': 'Ratio de Sharpe',
        'Máxima caída del fondo_clean': 'Máxima Caída (Drawdown)',
        'Tipo de activo': 'Tipo de Activo',
        'Región': 'Región Geográfica',
        'Divisa': 'Divisa',
        'min_first_buy_clean': 'Inversión Mínima',
        'Patrimonio (millones)_clean': 'Patrimonio (Millones)',
        'es_sostenible': 'Fondo Sostenible (ESG)',
    }
