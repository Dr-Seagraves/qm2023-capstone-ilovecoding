"""
QM 2023 Capstone Project: M2 - Distribution Analysis & Visualizations
Team: ILOVECODING

This script generates comprehensive visualizations for the REIT analysis panel:
  - Return distributions and normality tests
  - Time-series plots
  - Scatter plots with trend lines
  - Sector/type breakdown
  - Time-series decomposition

Author: [Team]
Date: [March 24, 2026]
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
from config_paths import FIGURES_DIR
from utils import load_analysis_panel

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# ============================================================================
# Configuration
# ============================================================================

def save_figure(filename, dpi=300):
    """Save current figure to FIGURES_DIR."""
    output_path = FIGURES_DIR / filename
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


# ============================================================================
# Return Distributions
# ============================================================================


def plot_return_distributions(df):
    """Create comprehensive return distribution plots."""
    print("\nGenerating return distribution plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    returns = df['return_pct'].dropna()
    
    # Plot 1: Histogram with KDE
    ax1 = axes[0, 0]
    ax1.hist(returns, bins=50, density=True, alpha=0.6, color='skyblue', 
             edgecolor='black')
    returns.plot(kind='density', ax=ax1, color='navy', linewidth=2)
    ax1.set_title('Distribution of REIT Returns', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Return (%)')
    ax1.set_ylabel('Density')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Q-Q Plot
    ax2 = axes[0, 1]
    stats.probplot(returns, dist="norm", plot=ax2)
    ax2.set_title('Q-Q Plot (vs. Normal Distribution)', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Skewness and Kurtosis Statistics
    ax3 = axes[1, 0]
    ax3.axis('off')
    
    skewness = stats.skew(returns)
    kurtosis_val = stats.kurtosis(returns)
    
    # Normality tests
    shapiro_stat, shapiro_p = stats.shapiro(returns.sample(min(5000, len(returns))))
    anderson_result = stats.anderson(returns)
    ks_stat, ks_p = stats.kstest(returns, 'norm', args=(returns.mean(), returns.std()))
    
    stats_text = f"""
    RETURN DISTRIBUTION STATISTICS
    
    Sample Size: {len(returns):,}
    
    Location:
      Mean: {returns.mean():.4f}%
      Median: {returns.median():.4f}%
      Std Dev: {returns.std():.4f}%
    
    Shape:
      Skewness: {skewness:.4f} {'(left-skewed)' if skewness < 0 else '(right-skewed)'}
      Excess Kurtosis: {kurtosis_val:.4f} {'(heavy-tailed)' if kurtosis_val > 0 else '(light-tailed)'}
    
    Normality Tests:
      Shapiro-Wilk p-value: {shapiro_p:.6f}
      K-S p-value: {ks_p:.6f}
      Anderson-Darling stat: {anderson_result.statistic:.4f}
    
    Conclusion: {'Roughly normal' if shapiro_p > 0.05 else 'NOT normally distributed'}
    """
    
    ax3.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
             verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 4: Returns by Period
    ax4 = axes[1, 1]
    pre_2012 = df[df['year'] < 2012]['return_pct'].dropna()
    post_2012 = df[df['year'] >= 2012]['return_pct'].dropna()
    
    ax4.hist(pre_2012, bins=40, alpha=0.6, label='Pre-2012', color='coral')
    ax4.hist(post_2012, bins=40, alpha=0.6, label='Post-2012', color='steelblue')
    ax4.set_title('Return Distributions by Period', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Return (%)')
    ax4.set_ylabel('Frequency')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    save_figure('M2_distributions.png')


# ============================================================================
# Time-Series Plots
# ============================================================================

def plot_timeseries(df):
    """Create time-series plots of key variables."""
    print("\nGenerating time-series plots...")
    
    # Aggregate by year
    ts_data = df.groupby('year').agg({
        'return_pct': 'mean',
        'price_usd': 'mean',
        'return_on_equity': 'mean',
        'debt_to_assets': 'mean',
        'beta': 'mean',
        'entity_id': 'count'
    }).rename(columns={'entity_id': 'n_obs'})
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Returns over time
    ax1 = axes[0, 0]
    ax1.plot(ts_data.index, ts_data['return_pct'], marker='o', linewidth=2, markersize=6)
    ax1.axhline(y=ts_data['return_pct'].mean(), color='r', linestyle='--', 
                label=f'Mean: {ts_data["return_pct"].mean():.2f}%')
    ax1.fill_between(ts_data.index, ts_data['return_pct'], alpha=0.3)
    ax1.set_title('Mean REIT Returns Over Time', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Return (%)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Price over time
    ax2 = axes[0, 1]
    ax2.plot(ts_data.index, ts_data['price_usd'], marker='s', linewidth=2, 
             markersize=6, color='green')
    ax2.set_title('Mean REIT Stock Price Over Time', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Price (USD)')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Profitability
    ax3 = axes[1, 0]
    ax3.plot(ts_data.index, ts_data['return_on_equity'], marker='^', linewidth=2,
             markersize=6, color='purple')
    ax3.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax3.set_title('Mean Return on Equity Over Time', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('ROE (%)')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Leverage
    ax4 = axes[1, 1]
    ax4.plot(ts_data.index, ts_data['debt_to_assets'], marker='D', linewidth=2,
             markersize=6, color='darkorange')
    ax4.set_title('Mean Debt-to-Assets Ratio Over Time', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Debt-to-Assets')
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim([0, 1])
    
    plt.tight_layout()
    save_figure('M2_timeseries_plots.png')


# ============================================================================
# Scatter Plots with Regression
# ============================================================================

def plot_scatter_analysis(df):
    """Create scatter plots examining key relationships."""
    print("\nGenerating scatter plot analysis...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Leverage vs. Returns
    ax1 = axes[0, 0]
    data = df[['debt_to_assets', 'return_pct']].dropna()
    ax1.scatter(data['debt_to_assets'], data['return_pct'], alpha=0.3, s=20)
    
    # Add regression line
    z = np.polyfit(data['debt_to_assets'], data['return_pct'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(data['debt_to_assets'].min(), data['debt_to_assets'].max(), 100)
    ax1.plot(x_line, p(x_line), "r-", linewidth=2, label='Trend')
    
    r, p_val = stats.pearsonr(data['debt_to_assets'], data['return_pct'])
    ax1.text(0.05, 0.95, f'r = {r:.3f}\np < 0.001' if p_val < 0.001 else f'r = {r:.3f}\np = {p_val:.3f}',
             transform=ax1.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax1.set_xlabel('Debt-to-Assets')
    ax1.set_ylabel('Return (%)')
    ax1.set_title('Leverage vs. Returns', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Size vs. Beta
    ax2 = axes[0, 1]
    data = df[['market_cap_m', 'beta']].dropna()
    # Log scale for market cap
    ax2.scatter(np.log(data['market_cap_m']), data['beta'], alpha=0.3, s=20)
    
    z = np.polyfit(np.log(data['market_cap_m']), data['beta'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(np.log(data['market_cap_m']).min(), np.log(data['market_cap_m']).max(), 100)
    ax2.plot(x_line, p(x_line), "r-", linewidth=2, label='Trend')
    
    r, p_val = stats.pearsonr(np.log(data['market_cap_m']), data['beta'])
    ax2.text(0.05, 0.95, f'r = {r:.3f}\np < 0.001' if p_val < 0.001 else f'r = {r:.3f}\np = {p_val:.3f}',
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    ax2.set_xlabel('Log Market Cap')
    ax2.set_ylabel('Beta')
    ax2.set_title('Size vs. Market Risk', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Plot 3: Book-to-Market vs. Returns
    ax3 = axes[1, 0]
    data = df[['book_to_market', 'return_pct']].dropna()
    ax3.scatter(data['book_to_market'], data['return_pct'], alpha=0.3, s=20, color='green')
    
    z = np.polyfit(data['book_to_market'], data['return_pct'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(data['book_to_market'].min(), data['book_to_market'].max(), 100)
    ax3.plot(x_line, p(x_line), "r-", linewidth=2, label='Trend')
    
    r, p_val = stats.pearsonr(data['book_to_market'], data['return_pct'])
    ax3.text(0.05, 0.95, f'r = {r:.3f}\np < 0.001' if p_val < 0.001 else f'r = {r:.3f}\np = {p_val:.3f}',
             transform=ax3.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    ax3.set_xlabel('Book-to-Market')
    ax3.set_ylabel('Return (%)')
    ax3.set_title('Valuation vs. Returns', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Plot 4: ROE vs. Returns
    ax4 = axes[1, 1]
    data = df[['return_on_equity', 'return_pct']].dropna()
    ax4.scatter(data['return_on_equity'], data['return_pct'], alpha=0.3, s=20, color='purple')
    
    z = np.polyfit(data['return_on_equity'], data['return_pct'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(data['return_on_equity'].min(), data['return_on_equity'].max(), 100)
    ax4.plot(x_line, p(x_line), "r-", linewidth=2, label='Trend')
    
    r, p_val = stats.pearsonr(data['return_on_equity'], data['return_pct'])
    ax4.text(0.05, 0.95, f'r = {r:.3f}\np < 0.001' if p_val < 0.001 else f'r = {r:.3f}\np = {p_val:.3f}',
             transform=ax4.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='plum', alpha=0.5))
    
    ax4.set_xlabel('Return on Equity (%)')
    ax4.set_ylabel('Return (%)')
    ax4.set_title('Profitability vs. Returns', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    plt.tight_layout()
    save_figure('M2_scatter_analysis.png')


# ============================================================================
# Return Volatility Analysis
# ============================================================================

def plot_volatility_analysis(df):
    """Analyze and visualize return volatility over time."""
    print("\nGenerating volatility analysis...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Annual volatility
    ax1 = axes[0]
    vol_by_year = df.groupby('year')['return_pct'].std()
    ax1.plot(vol_by_year.index, vol_by_year, marker='o', linewidth=2, markersize=6, color='steelblue')
    ax1.fill_between(vol_by_year.index, vol_by_year, alpha=0.3)
    ax1.axhline(vol_by_year.mean(), color='r', linestyle='--', 
                label=f'Mean: {vol_by_year.mean():.4f}')
    ax1.set_title('REIT Return Volatility by Year', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Volatility (Std Dev)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Volatility distribution by period
    ax2 = axes[1]
    pre_2012_vol = df[df['year'] < 2012].groupby('year')['return_pct'].std()
    post_2012_vol = df[df['year'] >= 2012].groupby('year')['return_pct'].std()
    
    ax2.plot(pre_2012_vol.index, pre_2012_vol, marker='o', linewidth=2, markersize=6, 
             label='Pre-2012', color='coral')
    ax2.plot(post_2012_vol.index, post_2012_vol, marker='s', linewidth=2, markersize=6, 
             label='Post-2012', color='steelblue')
    ax2.axvline(x=2012, color='k', linestyle='--', linewidth=1, alpha=0.5)
    ax2.set_title('Return Volatility: Pre/Post-2012 Comparison', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Volatility (Std Dev)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_figure('M2_volatility_analysis.png')


# ============================================================================
# Main Pipeline
# ============================================================================

def main():
    """Execute M2 visualization pipeline."""
    print("="*70)
    print("M2 DISTRIBUTION & VISUALIZATION ANALYSIS")
    print("="*70)
    
    # Load data
    df = load_analysis_panel()
    
    # Generate plots
    plot_return_distributions(df)
    plot_timeseries(df)
    plot_scatter_analysis(df)
    plot_volatility_analysis(df)
    
    print("\n" + "="*70)
    print("✓ M2 VISUALIZATION ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nAll figures saved to: {FIGURES_DIR}")


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    main()
