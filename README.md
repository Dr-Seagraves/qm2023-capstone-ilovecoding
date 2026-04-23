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

### Milestone 2: Exploratory Data Analysis & Visualization

#### Step 1: Generate Summary Statistics & Correlations
```bash
python code/M2_exploratory_analysis.py
```
**Outputs:**
- `results/tables/M2_summary_statistics.csv` — Statistics by year/size
- `results/tables/M2_descriptive_stats_table.csv` — Manuscript-ready summary
- `results/tables/M2_correlation_matrix.csv` — Pearson/Spearman correlations

#### Step 2: Generate Visualizations
```bash
python code/M2_visualizations.py
```
**Outputs:**
- `results/figures/M2_distributions.png` — Return distributions & normality tests
- `results/figures/M2_timeseries_plots.png` — Time-series analysis
- `results/figures/M2_scatter_analysis.png` — Relationship scatter plots
- `results/figures/M2_volatility_analysis.png` — Return volatility over time

### Milestone 3: Regression Outputs

When you add the final M3 deliverables, keep the results in `results/tables/` and format the main regression table in a standard academic style:
- One column per model
- Variables listed in the leftmost column
- Standard errors in parentheses beneath coefficients
- Summary rows for fixed effects, clustered standard errors, observations, and adjusted R-squared
- Export the final table as CSV or Excel for easy review

