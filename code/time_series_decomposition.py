"""
Time Series Decomposition: Trend, Seasonality, and Residuals
============================================================

This script builds a monthly aggregate REIT return series and decomposes it into:
- Trend
- Seasonality
- Residuals

Outputs:
- results/figures/time_series_decomposition_usdret.png
- results/figures/time_series_decomposition_usdret.pdf
- results/tables/time_series_decomposition_usdret.csv
- results/reports/Time_Series_Decomposition_Report.md
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root / 'code'))

from config_paths import RAW_DATA_DIR, FIGURES_DIR, TABLES_DIR, REPORTS_DIR


def build_monthly_series(df: pd.DataFrame, value_col: str = 'usdret') -> pd.Series:
    """Aggregate panel data into a monthly mean return time series."""
    temp = df[['date', value_col]].copy()
    temp['date'] = pd.to_datetime(temp['date'])
    temp = temp.dropna(subset=['date', value_col])

    monthly = (
        temp
        .groupby(temp['date'].dt.to_period('M'))[value_col]
        .mean()
        .to_timestamp()
        .sort_index()
    )
    monthly.index = pd.DatetimeIndex(monthly.index, freq='MS')
    monthly.name = f'monthly_mean_{value_col}'
    return monthly


def decompose_series(series: pd.Series, period: int = 12, model: str = 'additive'):
    """Run classical seasonal decomposition."""
    return seasonal_decompose(series, model=model, period=period, extrapolate_trend='freq')


def save_decomposition_plot(result, series_name: str):
    """Save decomposition plot to figures directory."""
    fig = result.plot()
    fig.set_size_inches(14, 10)
    fig.suptitle(f"Time Series Decomposition: {series_name}", fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout()

    png_path = FIGURES_DIR / 'time_series_decomposition_usdret.png'
    pdf_path = FIGURES_DIR / 'time_series_decomposition_usdret.pdf'
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    fig.savefig(pdf_path, bbox_inches='tight')
    plt.close(fig)

    return png_path, pdf_path


def save_components_table(result):
    """Save observed/trend/seasonal/resid components as a table."""
    components = pd.DataFrame({
        'observed': result.observed,
        'trend': result.trend,
        'seasonal': result.seasonal,
        'residual': result.resid,
    })
    out_path = TABLES_DIR / 'time_series_decomposition_usdret.csv'
    components.to_csv(out_path, index=True, index_label='date')
    return components, out_path


def write_report(series: pd.Series, components: pd.DataFrame, report_path):
    """Write a short markdown summary report."""
    valid = components.dropna()
    observed_var = valid['observed'].var()

    trend_share = valid['trend'].var() / observed_var if observed_var else 0
    seasonal_share = valid['seasonal'].var() / observed_var if observed_var else 0
    residual_share = valid['residual'].var() / observed_var if observed_var else 0

    report = f"""# Time Series Decomposition Report

## Dataset and Series
- Source: `data/raw/REIT_sample_2000_2024_All_Variables.csv`
- Series: monthly mean `usdret` (equal-weighted across firms each month)
- Sample period: {series.index.min().strftime('%Y-%m')} to {series.index.max().strftime('%Y-%m')}
- Number of monthly observations: {len(series)}

## Decomposition Setup
- Method: Classical seasonal decomposition (`seasonal_decompose`)
- Model: Additive
- Seasonal period: 12 months

## Variance Shares (approximate)
- Trend variance share: {trend_share:.2%}
- Seasonal variance share: {seasonal_share:.2%}
- Residual variance share: {residual_share:.2%}

## Output Files
- Figure (PNG): `results/figures/time_series_decomposition_usdret.png`
- Figure (PDF): `results/figures/time_series_decomposition_usdret.pdf`
- Components table: `results/tables/time_series_decomposition_usdret.csv`
"""

    report_path.write_text(report, encoding='utf-8')


def main():
    print("=" * 80)
    print("TIME SERIES DECOMPOSITION: TREND, SEASONALITY, RESIDUALS")
    print("=" * 80)

    input_path = RAW_DATA_DIR / 'REIT_sample_2000_2024_All_Variables.csv'
    print(f"\n1. Loading data: {input_path}")
    df = pd.read_csv(input_path)
    print(f"   Loaded {len(df):,} rows")

    print("\n2. Building monthly time series from `usdret`...")
    series = build_monthly_series(df, value_col='usdret')
    print(f"   Monthly observations: {len(series)}")
    print(f"   Date range: {series.index.min().date()} to {series.index.max().date()}")

    print("\n3. Running decomposition (period=12)...")
    decomposition = decompose_series(series, period=12, model='additive')

    print("\n4. Saving component table...")
    components, table_path = save_components_table(decomposition)
    print(f"   Saved: {table_path}")

    print("\n5. Saving decomposition figure...")
    png_path, pdf_path = save_decomposition_plot(decomposition, series.name)
    print(f"   Saved: {png_path}")
    print(f"   Saved: {pdf_path}")

    print("\n6. Writing report...")
    report_path = REPORTS_DIR / 'Time_Series_Decomposition_Report.md'
    write_report(series, components, report_path)
    print(f"   Saved: {report_path}")

    print("\n" + "=" * 80)
    print("DECOMPOSITION COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()