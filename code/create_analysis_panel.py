"""
QM 2023 Capstone Project: M1 - Create Analysis Panel
Team: [ILOVECODING]
Members: [Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez]

This script creates the final analysis-ready panel dataset from cleaned REIT data.
Converts to long format (Entity × Time), handles merges, and generates summary statistics.

Output: data/final/REIT_analysis_panel.csv

Author: [Ashley]
Date: [2/19/2026]
"""

import pandas as pd
import numpy as np
from pathlib import Path
from config_paths import PROCESSED_DATA_DIR, FINAL_DATA_DIR

# ============================================================================
# Configuration
# ============================================================================

CLEANED_DATA = "REIT_sample_clean.csv"
FINAL_OUTPUT = "REIT_analysis_panel.csv"

# ============================================================================
# Load Cleaned Data
# ============================================================================

def load_cleaned_data(filename=CLEANED_DATA):
    """Load the cleaned REIT data."""
    path = PROCESSED_DATA_DIR / filename
    df = pd.read_csv(path)
    print(f"✓ Loaded cleaned data: {len(df):,} rows × {len(df.columns)} columns")
    return df

# ============================================================================
# Create Analysis Panel
# ============================================================================

def create_analysis_panel(df):
    """
    Transform cleaned data into analysis-ready panel format.
    
    Panel structure: Entity × Time (one row per REIT per period)
    Ensures proper sorting and no missing keys
    """
    print("\nCreating Analysis Panel...")
    
    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by entity and time
    df = df.sort_values(['ticker', 'date']).reset_index(drop=True)
    
    # Create year and month columns for analysis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Rename for clarity
    df = df.rename(columns={
        'ticker': 'entity_id',
        'comnam': 'entity_name',
        'date': 'date_obs',
        'usdret': 'return_pct',
        'usdprc': 'price_usd',
        'market_equity': 'market_cap_m',
        'assets': 'total_assets_m',
        'sales': 'revenue_m',
        'net_income': 'net_income_m',
        'book_equity': 'equity_book_m',
        'debt_at': 'debt_to_assets',
        'cash_at': 'cash_to_assets',
        'ocf_at': 'ocf_to_assets',
        'roe': 'return_on_equity',
        'btm': 'book_to_market'
    })
    
    # Select key columns for analysis
    key_cols = [
        'entity_id', 'entity_name', 'date_obs', 'year', 'month', 'year_month',
        'return_pct', 'price_usd', 'market_cap_m', 'total_assets_m', 'revenue_m',
        'net_income_m', 'equity_book_m', 'debt_to_assets', 'cash_to_assets',
        'ocf_to_assets', 'return_on_equity', 'book_to_market', 'beta', 'rtype'
    ]
    
    df = df[[col for col in key_cols if col in df.columns]]
    
    print(f"  Panel structure: {len(df.groupby('entity_id'))} entities × {len(df.groupby('year'))} years")
    print(f"  Observations: {len(df):,} rows")
    
    return df

# ============================================================================
# Verify Panel Structure
# ============================================================================

def verify_panel(df):
    """Verify panel structure and data quality."""
    print("\nVerifying Panel Structure...")
    
    # Check for missing keys
    if df[['entity_id', 'date_obs']].isnull().any().any():
        print("  ⚠ WARNING: Missing entity_id or date_obs")
    else:
        print("  ✓ No missing entity IDs or dates")
    
    # Check for duplicates
    dup_check = df[['entity_id', 'date_obs']].duplicated().sum()
    if dup_check == 0:
        print("  ✓ No duplicate entity-date combinations")
    else:
        print(f"  ⚠ {dup_check} duplicate entity-date pairs found")
    
    # Summary statistics
    n_entities = df['entity_id'].nunique()
    n_years = df['year'].nunique()
    n_obs = len(df)
    
    print(f"\n  Dataset Structure:")
    print(f"    Entities: {n_entities}")
    print(f"    Years: {n_years} ({df['year'].min()}-{df['year'].max()})")
    print(f"    Observations: {n_obs:,}")
    print(f"    Variables: {len(df.columns)}")
    
    return df

# ============================================================================
# Save Final Dataset
# ============================================================================

def save_final_panel(df, filename=FINAL_OUTPUT):
    """Save analysis-ready panel to CSV."""
    output_path = FINAL_DATA_DIR / filename
    
    print(f"\nSaving Final Analysis Panel...")
    df.to_csv(output_path, index=False)
    
    print(f"  Output: {output_path}")
    print(f"  Size: {len(df):,} rows × {len(df.columns)} columns")
    print(f"  File size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    return output_path

# ============================================================================
# Generate Summary Statistics
# ============================================================================

def generate_summary_stats(df):
    """Generate summary statistics for data quality report."""
    print("\nSummary Statistics:")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    summary = df[numeric_cols].describe()
    
    print(f"\n{summary.to_string()}")
    
    return summary

# ============================================================================
# Main Pipeline
# ============================================================================

def main():
    """Execute panel creation pipeline."""
    print("=" * 70)
    print("REIT Analysis Panel Creation")
    print("=" * 70)
    
    # Load cleaned data
    df = load_cleaned_data()
    
    # Create analysis panel
    df = create_analysis_panel(df)
    
    # Verify structure
    df = verify_panel(df)
    
    # Generate summary stats
    summary = generate_summary_stats(df)
    
    # Save final dataset
    output_path = save_final_panel(df)
    
    print("\n" + "=" * 70)
    print("✓ Analysis Panel Created Successfully")
    print("=" * 70)
    
    return df, output_path

# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    df_panel, path = main()
