"""
QM 2023 Capstone Project - Shared Utility Functions
Team: ILOVECODING

Centralized utilities for common operations used across M1 and M2 scripts.
"""

import pandas as pd
from config_paths import FINAL_DATA_DIR


def load_analysis_panel(filename: str = "REIT_analysis_panel.csv") -> pd.DataFrame:
    """
    Load the M1 analysis panel from final data directory.
    
    Parameters
    ----------
    filename : str
        Name of the analysis panel file (default: REIT_analysis_panel.csv)
    
    Returns
    -------
    pd.DataFrame
        Loaded and validated analysis panel with datetime columns converted
    """
    path = FINAL_DATA_DIR / filename
    
    if not path.exists():
        raise FileNotFoundError(f"Analysis panel not found: {path}")
    
    df = pd.read_csv(path)
    
    # Ensure date columns are datetime
    if 'date_obs' in df.columns:
        df['date_obs'] = pd.to_datetime(df['date_obs'])
    
    print(f"✓ Loaded: {len(df):,} rows × {len(df.columns)} columns")
    if 'year' in df.columns:
        print(f"  Date range: {df['year'].min():.0f} - {df['year'].max():.0f}")
    
    return df
