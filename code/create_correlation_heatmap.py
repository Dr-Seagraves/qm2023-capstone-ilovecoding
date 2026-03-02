"""
Correlation Heatmap: Interest Rates vs REIT Returns
Creates a correlation heatmap analyzing relationships between REIT returns and financial variables
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

from config_paths import RAW_DATA_DIR, FIGURES_DIR

def main():
    print("="*80)
    print("CORRELATION ANALYSIS: REIT RETURNS AND FINANCIAL VARIABLES")
    print("="*80)
    
    # 1. Load data
    print("\n1. Loading data...")
    input_file = RAW_DATA_DIR / "REIT_sample_2000_2024_All_Variables.csv"
    df = pd.read_csv(input_file)
    print(f"   Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # 2. Select relevant numeric columns
    print("\n2. Selecting variables for analysis...")
    numeric_cols = ['usdret', 'market_equity', 'assets', 'sales', 'net_income', 
                    'book_equity', 'debt_at', 'cash_at', 'ocf_at', 'roe', 'btm', 'beta']
    
    available_cols = [col for col in numeric_cols if col in df.columns]
    print(f"   Variables: {', '.join(available_cols)}")
    
    # 3. Clean data
    print("\n3. Cleaning data...")
    df_analysis = df[available_cols].copy()
    rows_before = len(df_analysis)
    df_clean = df_analysis.dropna()
    rows_after = len(df_clean)
    print(f"   Rows before: {rows_before:,}")
    print(f"   Rows after: {rows_after:,}")
    print(f"   Rows removed: {rows_before - rows_after:,}")
    
    # 4. Calculate correlation matrix
    print("\n4. Computing correlation matrix...")
    correlation_matrix = df_clean.corr()
    print(f"   Matrix size: {correlation_matrix.shape[0]}×{correlation_matrix.shape[1]}")
    
    # Display correlations with returns
    if 'usdret' in correlation_matrix.columns:
        print("\n   Correlations with REIT Returns (usdret):")
        returns_corr = correlation_matrix['usdret'].sort_values(ascending=False)
        for var, corr in returns_corr.items():
            print(f"      {var:15s}: {corr:7.4f}")
    
    # 5. Create heatmap
    print("\n5. Generating correlation heatmap...")
    
    # Set style
    sns.set_style("whitegrid")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create heatmap
    sns.heatmap(correlation_matrix, 
                annot=True,  # Show correlation values
                fmt='.3f',   # Format to 3 decimal places
                cmap='RdBu_r',  # Red-Blue diverging colormap
                center=0,    # Center colormap at 0
                vmin=-1, vmax=1,  # Set range from -1 to 1
                square=True,  # Make cells square
                linewidths=0.5,  # Add gridlines
                cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"},
                ax=ax)
    
    # Customize the plot
    ax.set_title('Correlation Heatmap: REIT Returns and Financial Variables\n(2000-2024)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Variables', fontsize=12, fontweight='bold')
    ax.set_ylabel('Variables', fontsize=12, fontweight='bold')
    
    # Rotate labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Adjust layout
    plt.tight_layout()
    
    # 6. Save figure
    print("\n6. Saving heatmap...")
    
    # Save as PNG
    output_png = FIGURES_DIR / 'reit_correlation_heatmap.png'
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"   PNG saved: {output_png}")
    
    # Save as PDF
    output_pdf = FIGURES_DIR / 'reit_correlation_heatmap.pdf'
    plt.savefig(output_pdf, bbox_inches='tight')
    print(f"   PDF saved: {output_pdf}")
    
    # Display the plot
    plt.show()
    
    # Close after showing
    plt.close()
    
    # 7. Summary
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"Dataset: {len(df_clean):,} complete observations")
    print(f"Variables analyzed: {len(correlation_matrix.columns)}")
    print(f"Output directory: {FIGURES_DIR}")
    print("\n✓ Correlation heatmap generated successfully!")
    
    return correlation_matrix

if __name__ == "__main__":
    correlation_matrix = main()
