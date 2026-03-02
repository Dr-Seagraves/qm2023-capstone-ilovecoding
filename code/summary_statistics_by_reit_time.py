"""
Summary Statistics by REIT and Time Period
==========================================

Creates grouped summary statistics from the REIT panel for:
- REIT-level (full sample)
- Year-level (all REITs)
- REIT-year level
- Decade-level (all REITs)

Outputs:
- results/tables/summary_stats_by_reit.csv
- results/tables/summary_stats_by_year.csv
- results/tables/summary_stats_by_reit_year.csv
- results/tables/summary_stats_by_decade.csv
- results/reports/Summary_Statistics_REIT_Time_Report.md
"""

from pathlib import Path
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root / 'code'))

from config_paths import RAW_DATA_DIR, TABLES_DIR, REPORTS_DIR, FIGURES_DIR


VARIABLES_FOR_SUMMARY = [
    'usdret', 'market_equity', 'assets', 'sales', 'net_income',
    'book_equity', 'debt_at', 'cash_at', 'ocf_at', 'roe', 'beta', 'btm'
]


def load_data() -> pd.DataFrame:
    """Load raw REIT data and create time features."""
    df = pd.read_csv(RAW_DATA_DIR / 'REIT_sample_2000_2024_All_Variables.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['decade'] = (df['year'] // 10) * 10
    df['decade_label'] = df['decade'].astype(str) + 's'
    return df


def grouped_summary(df: pd.DataFrame, group_cols, value_cols) -> pd.DataFrame:
    """Return count/mean/std/min/median/max for each value variable by group."""
    available_cols = [col for col in value_cols if col in df.columns]

    agg_spec = {
        col: ['count', 'mean', 'std', 'min', 'median', 'max']
        for col in available_cols
    }

    summary = df.groupby(group_cols, dropna=False).agg(agg_spec)
    summary.columns = [f"{var}_{stat}" for var, stat in summary.columns]
    summary = summary.reset_index()
    return summary


def build_reit_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Create one representative ticker/name per permno."""
    labels = (
        df.sort_values('date')
        .dropna(subset=['permno'])
        .groupby('permno', as_index=False)
        .agg(
            ticker=('ticker', lambda s: s.dropna().iloc[-1] if not s.dropna().empty else pd.NA),
            comnam=('comnam', lambda s: s.dropna().iloc[-1] if not s.dropna().empty else pd.NA),
        )
    )
    return labels


def save_yearly_trend_figure(year_stats: pd.DataFrame):
    """Create compact yearly trend visualizations from year-level summary stats."""
    plot_df = year_stats.sort_values('year').copy()

    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    axes[0].plot(plot_df['year'], plot_df['usdret_mean'], color='#1f77b4', linewidth=2)
    axes[0].axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    axes[0].set_ylabel('Mean usdret', fontweight='bold')
    axes[0].set_title('Yearly Mean REIT Return', fontweight='bold')
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(plot_df['year'], plot_df['usdret_std'], color='#d62728', linewidth=2)
    axes[1].set_ylabel('Std usdret', fontweight='bold')
    axes[1].set_title('Yearly Return Volatility', fontweight='bold')
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(plot_df['year'], plot_df['beta_mean'], color='#2ca02c', linewidth=2)
    axes[2].axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    axes[2].set_ylabel('Mean beta', fontweight='bold')
    axes[2].set_xlabel('Year', fontweight='bold')
    axes[2].set_title('Yearly Average Market Beta', fontweight='bold')
    axes[2].grid(True, alpha=0.3)

    plt.suptitle('REIT Summary Statistics: Yearly Trends', fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()

    png_path = FIGURES_DIR / 'summary_stats_yearly_trends.png'
    pdf_path = FIGURES_DIR / 'summary_stats_yearly_trends.pdf'
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    fig.savefig(pdf_path, bbox_inches='tight')
    plt.close(fig)

    return png_path, pdf_path


def write_report(df: pd.DataFrame, reit_stats: pd.DataFrame, year_stats: pd.DataFrame, path: Path):
    """Write markdown summary of generated statistics."""
    n_rows = len(df)
    n_reits = df['permno'].nunique()
    year_min = int(df['year'].min())
    year_max = int(df['year'].max())

    top_reits = reit_stats.sort_values('usdret_mean', ascending=False).head(5)
    top_reits_lines = "\n".join([
        f"  - permno {int(row['permno'])}, ticker {row['ticker']}: mean usdret = {row['usdret_mean']:.4f}"
        for _, row in top_reits.iterrows()
    ])

    report = f"""# Summary Statistics by REIT and Time Period

## Dataset Overview
- Source: `data/raw/REIT_sample_2000_2024_All_Variables.csv`
- Observations: {n_rows:,}
- Unique REITs (`permno`): {n_reits}
- Time range: {year_min} to {year_max}

## Grouped Outputs
- REIT-level summary: `results/tables/summary_stats_by_reit.csv`
- Year-level summary: `results/tables/summary_stats_by_year.csv`
- REIT-year summary: `results/tables/summary_stats_by_reit_year.csv`
- Decade-level summary: `results/tables/summary_stats_by_decade.csv`

## Visual Outputs
- Yearly trend figure (PNG): `results/figures/summary_stats_yearly_trends.png`
- Yearly trend figure (PDF): `results/figures/summary_stats_yearly_trends.pdf`

## Top 5 REITs by Average Return (`usdret_mean`)
{top_reits_lines}

## Notes
- Statistics include: `count`, `mean`, `std`, `min`, `median`, `max`
- Variables summarized: {', '.join([f'`{v}`' for v in VARIABLES_FOR_SUMMARY])}
"""

    path.write_text(report, encoding='utf-8')


def main():
    print('=' * 80)
    print('SUMMARY STATISTICS BY REIT AND TIME PERIOD')
    print('=' * 80)

    print('\n1. Loading data...')
    df = load_data()
    print(f"   Loaded {len(df):,} rows")
    print(f"   REITs: {df['permno'].nunique()} | Years: {df['year'].min()}-{df['year'].max()}")

    print('\n2. Computing grouped summaries...')
    reit_labels = build_reit_labels(df)

    reit_stats = grouped_summary(df, ['permno'], VARIABLES_FOR_SUMMARY)
    year_stats = grouped_summary(df, ['year'], VARIABLES_FOR_SUMMARY)
    reit_year_stats = grouped_summary(df, ['permno', 'year'], VARIABLES_FOR_SUMMARY)
    decade_stats = grouped_summary(df, ['decade_label'], VARIABLES_FOR_SUMMARY)

    reit_stats = reit_stats[reit_stats['usdret_count'] > 0].merge(reit_labels, on='permno', how='left')
    reit_stats = reit_stats[['permno', 'ticker', 'comnam'] + [c for c in reit_stats.columns if c not in ['permno', 'ticker', 'comnam']]]

    reit_year_stats = reit_year_stats[reit_year_stats['usdret_count'] > 0].merge(
        reit_labels[['permno', 'ticker']], on='permno', how='left'
    )
    reit_year_stats = reit_year_stats[['permno', 'ticker', 'year'] + [c for c in reit_year_stats.columns if c not in ['permno', 'ticker', 'year']]]

    print('\n3. Saving tables...')
    reit_path = TABLES_DIR / 'summary_stats_by_reit.csv'
    year_path = TABLES_DIR / 'summary_stats_by_year.csv'
    reit_year_path = TABLES_DIR / 'summary_stats_by_reit_year.csv'
    decade_path = TABLES_DIR / 'summary_stats_by_decade.csv'

    reit_stats.to_csv(reit_path, index=False)
    year_stats.to_csv(year_path, index=False)
    reit_year_stats.to_csv(reit_year_path, index=False)
    decade_stats.to_csv(decade_path, index=False)

    print(f'   Saved: {reit_path}')
    print(f'   Saved: {year_path}')
    print(f'   Saved: {reit_year_path}')
    print(f'   Saved: {decade_path}')

    print('\n4. Creating yearly trend figure...')
    fig_png_path, fig_pdf_path = save_yearly_trend_figure(year_stats)
    print(f'   Saved: {fig_png_path}')
    print(f'   Saved: {fig_pdf_path}')

    print('\n5. Writing report...')
    report_path = REPORTS_DIR / 'Summary_Statistics_REIT_Time_Report.md'
    write_report(df, reit_stats, year_stats, report_path)
    print(f'   Saved: {report_path}')

    print('\n' + '=' * 80)
    print('SUMMARY STATISTICS COMPLETE')
    print('=' * 80)


if __name__ == '__main__':
    main()