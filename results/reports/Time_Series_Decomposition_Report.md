# Time Series Decomposition Report

## Dataset and Series
- Source: `data/raw/REIT_sample_2000_2024_All_Variables.csv`
- Series: monthly mean `usdret` (equal-weighted across firms each month)
- Sample period: 1986-12 to 2024-12
- Number of monthly observations: 457

## Decomposition Setup
- Method: Classical seasonal decomposition (`seasonal_decompose`)
- Model: Additive
- Seasonal period: 12 months

## Variance Shares (approximate)
- Trend variance share: 8.00%
- Seasonal variance share: 3.71%
- Residual variance share: 88.24%

## Output Files
- Figure (PNG): `results/figures/time_series_decomposition_usdret.png`
- Figure (PDF): `results/figures/time_series_decomposition_usdret.pdf`
- Components table: `results/tables/time_series_decomposition_usdret.csv`
