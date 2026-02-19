# REIT Analysis Panel: Data Dictionary

**Dataset:** REIT_analysis_panel.csv  
**Created:** February 19, 2026  
**Team:** ILOVECODING  
**Team Members:** Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez

---

## Dataset Overview

| Metric | Value |
|--------|-------|
| **Data Source** | REIT Master Sample (2000-2024) |
| **Number of Entities (REITs)** | 186 unique REITs |
| **Time Period** | 2000-2024 (25 years) |
| **Number of Observations** | 34,121 entity-month pairs |
| **Panel Structure** | Long format (REIT × Month) |
| **Frequency** | Monthly |

---

## Variable Definitions

### Identifiers

| Variable | Description | Type | Source | Unit |
|----------|-------------|------|--------|------|
| `entity_id` | Stock ticker symbol | String | CRSP | - |
| `entity_name` | Full company name | String | CRSP | - |
| `date_obs` | Observation date | Date | CRSP | YYYY-MM-DD |
| `year` | Calendar year | Integer | Derived | Year |
| `month` | Calendar month | Integer | Derived | 1-12 |
| `year_month` | Year-Month period | String | Derived | YYYY-Mm |

### Outcome Variables

| Variable | Description | Type | Source | Unit | Notes |
|----------|-------------|------|--------|------|-------|
| `return_pct` | Monthly stock return | Float | CRSP | % | USD-denominated total return; imputed with median (0.92%) |
| `price_usd` | Stock price at month-end | Float | CRSP | USD | Adjusted closing price; range: $0.75-$1,000+ |

### Firm Characteristics & Scale

| Variable | Description | Type | Source | Unit | Notes |
|----------|-------------|------|--------|------|-------|
| `market_cap_m` | Market capitalization | Float | CRSP | $ Millions | = Price × Shares Outstanding; filter: ≥$100M |
| `total_assets_m` | Total book assets | Float | Compustat | $ Millions | Balance sheet; imputed with median ($1,462M) |
| `revenue_m` | Total revenue/sales | Float | Compustat | $ Millions | Annual; imputed with median ($204.5M) |
| `net_income_m` | Net income | Float | Compustat | $ Millions | Annual; imputed with median ($23.2M) |
| `equity_book_m` | Book value of equity | Float | Compustat | $ Millions | Total assets - liabilities; imputed with median ($479M) |

### Capital Structure & Leverage

| Variable | Description | Type | Source | Unit | Notes |
|----------|-------------|------|--------|------|-------|
| `debt_to_assets` | Debt-to-assets ratio | Float | Compustat | Ratio | Total debt / Total assets; range: 0-1 |
| `cash_to_assets` | Cash-to-assets ratio | Float | Compustat | Ratio | Cash / Total assets; range: 0-1 |

### Profitability & Efficiency

| Variable | Description | Type | Source | Unit | Notes |
|----------|-------------|------|--------|------|-------|
| `ocf_to_assets` | Operating cash flow ratio | Float | Compustat | Ratio | OCF / Total assets; measure of operational efficiency |
| `return_on_equity` | Return on equity (ROE) | Float | Compustat | % | Net income / Book equity; measure of profitability |
| `book_to_market` | Book-to-market ratio | Float | Compustat/CRSP | Ratio | Book value / Market value; value factor |

### Risk & Market

| Variable | Description | Type | Source | Unit | Notes |
|----------|-------------|------|--------|------|-------|
| `beta` | Market beta | Float | CRSP | Coefficient | Systematic risk; imputed with rolling 60-month estimate |
| `rtype` | REIT type code | Float | Compustat | Code | 2.0 = Equity REIT; all observations filtered to 2.0 |

---

## Data Preparation Summary

### Cleaning Decisions

| Step | Action | Before | After | Justification |
|------|--------|--------|-------|---|
| **Missing Values** | Drop columns >50% missing | 22 columns | 22 columns | Preserved all columns; imputed <50% gaps with median |
| **Imputation** | Median imputation (numeric) | 16,500+ nulls | 0 nulls | Median robust to outliers; preserves sample size |
| **Outliers** | Winsorize at 5% tails | 63,615 outliers | Capped | Preserves data while reducing extreme influence |
| **Duplicates** | Drop exact duplicates | 0 found | 0 removed | No duplicate observations detected |
| **Filters** | Asset size (≥$100M) | 48,019 | 34,121 | Remove illiquid/small REITs; focus on material firms |
| **Date Range** | Keep 2000-2024 | - | 25 years | Sufficient data for panel analysis |

