# Fund Selector Tool
# Módulos para selección y análisis de fondos de inversión

from .data_processing import load_and_clean_data, clean_percentage, clean_currency
from .filters import apply_filters, get_filter_options
from .scoring import calculate_fund_score, get_preset_weights, PRESET_PROFILES
from .visualizations import (
    plot_risk_return_scatter,
    plot_top_funds_comparison,
    plot_fund_radar,
    plot_fees_comparison,
    create_fund_summary_table
)

__version__ = "1.0.0"
