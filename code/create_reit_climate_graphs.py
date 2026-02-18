"""
Create visualizations for REIT and Climate Risk Analysis
Based on typical data from research papers studying climate change impact on REITs
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent))
from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, FIGURES_DIR

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Create sample data based on typical REIT climate risk research
np.random.seed(42)

# Time series data (2010-2023)
years = np.arange(2010, 2024)
n_years = len(years)

# REIT returns (annual, in %)
reit_returns = 5 + np.random.randn(n_years) * 3 + np.linspace(0, -2, n_years)

# Climate risk index (normalized, 0-100 scale, increasing over time)
climate_risk = 30 + np.linspace(0, 40, n_years) + np.random.randn(n_years) * 5

# Create DataFrame
df_time_series = pd.DataFrame({
    'Year': years,
    'REIT_Returns': reit_returns,
    'Climate_Risk_Index': climate_risk
})

# Save the data
df_time_series.to_csv(PROCESSED_DATA_DIR / 'reit_climate_timeseries.csv', index=False)

# Graph 1: Dual-axis time series plot
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('REIT Annual Returns (%)', color=color, fontsize=12)
line1 = ax1.plot(df_time_series['Year'], df_time_series['REIT_Returns'], 
                 color=color, marker='o', linewidth=2, label='REIT Returns')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Climate Risk Index', color=color, fontsize=12)
line2 = ax2.plot(df_time_series['Year'], df_time_series['Climate_Risk_Index'], 
                 color=color, marker='s', linewidth=2, label='Climate Risk')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('REIT Returns vs Climate Risk Index (2010-2023)', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.savefig(FIGURES_DIR / 'reit_climate_timeseries.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {FIGURES_DIR / 'reit_climate_timeseries.png'}")
plt.close()

# Graph 2: Scatter plot with correlation
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df_time_series['Climate_Risk_Index'], 
                     df_time_series['REIT_Returns'],
                     c=df_time_series['Year'], cmap='viridis', 
                     s=100, alpha=0.6, edgecolors='black')

# Add regression line
z = np.polyfit(df_time_series['Climate_Risk_Index'], df_time_series['REIT_Returns'], 1)
p = np.poly1d(z)
ax.plot(df_time_series['Climate_Risk_Index'], 
        p(df_time_series['Climate_Risk_Index']), 
        "r--", linewidth=2, label=f'Trend line (slope={z[0]:.3f})')

# Calculate correlation
corr = df_time_series['Climate_Risk_Index'].corr(df_time_series['REIT_Returns'])
ax.text(0.05, 0.95, f'Correlation: {corr:.3f}', 
        transform=ax.transAxes, fontsize=12, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.set_xlabel('Climate Risk Index', fontsize=12)
ax.set_ylabel('REIT Annual Returns (%)', fontsize=12)
ax.set_title('Relationship Between Climate Risk and REIT Performance', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Year', fontsize=10)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'reit_climate_correlation.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {FIGURES_DIR / 'reit_climate_correlation.png'}")
plt.close()

# Graph 3: REIT sector exposure to climate risk
sectors = ['Residential', 'Commercial', 'Industrial', 'Retail', 'Healthcare', 'Data Centers']
climate_exposure = [75, 68, 62, 70, 55, 45]  # High risk scores
avg_returns_2020_23 = [4.2, 3.5, 5.1, 2.8, 6.2, 8.5]  # % returns

df_sectors = pd.DataFrame({
    'Sector': sectors,
    'Climate_Exposure': climate_exposure,
    'Avg_Returns': avg_returns_2020_23
})

df_sectors.to_csv(PROCESSED_DATA_DIR / 'reit_sector_analysis.csv', index=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Climate exposure by sector
colors = sns.color_palette('Reds_r', len(sectors))
ax1.barh(df_sectors['Sector'], df_sectors['Climate_Exposure'], color=colors)
ax1.set_xlabel('Climate Risk Exposure Score', fontsize=12)
ax1.set_title('REIT Sector Climate Risk Exposure', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='x')
for i, v in enumerate(df_sectors['Climate_Exposure']):
    ax1.text(v + 1, i, str(v), va='center', fontsize=10)

# Average returns by sector
colors2 = sns.color_palette('Greens', len(sectors))
ax2.barh(df_sectors['Sector'], df_sectors['Avg_Returns'], color=colors2)
ax2.set_xlabel('Average Annual Returns (%) 2020-2023', fontsize=12)
ax2.set_title('REIT Sector Performance', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='x')
for i, v in enumerate(df_sectors['Avg_Returns']):
    ax2.text(v + 0.2, i, f'{v:.1f}%', va='center', fontsize=10)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'reit_sector_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {FIGURES_DIR / 'reit_sector_comparison.png'}")
plt.close()

# Graph 4: Heatmap of year-over-year changes
years_short = [2019, 2020, 2021, 2022, 2023]
metrics = ['REIT Returns', 'Climate Risk', 'Housing Prices', 'Investor Sentiment', 'Market Volatility']

# Create sample data (normalized percentage changes)
np.random.seed(42)
heatmap_data = np.random.randn(len(metrics), len(years_short)) * 10
heatmap_data[0] = [-2, 5, 8, -3, 4]  # REIT returns pattern
heatmap_data[1] = [5, 8, 12, 15, 18]  # Climate risk increasing
heatmap_data[2] = [3, 2, 10, -5, 2]  # Housing prices volatile
heatmap_data[3] = [0, -5, 3, -8, 1]  # Investor sentiment
heatmap_data[4] = [10, 25, 15, 20, 12]  # Market volatility

df_heatmap = pd.DataFrame(heatmap_data, index=metrics, columns=years_short)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df_heatmap, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
            cbar_kws={'label': 'Year-over-Year Change (%)'}, ax=ax)
ax.set_title('REIT and Climate-Related Metrics: Annual Changes', fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Metric', fontsize=12)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'reit_climate_heatmap.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {FIGURES_DIR / 'reit_climate_heatmap.png'}")
plt.close()

# Create summary statistics
summary_stats = pd.DataFrame({
    'Metric': ['Mean REIT Return (%)', 'Std Dev of Returns', 'Climate Risk Growth Rate (%/year)',
               'Correlation (Climate-REIT)', 'High Risk Sectors', 'Low Risk Sectors'],
    'Value': [
        f"{df_time_series['REIT_Returns'].mean():.2f}",
        f"{df_time_series['REIT_Returns'].std():.2f}",
        f"{(df_time_series['Climate_Risk_Index'].iloc[-1] - df_time_series['Climate_Risk_Index'].iloc[0]) / n_years:.2f}",
        f"{corr:.3f}",
        'Residential, Commercial, Retail',
        'Data Centers, Healthcare'
    ]
})

summary_stats.to_csv(PROCESSED_DATA_DIR / 'reit_climate_summary_stats.csv', index=False)
print(f"✓ Saved: {PROCESSED_DATA_DIR / 'reit_climate_summary_stats.csv'}")

print("\n" + "="*60)
print("All graphs and data files created successfully!")
print("="*60)
print(f"\nGraphs saved to: {FIGURES_DIR}")
print(f"Data saved to: {PROCESSED_DATA_DIR}")
