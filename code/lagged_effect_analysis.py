"""
Lagged Effect Analysis: Interest Rate Changes vs REIT Returns
==============================================================
This script analyzes how changes in financial variables (and potentially interest rates)
affect REIT returns over different time lags.

Note: To include actual interest rate data, merge with Federal Reserve data:
- Federal Funds Rate
- 10-Year Treasury Yield
- Mortgage rates
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config_paths import RAW_DATA_DIR, FIGURES_DIR, TABLES_DIR

def prepare_time_series_data(df):
    """Prepare data for time series analysis"""
    # Convert date columns to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['ym'] = pd.to_datetime(df['ym'].str.replace('m', '-'))
    
    # Sort by company and date
    df = df.sort_values(['permno', 'date'])
    
    return df

def create_lagged_variables(df, variable, max_lag=12):
    """Create lagged versions of a variable for each company"""
    df = df.copy()
    
    # Create lags within each company group
    for lag in range(1, max_lag + 1):
        df[f'{variable}_lag{lag}'] = df.groupby('permno')[variable].shift(lag)
    
    return df

def calculate_lagged_correlations(df, target_var='usdret', predictor_var='debt_at', max_lag=12):
    """Calculate correlations between target and lagged versions of predictor"""
    correlations = []
    sample_sizes = []
    
    # Current period (lag 0)
    mask = df[[target_var, predictor_var]].notna().all(axis=1)
    if mask.sum() > 0:
        corr = df.loc[mask, target_var].corr(df.loc[mask, predictor_var])
        correlations.append(corr)
        sample_sizes.append(mask.sum())
    else:
        correlations.append(np.nan)
        sample_sizes.append(0)
    
    # Lagged periods
    for lag in range(1, max_lag + 1):
        lag_col = f'{predictor_var}_lag{lag}'
        if lag_col in df.columns:
            mask = df[[target_var, lag_col]].notna().all(axis=1)
            if mask.sum() > 0:
                corr = df.loc[mask, target_var].corr(df.loc[mask, lag_col])
                correlations.append(corr)
                sample_sizes.append(mask.sum())
            else:
                correlations.append(np.nan)
                sample_sizes.append(0)
        else:
            correlations.append(np.nan)
            sample_sizes.append(0)
    
    results = pd.DataFrame({
        'lag': range(max_lag + 1),
        'correlation': correlations,
        'sample_size': sample_sizes
    })
    
    return results

def plot_lagged_effects(lag_results_dict, title="Lagged Effect Analysis"):
    """Plot lagged correlations for multiple variables"""
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: All variables together
    ax1 = axes[0]
    for var_name, results in lag_results_dict.items():
        ax1.plot(results['lag'], results['correlation'], 
                marker='o', linewidth=2, markersize=6, label=var_name, alpha=0.8)
    
    ax1.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax1.set_xlabel('Lag Period (months)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Correlation with Current REIT Returns', fontsize=12, fontweight='bold')
    ax1.set_title(f'{title}\nCorrelation between Lagged Variables and Current Returns', 
                  fontsize=14, fontweight='bold')
    ax1.legend(loc='best', frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(range(0, max([r['lag'].max() for r in lag_results_dict.values()]) + 1))
    
    # Plot 2: Individual heatmap-style visualization
    ax2 = axes[1]
    
    # Prepare data for heatmap
    lag_matrix = pd.DataFrame({
        var_name: results.set_index('lag')['correlation']
        for var_name, results in lag_results_dict.items()
    }).T
    
    sns.heatmap(lag_matrix, annot=True, fmt='.3f', cmap='RdBu_r', 
                center=0, vmin=-0.3, vmax=0.3,
                cbar_kws={'label': 'Correlation Coefficient'},
                linewidths=0.5, ax=ax2)
    
    ax2.set_xlabel('Lag Period (months)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Variable', fontsize=12, fontweight='bold')
    ax2.set_title('Lagged Correlation Heatmap', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig

def analyze_decay_pattern(lag_results):
    """Analyze the decay pattern of the lagged effect"""
    # Find peak correlation
    peak_idx = lag_results['correlation'].abs().idxmax()
    peak_lag = lag_results.loc[peak_idx, 'lag']
    peak_corr = lag_results.loc[peak_idx, 'correlation']
    
    # Calculate half-life (lag where effect drops to 50% of peak)
    half_effect = peak_corr * 0.5
    half_life = None
    
    for idx, row in lag_results.iterrows():
        if row['lag'] > peak_lag:
            if abs(row['correlation']) <= abs(half_effect):
                half_life = row['lag']
                break
    
    return {
        'peak_lag': peak_lag,
        'peak_correlation': peak_corr,
        'half_life': half_life
    }

def main():
    print("="*80)
    print("LAGGED EFFECT ANALYSIS: FINANCIAL VARIABLES vs REIT RETURNS")
    print("="*80)
    
    # 1. Load data
    print("\n1. Loading data...")
    input_file = RAW_DATA_DIR / "REIT_sample_2000_2024_All_Variables.csv"
    df = pd.read_csv(input_file)
    print(f"   Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # 2. Prepare time series data
    print("\n2. Preparing time series data...")
    df = prepare_time_series_data(df)
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    
    # 3. Select variables for analysis
    # Note: In a real analysis, this would include interest rate variables
    variables_to_analyze = {
        'beta': 'Market Beta (Interest Rate Sensitivity Proxy)',
        'debt_at': 'Debt Ratio (Interest Rate Exposure)',
        'roe': 'Return on Equity',
        'btm': 'Book-to-Market Ratio'
    }
    
    print("\n3. Creating lagged variables...")
    max_lag = 12  # Analyze up to 12 months of lag
    
    for var in variables_to_analyze.keys():
        print(f"   Creating lags for {var}...")
        df = create_lagged_variables(df, var, max_lag=max_lag)
    
    # 4. Calculate lagged correlations
    print("\n4. Calculating lagged correlations...")
    lag_results = {}
    
    for var, description in variables_to_analyze.items():
        print(f"   Analyzing {var}...")
        results = calculate_lagged_correlations(df, target_var='usdret', 
                                                predictor_var=var, max_lag=max_lag)
        lag_results[var] = results
        
        # Analyze decay pattern
        decay = analyze_decay_pattern(results)
        print(f"      Peak at lag {decay['peak_lag']}: {decay['peak_correlation']:.4f}")
        if decay['half_life']:
            print(f"      Half-life: ~{decay['half_life']} months")
    
    # 5. Create comprehensive summary table
    print("\n5. Creating summary table...")
    summary_data = []
    
    for var, results in lag_results.items():
        decay = analyze_decay_pattern(results)
        summary_data.append({
            'Variable': var,
            'Peak Lag (months)': decay['peak_lag'],
            'Peak Correlation': decay['peak_correlation'],
            'Half-Life (months)': decay['half_life'] if decay['half_life'] else 'N/A',
            'Lag 0': results.loc[results['lag']==0, 'correlation'].values[0],
            'Lag 3': results.loc[results['lag']==3, 'correlation'].values[0],
            'Lag 6': results.loc[results['lag']==6, 'correlation'].values[0],
            'Lag 12': results.loc[results['lag']==12, 'correlation'].values[0]
        })
    
    summary_df = pd.DataFrame(summary_data)
    print("\nLagged Effect Summary:")
    print(summary_df.to_string(index=False))
    
    # Save summary table
    summary_file = TABLES_DIR / 'lagged_effect_summary.csv'
    summary_df.to_csv(summary_file, index=False)
    print(f"\nSummary saved to: {summary_file}")
    
    # 6. Create detailed correlation table
    print("\n6. Creating detailed lagged correlation table...")
    detailed_corr = pd.DataFrame({
        var: results.set_index('lag')['correlation']
        for var, results in lag_results.items()
    })
    
    detailed_file = TABLES_DIR / 'lagged_correlations_detailed.csv'
    detailed_corr.to_csv(detailed_file)
    print(f"   Detailed correlations saved to: {detailed_file}")
    
    # 7. Visualize lagged effects
    print("\n7. Creating visualizations...")
    fig = plot_lagged_effects(lag_results, 
                              title="Lagged Effect Analysis: Financial Variables vs REIT Returns")
    
    # Save figure
    output_png = FIGURES_DIR / 'lagged_effect_analysis.png'
    fig.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"   Figure saved: {output_png}")
    
    output_pdf = FIGURES_DIR / 'lagged_effect_analysis.pdf'
    fig.savefig(output_pdf, bbox_inches='tight')
    print(f"   PDF saved: {output_pdf}")
    
    plt.close()
    
    # 8. Summary and interpretation
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nKEY FINDINGS:")
    print("-" * 80)
    
    for var, results in lag_results.items():
        decay = analyze_decay_pattern(results)
        print(f"\n{variables_to_analyze[var]} ({var}):")
        print(f"  • Peak effect at lag {decay['peak_lag']} months: {decay['peak_correlation']:.4f}")
        if decay['half_life']:
            print(f"  • Effect diminishes to 50% after ~{decay['half_life']} months")
        else:
            print(f"  • Effect persists beyond 12 months")
    
    print("\n" + "="*80)
    print("NOTE: To include actual interest rate data:")
    print("  1. Download Federal Reserve data (FRED)")
    print("  2. Merge by date with REIT dataset")
    print("  3. Run same analysis with interest rate variables")
    print("  4. Common rates to analyze: Fed Funds, 10Y Treasury, Mortgage rates")
    print("="*80)
    
    return lag_results, summary_df

if __name__ == "__main__":
    lag_results, summary_df = main()
