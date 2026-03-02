"""
REIT Sector Segmentation Analysis:
Identifying "Sensitive" vs. "Resilient" REIT Sectors

This script analyzes different REIT property types to determine which sectors
are more sensitive vs. resilient to market conditions, rate changes, and volatility.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add project root to path
project_root = Path.cwd().parent if 'code' in Path.cwd().parts else Path.cwd()
sys.path.append(str(project_root))

from config_paths import RAW_DATA_DIR, FIGURES_DIR, TABLES_DIR

# Property type mapping (based on CRSP REIT classification)
PROPERTY_TYPE_MAP = {
    1.0: 'Office',
    2.0: 'Industrial',
    3.0: 'Retail',
    4.0: 'Residential',
    5.0: 'Hotel/Lodging',
    8.0: 'Healthcare',
    9.0: 'Diversified',
    10.0: 'Self-Storage/Specialty'
}

def load_and_prepare_data():
    """Load REIT data and prepare for sector analysis"""
    df = pd.read_csv(RAW_DATA_DIR / "REIT_sample_2000_2024_All_Variables.csv")
    
    # Add sector names
    df['sector'] = df['ptype'].map(PROPERTY_TYPE_MAP)
    
    # Convert date
    df['date'] = pd.to_datetime(df['date'])
    
    return df

def calculate_sector_sensitivity_metrics(df):
    """Calculate comprehensive sensitivity metrics for each sector"""
    
    # Clean data for analysis
    analysis_cols = ['sector', 'usdret', 'beta', 'debt_at', 'roe', 'btm', 
                     'market_equity', 'assets', 'net_income']
    df_clean = df[analysis_cols].dropna()
    
    metrics_list = []
    
    for sector in sorted(df_clean['sector'].unique()):
        sector_data = df_clean[df_clean['sector'] == sector]
        
        metrics = {
            'Sector': sector,
            # Size metrics
            'N_Observations': len(sector_data),
            'N_Companies': df[df['sector'] == sector]['permno'].nunique(),
            'Avg_Market_Cap': sector_data['market_equity'].mean(),
            
            # Return characteristics
            'Avg_Return': sector_data['usdret'].mean(),
            'Return_Volatility': sector_data['usdret'].std(),
            'Return_Skewness': sector_data['usdret'].skew(),
            'Return_Kurtosis': sector_data['usdret'].kurtosis(),
            
            # Sensitivity metrics (higher = more sensitive)
            'Avg_Beta': sector_data['beta'].mean(),
            'Beta_Std': sector_data['beta'].std(),
            'Avg_Debt_Ratio': sector_data['debt_at'].mean(),
            'Debt_Volatility': sector_data['debt_at'].std(),
            
            # Profitability
            'Avg_ROE': sector_data['roe'].mean(),
            'ROE_Volatility': sector_data['roe'].std(),
            
            # Valuation
            'Avg_BTM': sector_data['btm'].mean(),
            'BTM_Std': sector_data['btm'].std(),
            
            # Composite sensitivity score (calculate later)
            'Sensitivity_Score': 0
        }
        
        metrics_list.append(metrics)
    
    metrics_df = pd.DataFrame(metrics_list)
    
    # Calculate composite sensitivity score
    # Higher score = more sensitive (normalized 0-100)
    sensitivity_components = [
        ('Return_Volatility', 1),  # Higher vol = more sensitive
        ('Avg_Beta', 1),  # Higher beta = more sensitive
        ('Avg_Debt_Ratio', 1),  # Higher debt = more sensitive
        ('ROE_Volatility', 1),  # Higher ROE vol = more sensitive
        ('Beta_Std', 1),  # Higher beta variation = more sensitive
    ]
    
    # Normalize each component to 0-1 scale
    for col, weight in sensitivity_components:
        if col in metrics_df.columns:
            normalized = (metrics_df[col] - metrics_df[col].min()) / (metrics_df[col].max() - metrics_df[col].min())
            metrics_df['Sensitivity_Score'] += normalized * weight
    
    # Scale to 0-100
    metrics_df['Sensitivity_Score'] = (metrics_df['Sensitivity_Score'] / 
                                        metrics_df['Sensitivity_Score'].max() * 100)
    
    # Classify sectors
    median_score = metrics_df['Sensitivity_Score'].median()
    metrics_df['Classification'] = metrics_df['Sensitivity_Score'].apply(
        lambda x: 'Sensitive' if x > median_score else 'Resilient'
    )
    
    return metrics_df

def calculate_crisis_period_performance(df):
    """Analyze sector performance during crisis periods"""
    
    crisis_periods = {
        'Financial Crisis': ('2007-10-01', '2009-03-31'),
        'COVID-19': ('2020-02-01', '2020-05-31'),
        'Rate Hiking (2022-23)': ('2022-03-01', '2023-06-30')
    }
    
    crisis_performance = []
    
    for crisis_name, (start, end) in crisis_periods.items():
        crisis_data = df[(df['date'] >= start) & (df['date'] <= end)]
        
        for sector in sorted(df['sector'].dropna().unique()):
            sector_crisis = crisis_data[crisis_data['sector'] == sector]
            
            if len(sector_crisis) > 0:
                crisis_performance.append({
                    'Crisis': crisis_name,
                    'Sector': sector,
                    'Avg_Return': sector_crisis['usdret'].mean(),
                    'Return_Volatility': sector_crisis['usdret'].std(),
                    'Max_Drawdown': sector_crisis['usdret'].min(),
                    'N_Obs': len(sector_crisis)
                })
    
    return pd.DataFrame(crisis_performance)

def plot_sector_sensitivity_dashboard(metrics_df, crisis_df):
    """Create comprehensive visualization dashboard"""
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Sort by sensitivity score
    metrics_sorted = metrics_df.sort_values('Sensitivity_Score')
    
    # Color mapping
    colors = metrics_sorted['Classification'].map({'Sensitive': '#E74C3C', 'Resilient': '#27AE60'})
    
    # 1. Sensitivity Score Bar Chart
    ax1 = fig.add_subplot(gs[0, :])
    bars = ax1.barh(metrics_sorted['Sector'], metrics_sorted['Sensitivity_Score'], color=colors)
    ax1.axvline(x=50, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax1.set_xlabel('Sensitivity Score (0=Resilient, 100=Sensitive)', fontsize=12, fontweight='bold')
    ax1.set_title('REIT Sector Sensitivity Ranking\nComposite Score Based on Volatility, Beta, Debt, and ROE Variation', 
                  fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Add score labels
    for i, (idx, row) in enumerate(metrics_sorted.iterrows()):
        ax1.text(row['Sensitivity_Score'] + 1, i, f"{row['Sensitivity_Score']:.1f}", 
                va='center', fontsize=9, fontweight='bold')
    
    # 2. Return vs Volatility Scatter
    ax2 = fig.add_subplot(gs[1, 0])
    scatter = ax2.scatter(metrics_df['Return_Volatility'], metrics_df['Avg_Return']*100,
                         c=metrics_df['Sensitivity_Score'], cmap='RdYlGn_r', s=200, alpha=0.7,
                         edgecolors='black', linewidth=1)
    
    for idx, row in metrics_df.iterrows():
        ax2.annotate(row['Sector'], (row['Return_Volatility'], row['Avg_Return']*100),
                    fontsize=8, ha='center', va='bottom')
    
    ax2.set_xlabel('Return Volatility (Std Dev)', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Average Return (%)', fontsize=10, fontweight='bold')
    ax2.set_title('Risk-Return Profile by Sector', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax2, label='Sensitivity Score')
    
    # 3. Beta Distribution
    ax3 = fig.add_subplot(gs[1, 1])
    metrics_sorted_beta = metrics_df.sort_values('Avg_Beta')
    bars = ax3.barh(metrics_sorted_beta['Sector'], metrics_sorted_beta['Avg_Beta'],
                   color=metrics_sorted_beta['Classification'].map({'Sensitive': '#E74C3C', 'Resilient': '#27AE60'}))
    ax3.axvline(x=1.0, color='gray', linestyle='--', linewidth=1, label='Market Beta=1.0')
    ax3.set_xlabel('Average Beta', fontsize=10, fontweight='bold')
    ax3.set_title('Market Sensitivity (Beta)', fontsize=11, fontweight='bold')
    ax3.legend()
    ax3.grid(axis='x', alpha=0.3)
    
    # 4. Debt Ratio Distribution
    ax4 = fig.add_subplot(gs[1, 2])
    metrics_sorted_debt = metrics_df.sort_values('Avg_Debt_Ratio')
    bars = ax4.barh(metrics_sorted_debt['Sector'], metrics_sorted_debt['Avg_Debt_Ratio'],
                   color=metrics_sorted_debt['Classification'].map({'Sensitive': '#E74C3C', 'Resilient': '#27AE60'}))
    ax4.set_xlabel('Average Debt Ratio', fontsize=10, fontweight='bold')
    ax4.set_title('Leverage Exposure', fontsize=11, fontweight='bold')
    ax4.grid(axis='x', alpha=0.3)
    
    # 5. Crisis Performance Heatmap
    ax5 = fig.add_subplot(gs[2, :])
    
    if len(crisis_df) > 0:
        crisis_pivot = crisis_df.pivot(index='Sector', columns='Crisis', values='Avg_Return')
        crisis_pivot = crisis_pivot * 100  # Convert to percentage
        
        sns.heatmap(crisis_pivot, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
                   ax=ax5, cbar_kws={'label': 'Average Return (%)'},
                   linewidths=0.5)
        ax5.set_title('Sector Performance During Crisis Periods\n(Average Monthly Returns %)', 
                     fontsize=11, fontweight='bold')
        ax5.set_xlabel('')
        ax5.set_ylabel('Sector', fontsize=10, fontweight='bold')
    
    plt.suptitle('REIT Sector Segmentation: Sensitive vs. Resilient Analysis', 
                fontsize=16, fontweight='bold', y=0.995)
    
    return fig

def main():
    print("="*80)
    print("REIT SECTOR SEGMENTATION ANALYSIS")
    print("="*80)
    
    # 1. Load data
    print("\n1. Loading and preparing data...")
    df = load_and_prepare_data()
    print(f"   Total observations: {len(df):,}")
    print(f"   Sectors identified: {df['sector'].nunique()}")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    
    # 2. Calculate sensitivity metrics
    print("\n2. Calculating sector sensitivity metrics...")
    metrics_df = calculate_sector_sensitivity_metrics(df)
    
    print("\n" + "="*80)
    print("SECTOR SENSITIVITY RANKINGS")
    print("="*80)
    
    display_cols = ['Sector', 'Classification', 'Sensitivity_Score', 'Avg_Return', 
                    'Return_Volatility', 'Avg_Beta', 'Avg_Debt_Ratio']
    print(metrics_df[display_cols].sort_values('Sensitivity_Score', ascending=False).to_string(index=False))
    
    # 3. Crisis period analysis
    print("\n3. Analyzing crisis period performance...")
    crisis_df = calculate_crisis_period_performance(df)
    
    # 4. Classification summary
    print("\n" + "="*80)
    print("CLASSIFICATION SUMMARY")
    print("="*80)
    
    sensitive = metrics_df[metrics_df['Classification'] == 'Sensitive']
    resilient = metrics_df[metrics_df['Classification'] == 'Resilient']
    
    print("\n🔴 SENSITIVE SECTORS (Higher volatility, higher beta, more debt exposure):")
    for _, row in sensitive.sort_values('Sensitivity_Score', ascending=False).iterrows():
        print(f"   • {row['Sector']:25} (Score: {row['Sensitivity_Score']:.1f}, Beta: {row['Avg_Beta']:.2f})")
    
    print("\n🟢  RESILIENT SECTORS (Lower volatility, defensive characteristics):")
    for _, row in resilient.sort_values('Sensitivity_Score').iterrows():
        print(f"   • {row['Sector']:25} (Score: {row['Sensitivity_Score']:.1f}, Beta: {row['Avg_Beta']:.2f})")
    
    # 5. Save results
    print("\n4. Saving results...")
    
    # Save metrics table
    metrics_file = TABLES_DIR / 'sector_sensitivity_metrics.csv'
    metrics_df.to_csv(metrics_file, index=False)
    print(f"   ✓ Metrics saved: {metrics_file}")
    
    # Save crisis performance
    crisis_file = TABLES_DIR / 'sector_crisis_performance.csv'
    crisis_df.to_csv(crisis_file, index=False)
    print(f"   ✓ Crisis analysis saved: {crisis_file}")
    
    # 6. Create visualizations
    print("\n5. Creating visualizations...")
    fig = plot_sector_sensitivity_dashboard(metrics_df, crisis_df)
    
    output_png = FIGURES_DIR / 'sector_segmentation_analysis.png'
    fig.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"   ✓ Dashboard saved: {output_png}")
    
    output_pdf = FIGURES_DIR / 'sector_segmentation_analysis.pdf'
    fig.savefig(output_pdf, bbox_inches='tight')
    print(f"   ✓ PDF saved: {output_pdf}")
    
    plt.close()
    
    # 7. Key insights
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)
    
    most_sensitive = metrics_df.loc[metrics_df['Sensitivity_Score'].idxmax()]
    most_resilient = metrics_df.loc[metrics_df['Sensitivity_Score'].idxmin()]
    
    print(f"\n📊 Most Sensitive Sector: {most_sensitive['Sector']}")
    print(f"   - Sensitivity Score: {most_sensitive['Sensitivity_Score']:.1f}/100")
    print(f"   - Average Beta: {most_sensitive['Avg_Beta']:.2f}")
    print(f"   - Return Volatility: {most_sensitive['Return_Volatility']:.4f}")
    print(f"   - Debt Ratio: {most_sensitive['Avg_Debt_Ratio']:.2f}")
    
    print(f"\n🛡️  Most Resilient Sector: {most_resilient['Sector']}")
    print(f"   - Sensitivity Score: {most_resilient['Sensitivity_Score']:.1f}/100")
    print(f"   - Average Beta: {most_resilient['Avg_Beta']:.2f}")
    print(f"   - Return Volatility: {most_resilient['Return_Volatility']:.4f}")
    print(f"   - Debt Ratio: {most_resilient['Avg_Debt_Ratio']:.2f}")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    
    return metrics_df, crisis_df

if __name__ == "__main__":
    metrics_df, crisis_df = main()
