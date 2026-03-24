"""
QM 2023 Capstone Project: M2 - Exploratory Data Analysis
Team: ILOVECODING
Members: Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez

This script generates comprehensive summary statistics and descriptive analyses
for the REIT analysis panel from M1.

Outputs:
  - Summary statistics by year, sector, and size
  - Descriptive statistics table (manuscript-ready format)
  - Correlation matrices with significance tests
  - Data for preliminary hypothesis development

Author: [Team]
Date: [March 24, 2026]
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# Import centralized path configuration and shared utilities
from config_paths import FINAL_DATA_DIR, TABLES_DIR
from utils import load_analysis_panel

# ============================================================================
# Configuration
# ============================================================================

ANALYSIS_PANEL = "REIT_analysis_panel.csv"
OUTPUT_SUMMARY_STATS = "M2_summary_statistics.csv"
OUTPUT_DESC_STATS = "M2_descriptive_stats_table.csv"
OUTPUT_CORRELATION = "M2_correlation_matrix.csv"


# ============================================================================
# Summary Statistics by Year
# ============================================================================


def summary_stats_by_year(df):
    """Generate annual summary statistics."""
    print("\n" + "="*70)
    print("SUMMARY STATISTICS BY YEAR")
    print("="*70)
    
    key_vars = [
        'return_pct', 'price_usd', 'market_cap_m', 'total_assets_m',
        'revenue_m', 'net_income_m', 'equity_book_m', 'debt_to_assets',
        'cash_to_assets', 'return_on_equity', 'book_to_market', 'beta'
    ]
    
    # Filter to available columns
    key_vars = [col for col in key_vars if col in df.columns]
    
    summary_by_year = df.groupby('year')[key_vars].agg([
        'count', 'mean', 'std', 'min', 'median', 'max'
    ])
    
    print(f"\nAnnual statistics ({len(df['year'].unique())} years)")
    print(f"  Variables: {len(key_vars)}")
    
    return summary_by_year


# ============================================================================
# Summary Statistics by Size Quartile
# ============================================================================

def summary_stats_by_size_quartile(df):
    """Generate statistics by market cap quartile."""
    print("\n" + "="*70)
    print("SUMMARY STATISTICS BY SIZE QUARTILE (Market Cap)")
    print("="*70)
    
    # Create size quartiles
    df_temp = df.copy()
    df_temp['size_quartile'] = pd.qcut(
        df_temp['market_cap_m'].replace(0, np.nan),
        q=4,
        labels=['Q1 (Small)', 'Q2', 'Q3', 'Q4 (Large)'],
        duplicates='drop'
    )
    
    key_vars = [
        'return_pct', 'market_cap_m', 'total_assets_m',
        'debt_to_assets', 'return_on_equity', 'beta'
    ]
    
    key_vars = [col for col in key_vars if col in df_temp.columns]
    
    summary_by_size = df_temp.groupby('size_quartile')[key_vars].agg([
        'count', 'mean', 'std', 'min', 'median', 'max'
    ])
    
    print(f"Size quartiles defined by market cap")
    print(f"  {summary_by_size.index.tolist()}")
    
    return summary_by_size


# ============================================================================
# Descriptive Statistics Table (Manuscript Format)
# ============================================================================

def create_descriptive_stats_table(df):
    """Generate publication-ready descriptive statistics table."""
    print("\n" + "="*70)
    print("DESCRIPTIVE STATISTICS TABLE (Manuscript Format)")
    print("="*70)
    
    key_vars = [
        'return_pct',
        'price_usd',
        'market_cap_m',
        'total_assets_m',
        'debt_to_assets',
        'cash_to_assets',
        'return_on_equity',
        'book_to_market',
        'beta'
    ]
    
    key_vars = [col for col in key_vars if col in df.columns]
    
    # Full sample
    stats_table = []
    
    for var in key_vars:
        # Remove NaN and outliers for reasonable summary
        data = df[var].dropna()
        
        row = {
            'Variable': var,
            'N': len(data),
            'Mean': data.mean(),
            'Std Dev': data.std(),
            'Min': data.min(),
            'Q1': data.quantile(0.25),
            'Median': data.quantile(0.50),
            'Q3': data.quantile(0.75),
            'Max': data.max()
        }
        stats_table.append(row)
    
    stats_df = pd.DataFrame(stats_table)
    
    print(f"\nFull Sample Statistics ({len(df):,} observations)")
    print(f"Variables: {len(key_vars)}")
    print(f"\n{stats_df.to_string(index=False)}")
    
    return stats_df


# ============================================================================
# Correlation Analysis
# ============================================================================

def correlation_analysis(df):
    """Compute correlation matrices with significance tests."""
    print("\n" + "="*70)
    print("CORRELATION ANALYSIS")
    print("="*70)
    
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Key variables for correlation
    key_vars = [
        'return_pct',
        'debt_to_assets',
        'return_on_equity',
        'market_cap_m',
        'book_to_market',
        'beta',
        'total_assets_m'
    ]
    
    key_vars = [col for col in key_vars if col in numeric_cols]
    
    # Select data
    corr_data = df[key_vars].dropna()
    
    # Pearson correlation
    pearson_corr = corr_data.corr(method='pearson')
    
    # Spearman correlation (rank)
    spearman_corr = corr_data.corr(method='spearman')
    
    print(f"\nCorrelation matrix based on {len(corr_data):,} observations")
    print(f"Variables: {len(key_vars)}")
    
    # Compute p-values for Pearson correlation
    pvalues = pd.DataFrame(
        np.zeros_like(pearson_corr),
        index=pearson_corr.index,
        columns=pearson_corr.columns
    )
    
    for i in range(len(key_vars)):
        for j in range(i+1, len(key_vars)):
            col_i, col_j = key_vars[i], key_vars[j]
            r, p = stats.pearsonr(corr_data[col_i], corr_data[col_j])
            pvalues.loc[col_i, col_j] = p
            pvalues.loc[col_j, col_i] = p
    
    print("\nPearson Correlation Matrix:")
    print(pearson_corr.round(3).to_string())
    
    print("\nSpearman Rank Correlation Matrix:")
    print(spearman_corr.round(3).to_string())
    
    # Identify significant correlations
    print("\nSignificant Correlations (p < 0.05):")
    sig_corrs = []
    for i in range(len(key_vars)):
        for j in range(i+1, len(key_vars)):
            col_i, col_j = key_vars[i], key_vars[j]
            if pvalues.loc[col_i, col_j] < 0.05:
                sig_corrs.append({
                    'Var1': col_i,
                    'Var2': col_j,
                    'Correlation': pearson_corr.loc[col_i, col_j],
                    'P-value': pvalues.loc[col_i, col_j]
                })
    
    if sig_corrs:
        sig_df = pd.DataFrame(sig_corrs).sort_values('Correlation', 
                                                      key=abs, ascending=False)
        print(sig_df.to_string(index=False))
    else:
        print("(No significant correlations found)")
    
    return pearson_corr, spearman_corr, pvalues


# ============================================================================
# Time Period Analysis (Pre/Post 2012)
# ============================================================================

def compare_periods(df):
    """Compare statistics pre- and post-2012 (climate policy shift)."""
    print("\n" + "="*70)
    print("PRE/POST-2012 ANALYSIS (Climate Policy Shift)")
    print("="*70)
    
    pre_2012 = df[df['year'] < 2012]
    post_2012 = df[df['year'] >= 2012]
    
    print(f"\nPre-2012: {len(pre_2012):,} obs ({len(pre_2012['year'].unique())} years)")
    print(f"Post-2012: {len(post_2012):,} obs ({len(post_2012['year'].unique())} years)")
    
    key_vars = ['return_pct', 'debt_to_assets', 'return_on_equity', 'beta']
    key_vars = [col for col in key_vars if col in df.columns]
    
    comparison_table = []
    
    for var in key_vars:
        pre_mean = pre_2012[var].mean()
        post_mean = post_2012[var].mean()
        diff = post_mean - pre_mean
        
        # T-test
        t_stat, p_value = stats.ttest_ind(
            post_2012[var].dropna(),
            pre_2012[var].dropna()
        )
        
        comparison_table.append({
            'Variable': var,
            'Pre-2012 Mean': pre_mean,
            'Post-2012 Mean': post_mean,
            'Difference': diff,
            'T-statistic': t_stat,
            'P-value': p_value
        })
    
    comparison_df = pd.DataFrame(comparison_table)
    
    print(f"\n{comparison_df.to_string(index=False)}")
    
    return comparison_df


# ============================================================================
# Export Results
# ============================================================================

def export_tables(summary_stats_year, desc_stats_table, pearson_corr):
    """Export summary statistics and correlations to CSV."""
    
    print("\n" + "="*70)
    print("EXPORTING RESULTS")
    print("="*70)
    
    # Export summary stats by year
    summary_stats_year.to_csv(TABLES_DIR / OUTPUT_SUMMARY_STATS)
    print(f"✓ Exported: {OUTPUT_SUMMARY_STATS}")
    
    # Export descriptive stats
    desc_stats_table.to_csv(TABLES_DIR / OUTPUT_DESC_STATS, index=False)
    print(f"✓ Exported: {OUTPUT_DESC_STATS}")
    
    # Export correlation matrix
    pearson_corr.to_csv(TABLES_DIR / OUTPUT_CORRELATION)
    print(f"✓ Exported: {OUTPUT_CORRELATION}")
    
    print(f"\nAll outputs saved to: {TABLES_DIR}")


# ============================================================================
# Main Pipeline
# ============================================================================

def main():
    """Execute the M2 exploratory analysis pipeline."""
    print("="*70)
    print("M2 EXPLORATORY DATA ANALYSIS")
    print("="*70)
    
    # Load data
    df = load_analysis_panel()
    
    # Summary statistics by year
    summary_by_year = summary_stats_by_year(df)
    
    # Summary statistics by size
    summary_by_size = summary_stats_by_size_quartile(df)
    
    # Descriptive statistics (manuscript format)
    desc_stats = create_descriptive_stats_table(df)
    
    # Correlation analysis
    pearson_corr, spearman_corr, pvalues = correlation_analysis(df)
    
    # Pre/Post 2012 comparison
    period_comparison = compare_periods(df)
    
    # Export results
    export_tables(summary_by_year, desc_stats, pearson_corr)
    
    print("\n" + "="*70)
    print("✓ M2 EXPLORATORY ANALYSIS COMPLETE")
    print("="*70)
    
    return df, summary_by_year, summary_by_size, desc_stats, pearson_corr


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    results = main()