### Quality Metrics

- **Missing Keys:** 0 (no null entity_id or date_obs)
- **Duplicate Entity-Dates:** 0 (proper panel structure)
- **Missing Data (Final Set):** <0.1% (minimal imputation)
- **Rows Retained:** 71.1% of raw observations (13,898 removed by size filters)

---

## Merge & Integration Strategy

### Primary Data
- **REIT Master Sample (2000-2024)** — 186 REITs, 48,019 monthly observations
- **Variables:** Returns, prices, financial metrics, characteristics
- **Frequency:** Monthly
- **Form:** Panel (entity × month)

### Integration Notes
- Cleaned dataset ready for direct analysis
- Monthly frequency allows seasonal analysis
- 25-year span covers multiple market cycles
- No secondary data merges required (all from REIT Master)

---

## Sample Data Description

| Variable | N | Mean | Std Dev | Min | Max |
|----------|---|------|---------|-----|-----|
| `return_pct` | 34,121 | 0.85 | 18.3 | -99.9 | 95.5 |
| `price_usd` | 34,121 | 24.5 | 19.2 | 0.75 | 1,002 |
| `market_cap_m` | 34,121 | 4,251 | 6,983 | 100 | 87,450 |
| `total_assets_m` | 34,121 | 3,120 | 5,241 | 150 | 92,100 |
| `debt_to_assets` | 34,121 | 0.48 | 0.18 | 0.05 | 0.95 |
| `return_on_equity` | 34,121 | 0.067 | 0.152 | -0.85 | 0.92 |
| `beta` | 34,121 | 0.57 | 0.42 | 0.01 | 2.85 |

---

## Reproducibility

**Data Pipeline:**
```bash
# Step 1: Clean raw data
python code/fetch_REIT_data.py

# Step 2: Create analysis panel
python code/create_analysis_panel.py

# Output: data/final/REIT_analysis_panel.csv
```

**Dependencies:**
- pandas ≥2.0.0
- numpy ≥1.24.0
- scipy ≥1.10.0

**Verification:**
- Run `python code/config_paths.py` to verify directory structure
- Check `data/processed/REIT_sample_clean.csv` exists before running panel creation

---

## Ethical Considerations

### Data Privacy
- **Public data only:** All data from publicly-traded REITs (CRSP/Compustat)
- **No PII:** No personally identifiable information included
- **Aggregated:** Firm-level, not individual investor data

### Selection Bias
- **Survivorship bias:** Only includes REITs that existed during period; acquired/merged REITs excluded
- **Size bias:** Filter for ≥$100M assets exclusion introduces survivorship bias toward larger, more stable REITs
- **Market bias:** CRSP coverage skews toward larger exchanges (NYSE/NASDAQ)

### Data Loss
- **13,898 observations removed (28.9%):** Mostly from small REITs filtered out
- **Missing data imputation:** ~16,500 values replaced with median; assumes MCAR
- **Outlier winsorization:** 63,615 extreme values capped; may mask genuine extreme events

### Usage Recommendations
1. Report sample composition in empirical results
2. Run robustness checks with unfiltered data (if available)
3. Disclose winsorization procedure in methodology
4. Consider time-fixed effects to address unobserved REIT heterogeneity

---

## Notes for Analysis

- **Panel regression ready:** Proper long format (entity × time) with no missing keys
- **Time-series properties:** Monthly frequency allows for seasonal analysis and dynamic models
- **Market conditions:** 25-year span includes housing crisis (2008), recovery (2009-2019), pandemic (2020), rate hikes (2022-2024)
- **Future supplementary variables:** Consider adding macro indicators (Fed rates, Treasury yields, housing starts) for M2 exploratory analysis

---

**Last Updated:** February 19, 2026  
**Next Steps:** M2 Exploratory Data Analysis & Visualization
