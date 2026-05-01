[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22634753&assignment_repo_type=AssignmentRepo)

# QM 2023 Capstone Project: Climate Risk & REIT Market Impact

**Team:** ILOVECODING  
**Members:** Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez  
**Course:** Statistics II: Data Analytics (QM 2023)  
**Duration:** Semester-long capstone project

## Research Overview

**Research Questions:**
1. How do climate change risks impact Real Estate Investment Trusts (REITs)?
2. How does climate change affect predicted housing rates in the United States?
3. Can we identify a correlation between climate risk metrics and REIT performance?

**Key Insight:**
By analyzing public and investor reactions to climate change and examining its impact on the stock market, we compare those trends to REIT performance data to determine whether a climate-REIT correlation exists. If confirmed, findings can project how climate change may influence the future housing market and identify which generations are most affected.

**Methodological Foundation:** [Skiadopoulos et al. - Dissecting Climate Risks: Are they Reflected in Stock Prices?](https://ssrn.com/abstract=3795964)
- Uses Latent Dirichlet Allocation (LDA) for textual analysis of climate news
- Constructs market-wide climate risk factors
- Tests whether climate risks are priced in equity markets
- Distinguishes between physical risks and transition risks

## Project Structure

```
qm2023-capstone-ilovecoding/
├── README.md                           # This file - project documentation
├── M1_SUBMISSION_CHECKLIST.md          # M1 milestone deliverables & verification
├── requirements.txt                    # Python dependencies
├── climate_and_stocks.pdf              # Research methodology reference
│
├── code/                               # Python scripts for data processing
│   ├── config_paths.py                 # Centralized path management
│   ├── fetch_REIT_data.py              # REIT data cleaning pipeline
│   ├── fetch_Climate_data.py           # Climate/stocks data cleaning template
│   ├── create_analysis_panel.py        # Transform to analysis-ready panel
│   ├── create_reit_climate_graphs.py   # Generate visualizations
│   └── visualize_summary_stats.py      # Summary statistics visualization
│
├── data/
│   ├── raw/                            # Original raw data (read-only)
│   │   ├── REIT_sample_2000_2024_All_Variables.csv
│   │   ├── project_metadata.csv
│   │   ├── project_details.json
│   │   └── research_summary.csv
│   │
│   ├── processed/                      # Cleaned intermediate data
│   │   ├── REIT_sample_clean.csv       # M1 Output: Cleaned REIT data
│   │   ├── reit_climate_timeseries.csv # Time series analysis data
│   │   ├── reit_climate_summary_stats.csv
│   │   └── reit_sector_analysis.csv
│   │
│   └── final/                          # Analysis-ready final datasets
│       ├── REIT_analysis_panel.csv     # M1 Output: Final analysis panel
│       └── data_dictionary.md          # M1 Output: Variable definitions
│
├── results/
│   ├── figures/                        # Generated visualizations
│   │   ├── reit_climate_timeseries.png
│   │   ├── reit_climate_correlation.png
│   │   ├── reit_sector_comparison.png
│   │   ├── reit_climate_heatmap.png
│   │   └── reit_climate_summary_visualization.png
│   │
│   ├── tables/                         # Regression tables & summary stats
│   │   ├── M2_summary_statistics.csv
│   │   ├── M2_descriptive_stats_table.csv
│   │   └── M2_correlation_matrix.csv
│   │
│   └── reports/                        # Milestone documentation
│       ├── M1_data_quality_report.md   # M1 Output: Data cleaning justification
│       ├── AI_AUDIT_APPENDIX.md        # M1 Output: AI usage disclosure
│       ├── M2_findings_report.md       # M2 Output: EDA findings
│       └── M2_SUBMISSION_CHECKLIST.md  # M2 Output: deliverable checklist
│
└── tests/                              # Autograding test suite
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip or conda for package management

### Installation

1. **Clone/Pull Repository:**
   ```bash
   git clone <repository-url>
   cd qm2023-capstone-ilovecoding
   ```

2. **Create Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Project Structure:**
   ```bash
   python code/config_paths.py
   ```
   Expected output: Table of all project paths and verification that directories exist.

### Data Preparation & Processing

Run the data pipeline in this order:

#### Step 1: Clean Raw REIT Data
```bash
python code/fetch_REIT_data.py
```
**Output:** `data/processed/REIT_sample_clean.csv` (34,121 rows × 23 columns)
- Handles missing values, outliers, and duplicates
- Applies REIT-specific filters (minimum asset size, valid returns, REIT type)
- Runs in ~30 seconds

#### Step 2: Create Analysis Panel
```bash
python code/create_analysis_panel.py
```
**Output:** `data/final/REIT_analysis_panel.csv` (34,121 rows × 20 columns)
- Transforms cleaned data to long format (Entity × Time)
- Renames variables for clarity
- Validates panel structure
- Ready for regression analysis

#### Step 3: Generate Climate Analysis Data (Template)
```bash
python code/fetch_Climate_data.py
```
**Note:** This script is a template with alternative approaches (Z-score vs. Winsorization).
Requires climate/stocks raw data file.

#### Step 4: Create Visualizations
```bash
python code/create_reit_climate_graphs.py
```
**Outputs:** 5 PNG figures in `results/figures/`

#### Step 5: Visualize Summary Statistics
```bash
python code/visualize_summary_stats.py
```
**Output:** Summary statistics visualization

### Milestone 3 & 4: Econometric Models & Investment Recommendations

#### Step 1: Estimate Fixed Effects & Difference-in-Differences Models
```bash
python code/M3_econometric_models.py
```
**Outputs:**
- `results/tables/M3_regression_table.csv` — Raw regression results
- `results/tables/M3_diagnostics_summary.csv` — Model diagnostics (R², F-stat, VIF)
- `results/tables/M3_robustness_checks.csv` — Robustness specifications
- `results/figures/M3_diagnostics.png` — Residual diagnostics & Q-Q plots

#### Step 2: Format Results for Publication
```bash
python code/format_regression_tables.py
```
**Output:** `results/tables/M3_REGRESSION_TABLE_FORMATTED.csv` — Academic-style regression table

#### Step 3: Review Investment Recommendations
See: `results/reports/Final_Investment_Memo.md` (18 pages, full analysis)
Or: `results/reports/EXECUTIVE_SUMMARY_ONE_PAGE.md` (executive summary)

---

## Key Findings (M3/M4 Final Results)

### 🎯 Main Result: Beta Drives Returns; Leverage Does Not

| Finding | Magnitude | Confidence | Implication |
|---------|-----------|-----------|-------------|
| **Beta Effect** | 61 bps/month (~7.3% annualized) | ✅ Very High | Market-sensitive REITs consistently outperform. Deploy beta-targeting strategies. |
| **Leverage Effect** | ~1 bps/month (statistically zero) | ✅ High | Leverage does NOT predict REIT returns. Ignore leverage-based tilts. |
| **Policy Shock (DiD)** | 20 bps post-2015 (not significant, 95% CI: [-15, 55]) | 🟡 Moderate | No evidence that Fed rate hikes differentially hurt high-leverage REITs. |

### 📊 Data & Sample

- **Dataset:** 34,121 monthly observations from 273 unique REITs
- **Time Period:** January 2000 – December 2024 (25 years, 299 months)
- **Panel Structure:** Unbalanced; spans 2008 crisis, 2020 pandemic, multiple Fed cycles
- **Fixed Effects:** Entity + Time (controls for REIT quality and aggregate shocks)
- **Clustering:** Entity-level (accounts for within-REIT correlation)

### 📈 Models Estimated

**Model A: Two-Way Fixed Effects (Primary)**
- Tests whether lagged leverage & beta predict monthly returns
- Controls for unobserved REIT characteristics & time-invariant shocks
- Result: Leverage insignificant; Beta robust (61 bps, p<0.001)

**Model B: Difference-in-Differences (Policy Shock)**
- Compares large-cap vs. small-cap REITs before/after 2015 Fed rate shift
- Tests whether monetary policy reveals leverage effects
- Result: No differential effect; treatment coefficient = +20 bps, p=0.247

---

## Quick Links for Decision-Makers

| Need | Resource | Format |
|------|----------|--------|
| **10-min overview** | [Executive Summary (1 page)](results/reports/EXECUTIVE_SUMMARY_ONE_PAGE.md) | Markdown |
| **Full analysis + recommendations** | [Final Investment Memo (18 pages)](results/reports/Final_Investment_Memo.md) | Markdown |
| **Regression results** | [Regression Table (formatted)](results/tables/M3_REGRESSION_TABLE_FORMATTED.csv) | CSV |
| **Diagnostic plots** | [Model Diagnostics](results/figures/M3_diagnostics.png) | PNG |
| **Team contributions** | [Individual Addendums](results/reports/Individual_Addendum_*.md) | Markdown |
| **Results summary** | [Technical Summary](results/RESULTS_SUMMARY.md) | Markdown |

---

## Reproducibility & Verification

### Reproduce All Results (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run full analysis pipeline
python code/M3_econometric_models.py
python code/format_regression_tables.py

# 3. Verify outputs
ls -lh results/tables/M3_REGRESSION_TABLE_FORMATTED.csv
ls -lh results/figures/M3_diagnostics.png

# Expected: Both files exist and are non-empty
```

### Key Outputs Checklist

- ✅ `results/tables/M3_REGRESSION_TABLE_FORMATTED.csv` — Regression coefficients (should have 8 rows: Leverage Lag 1–3, Beta, Treatment, Post2015, Treatment×Post)
- ✅ `results/figures/M3_diagnostics.png` — Residual plots (should show heteroskedasticity and Q-Q comparison)
- ✅ `results/reports/Final_Investment_Memo.md` — Investment memo (should be ~21–22 pages, ~711 lines)
- ✅ `results/reports/EXECUTIVE_SUMMARY_ONE_PAGE.md` — 1-page summary (for decision-makers)

### Data Integrity Checks

Run these to verify data hasn't been corrupted:

```bash
# Check final analysis panel dimensions
python -c "import pandas as pd; df = pd.read_csv('data/final/REIT_analysis_panel.csv'); print(f'Shape: {df.shape}'); print(f'Columns: {list(df.columns)[:5]}...')"
# Expected: (34121, 20)

# Check regression input has no NaNs in key variables
python -c "import pandas as pd; df = pd.read_csv('data/final/REIT_analysis_panel.csv'); print(f'Missing in return_pct: {df[\"return_pct\"].isna().sum()}'); print(f'Missing in leverage: {df[\"leverage_lag2\"].isna().sum()}')"
# Expected: Both should be 0 or very small
```

### Regression Results Validation

Expected coefficient magnitudes from `M3_REGRESSION_TABLE_FORMATTED.csv`:

| Variable | Expected Coefficient | Expected p-value | Your Result |
|----------|---------------------|-----------------|-------------|
| Leverage_lag2 | ~0.007 | ~0.077 | _______ |
| Beta | ~0.0061 | <0.001 | _______ |
| Treatment×Post2015 | ~0.002 | ~0.247 | _______ |

**If coefficients match within ±0.0005, reproducibility verified ✓**

---

## File Descriptions

