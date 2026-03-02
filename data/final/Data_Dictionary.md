# REIT Dataset Data Dictionary

**Dataset:** REIT_sample_2000_2024_All_Variables.csv  
**Time Period:** 2000-2024  
**Total Records:** 48,021  
**Total Variables:** 22  
**Data Sources:** CRSP, Compustat

---

## Identifier Variables

| Variable | Type | Description | Units |
|----------|------|-------------|-------|
| `permno` | Numeric | Permanent identifier for each REIT in CRSP database | ID Code |
| `ticker` | Text | Stock ticker symbol | Character |
| `comnam` | Text | Company/REIT name | Character |

---

## Classification Variables

| Variable | Type | Description | Units | Notes |
|----------|------|-------------|-------|-------|
| `rtype` | Numeric | REIT Type | Category | 1=Equity REIT; 2=Mortgage REIT; 3=Hybrid REIT |
| `ptype` | Numeric | Security property type | Category | Property type classification from CRSP |
| `psub` | Numeric | Property type subsector | Category | Detailed subsector classification |

---

## Time Variables

| Variable | Type | Description | Format | Notes |
|----------|------|-------------|--------|-------|
| `date` | Date | Observation date (last trading day of period) | YYYY-MM-DD | Primary date identifier |
| `caldt` | Date | Calendar date | YYYY-MM-DD | Matching date field |
| `ym` | Text | Year-Month identifier | YYYY-Mm | For time series grouping |

---

## Price & Market Variables

| Variable | Type | Description | Units | Source | Missing Values |
|----------|------|-------------|-------|--------|-----------------|
| `usdret` | Numeric | Total return in USD including dividends | Decimal ratio | CRSP | Some (~5%) |
| `usdprc` | Numeric | Share price in USD | USD per share | CRSP | Some (~3%) |
| `market_equity` | Numeric | Market capitalization | Millions USD | CRSP | Some (~5%) |

---

## Financial Statement Variables

| Variable | Type | Description | Units | Source | Missing Values |
|----------|------|-------------|-------|--------|-----------------|
| `assets` | Numeric | Total assets | Millions USD | Compustat | Some (~15%) |
| `sales` | Numeric | Total revenue/sales | Millions USD | Compustat | Some (~20%) |
| `net_income` | Numeric | Net income (loss) | Millions USD | Compustat | Some (~20%) |
| `book_equity` | Numeric | Book value of equity | Millions USD | Compustat | Some (~15%) |
| `debt_at` | Numeric | Total debt outstanding | Millions USD | Compustat | Some (~15%) |
| `cash_at` | Numeric | Cash and short-term investments | Millions USD | Compustat | Some (~15%) |
| `ocf_at` | Numeric | Operating cash flow | Millions USD | Compustat | Some (~15%) |

---

## Calculated/Derived Variables

| Variable | Type | Description | Formula | Missing Values |
|----------|------|-------------|---------|-----------------|
| `roe` | Numeric | Return on Equity | net_income / book_equity | Some (~20%) |
| `btm` | Numeric | Book-to-Market ratio | book_equity / market_equity | Some (~5%) |
| `beta` | Numeric | Market Beta (systematic risk) | Calculated from historical returns | Some (~10%) |

---

## Data Quality Notes

### Missing Values by Category
- **Price/Market Data:** 3-5% (CRSP source, generally reliable)
- **Returns:** ~5% (primarily early historical periods)
- **Accounting Data:** 15-20% (Compustat coverage varies by REIT)
- **Derived Metrics:** 5-20% (calculated from source variables)

### Key Characteristics
- **Time Coverage:** January 2000 - December 2024
- **REIT Types:** Primarily Equity REITs (rtype=1), with some Mortgage (2) and Hybrid (3)
- **Property Sectors:** Office, Retail, Residential, Industrial, Diversified, Specialty
- **Frequency:** Monthly observations (last trading day of month)
- **Currency:** All values in USD

### Data Cleaning Recommendations
1. Remove rows with missing `usdret` or `market_equity` for return analysis
2. Remove rows with missing `assets` for financial ratio analysis
3. Cross-check `date` and `ym` for consistency
4. Verify `market_equity` consistency across observation dates

---

## Usage Examples

### Loading the Data
```python
import pandas as pd
from config_paths import RAW_DATA_DIR

df = pd.read_csv(RAW_DATA_DIR / 'REIT_sample_2000_2024_All_Variables.csv')
```

### Filtering by REIT Type
```python
equity_reits = df[df['rtype'] == 1]  # Equity REITs only
mortgage_reits = df[df['rtype'] == 2]  # Mortgage REITs only
```

### Time Series Analysis
```python
# Group by year-month for aggregate analysis
monthly_stats = df.groupby('ym')[['usdret', 'roe', 'btm']].mean()
```

### Return Analysis
```python
# Calculate cumulative returns by REIT
returns_by_ticker = df.groupby('ticker')['usdret'].sum().sort_values()
```

---

## Related Documentation
- See `clean_reit_data.ipynb` for data cleaning procedures
- See project analysis scripts (`sector_segmentation_analysis.py`, etc.) for usage examples
- Run `python code/config_paths.py` to verify all data paths
