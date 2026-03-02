# Summary Statistics by REIT and Time Period

## Dataset Overview
- Source: `data/raw/REIT_sample_2000_2024_All_Variables.csv`
- Observations: 48,019
- Unique REITs (`permno`): 369
- Time range: 1986 to 2024

## Grouped Outputs
- REIT-level summary: `results/tables/summary_stats_by_reit.csv`
- Year-level summary: `results/tables/summary_stats_by_year.csv`
- REIT-year summary: `results/tables/summary_stats_by_reit_year.csv`
- Decade-level summary: `results/tables/summary_stats_by_decade.csv`

## Visual Outputs
- Yearly trend figure (PNG): `results/figures/summary_stats_yearly_trends.png`
- Yearly trend figure (PDF): `results/figures/summary_stats_yearly_trends.pdf`

## Top 5 REITs by Average Return (`usdret_mean`)
  - permno 76249, ticker SZH: mean usdret = 0.0968
  - permno 24817, ticker AHR: mean usdret = 0.0874
  - permno 75040, ticker BPP: mean usdret = 0.0767
  - permno 67264, ticker BED: mean usdret = 0.0577
  - permno 80075, ticker CNT: mean usdret = 0.0571

## Notes
- Statistics include: `count`, `mean`, `std`, `min`, `median`, `max`
- Variables summarized: `usdret`, `market_equity`, `assets`, `sales`, `net_income`, `book_equity`, `debt_at`, `cash_at`, `ocf_at`, `roe`, `beta`, `btm`
