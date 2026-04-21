# M3 Submission Checklist

**QM 2023 Capstone Project — Milestone 3: Econometric Models & Causal Inference**

**Team:** ILOVECODING  
**Members:** Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez  
**Due Date:** Friday, Week 14 (April 24, 2026) by 11:59 PM  
**Status:** ⏳ IN PROGRESS  
**Points:** 50 (25% of capstone grade)

---

## Project Overview

Milestone 3 transitions from descriptive analysis (M2) to causal inference. This phase estimates econometric models to quantify the effects of driver variables on outcomes, control for confounders, and test methodological assumptions. Success requires publication-ready regression tables and rigorous diagnostic testing.

**Core Deliverables:**
- `code/capstone_models.py` — Full econometric analysis pipeline
- `results/tables/M3_*.csv` — Regression output tables
- `results/figures/M3_*.png` — Diagnostic plots
- `results/reports/M3_findings_report.md` — Interpretation & findings (~3,500 words)

---

## Part 1: Python Script Requirements

### ✅ File: `code/capstone_models.py`

**Status:** IN PROGRESS

**Required Elements:**

1. **Header & Metadata (✓)**
   - Team name, members, submission date
   - Research objective
   - Data source and time period

2. **Section 1: Imports & Environment Setup (✓)**
   - Load config_paths: `FINAL_DATA_DIR`, `FIGURES_DIR`, `TABLES_DIR`
   - Import libraries: pandas, numpy, matplotlib, seaborn, statsmodels, linearmodels
   - Install: `pip install linearmodels` (for PanelOLS)
   - Set matplotlib defaults

3. **Section 2: Load & Prepare Data (✓)**
   - Input: `data/final/REIT_analysis_panel.csv` (M1 output)
   - Check: Does data have panel structure (Entity × Time)?
   - Check: Are variables properly scaled/normalized?
   - Create subset if needed for computational efficiency

4. **Section 3: Feature Engineering (✓)**
   - Create lagged variables: `[driver]_lag1`, `[driver]_lag2`, etc.
   - Create interactions if theory suggests
   - Create dummy variables (if needed for DiD)
   - Create time dummies for time fixed effects
   - Document lag selection rationale (from M2 correlations)

5. **Section 4: Model A — Fixed Effects Regression (REQUIRED) (✓)**
   - **Specification:**
     ```
     outcome_it = β₀ + β₁·driver_lag[X]_it + β₂·control1_it + β₃·control2_it 
                  + α_i + δ_t + ε_it
     ```
   - **Implementation:** `linearmodels.panel.PanelOLS`
   - **Steps:**
     1. Set panel index: `.set_index(['entity_id', 'time_var'])`
     2. Define outcome: `y = data['outcome']`
     3. Define predictors: `X = data[['driver_lag', 'control1', 'control2']]`
     4. Estimate: `PanelOLS(y, X, entity_effects=True, time_effects=True).fit(cov_type='clustered', cluster_entity=True)`
     5. Print summary with formatted coefficients, p-values, R²

   - **Expected Output:**
     - Coefficient table (coef, SE, t-stat, p-value)
     - R² (within, between, overall)
     - F-statistic, joint significance
     - Number of observations, entities, time periods

6. **Section 5: Model B — Alternative Specification (CHOOSE ONE) (✓)**

   **Option 1: Difference-in-Differences (DiD)**
   - Requires: Treatment/control grouping, policy shock date
   - Specification:
     ```
     outcome_it = β₀ + β₁·Treated_i + β₂·Post_t + β₃·(Treated × Post) + controls + ε_it
     ```
   - Report: Treatment effect (β₃), interaction term significance
   - Validity check: Pre-trend test (are pre-shock trends parallel?)

   **Option 2: ARIMA Time Series Forecast**
   - Requires: Single time series (aggregate if needed)
   - Steps:
     1. Test stationarity (ADF test)
     2. Use `pmdarima.auto_arima()` for order selection
     3. Fit `ARIMA(p,d,q)` model
     4. Forecast 6-12 periods ahead with 95% CI
     5. Evaluate: MAE, RMSE vs. naive baseline
   - Report: Forecast accuracy, model diagnostics

   **Option 3: Machine Learning Comparison (Random Forest vs. OLS)**
   - Train/test split (80/20)
   - Fit OLS and RandomForestRegressor
   - Compare on test set: R², RMSE, MAE
   - Feature importance: Which predictors matter most?
   - Report: Accuracy trade-off between interpretability (OLS) and flexibility (RF)

7. **Section 6: Diagnostic Tests (REQUIRED) (✓)**

   **1. Heteroskedasticity Test (Breusch-Pagan)**
   - Code:
     ```python
     from statsmodels.stats.diagnostic import het_breuschpagan
     bp_test = het_breuschpagan(residuals, X)
     print(f"BP Test p-value: {bp_test[1]}")
     ```
   - Interpretation: p < 0.05 = heteroskedasticity present → use robust SEs
   - Already addressed: PanelOLS uses `cov_type='clustered'`

   **2. Multicollinearity (Variance Inflation Factor)**
   - Code:
     ```python
     from statsmodels.stats.outliers_influence import variance_inflation_factor
     vif_data = pd.DataFrame({
         'Variable': X.columns,
         'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
     })
     ```
   - Threshold: VIF > 10 indicates problematic multicollinearity
   - Action: Drop or combine correlated variables if needed

   **3. Residual Plots**
   - Residuals vs. Fitted: Check for random scatter (no patterns)
   - Q-Q Plot: Check for normality
   - ACF/PACF: Check for autocorrelation

8. **Section 7: Robustness Checks (REQUIRED) (✓)**
   - Alternative lag specifications
   - Drop outliers and re-estimate
   - Subset: First/second half of time period
   - Alternative control variable sets
   - Report how results change

9. **Section 8: Save Results (✓)**
   - Regression tables → `results/tables/M3_model_A_results.csv`
   - Diagnostic plots → `results/figures/M3_*.png`
   - Model summaries, coefficient tables, p-values

**Code Quality:**
- ✅ Runs top-to-bottom without errors
- ✅ Uses relative paths only (config_paths module)
- ✅ Clear section headers (#, ##, ###)
- ✅ Comments on all major steps
- ✅ Logging: Print progress messages

---

## Part 2: Outputs & Tables

### Results Tables

**Status:** IN PROGRESS

| Table | Location | Contents | Format |
|-------|----------|----------|--------|
| Model A Results | `results/tables/M3_model_A_results.csv` | Coefficients, SE, t-stats, p-values | CSV |
| Model B Results | `results/tables/M3_model_B_results.csv` | Results from alternative model | CSV |
| VIF Diagnostics | `results/tables/M3_vif_diagnostics.csv` | Multicollinearity check | CSV |
| Robustness Summary | `results/tables/M3_robustness.csv` | Alternative specifications | CSV |

**Expected Table Format (Model A):**
```
Variable,Coefficient,Std Error,t-stat,p-value,CI_Lower,CI_Upper
driver_lag2,0.0234,0.0087,2.69,0.0071,0.0063,0.0405
control1,-0.1203,0.0456,-2.64,0.0083,-0.2097,-0.0309
control2,0.0567,0.0234,2.42,0.0155,0.0108,0.1026
```

---

### Diagnostic Figures

**Status:** IN PROGRESS

| Figure | Location | Description |
|--------|----------|-------------|
| Residuals vs Fitted | `results/figures/M3_residuals_vs_fitted.png` | Check homoskedasticity |
| Q-Q Plot | `results/figures/M3_qq_plot.png` | Check normality assumption |
| ACF/PACF | `results/figures/M3_acf_pacf.png` | Check autocorrelation |
| Model B Forecast (if ARIMA) | `results/figures/M3_arima_forecast.png` | Time series forecast with CI |
| Feature Importance (if RF) | `results/figures/M3_feature_importance.png` | Predictor rankings |

---

## Part 3: Findings Report

### File: `results/reports/M3_findings_report.md`

**Status:** IN PROGRESS

**Required Sections (Target: 3,000-3,500 words):**

1. **Executive Summary** (200 words)
   - Key research questions
   - Main findings
   - Causal interpretation
   - Policy/investment implications

2. **Methodology** (600 words)
   - Panel regression approach
   - Fixed effects rationale (why control for entity/time effects?)
   - Lag selection justification (from M2 correlations)
   - Variable definitions and data sources
   - Identification assumptions model A and model B

3. **Results from Model A** (000 words)
   - Coefficient interpretation (economic significance)
   - Statistical significance (p-values, CI)
   - Which drivers matter most?
   - R² and model fit
   - Comparison to baseline/naive predictions

4. **Results from Model B** (500 words)
   - Specification + rational for choice
   - Key findings
   - Robustness to alternative assumptions
   - Limitations and threats to validity

5. **Diagnostics & Assumption Checks** (400 words)
   - Heteroskedasticity test results
   - Multicollinearity (VIF) assessment
   - Residual plots interpretation
   - Autocorrelation (if applicable)
   - How violations addressed (e.g., robust SEs)

6. **Robustness Checks** (300 words)
   - Alternative lag specifications
   - Outlier sensitivity
   - Time-period stability
   - Control variable robustness
   - Summary: Are results stable?

7. **Conclusions & Next Steps** (300 words)
   - Do findings support/refute hypotheses from M2?
   - Causal interpretation defensibility
   - Practical implications
   - Limitations & confounders
   - Future research directions

**Writing Quality:**
- Professional tone
- Economic intuition for statistical results
- Proper citation of methodology sources
- Tables & figures embedded with captions

---

## Part 4: Submission Checklist

### Files to Submit

- [ ] **code/capstone_models.py** — Econometric model script
- [ ] **results/tables/M3_model_A_results.csv** — Main regression table
- [ ] **results/tables/M3_model_B_results.csv** — Alternative model table
- [ ] **results/tables/M3_vif_diagnostics.csv** — Multicollinearity check
- [ ] **results/tables/M3_robustness.csv** — Robustness summary
- [ ] **results/figures/M3_residuals_vs_fitted.png** — Diagnostic plot
- [ ] **results/figures/M3_qq_plot.png** — Diagnostic plot
- [ ] **results/figures/M3_acf_pacf.png** — Diagnostic plot (if applicable)
- [ ] **results/reports/M3_findings_report.md** — Findings & interpretation
- [ ] **M3_SUBMISSION_CHECKLIST.md** — This checklist (updated)

---

## Part 5: Testing & Validation

### Pre-Submission Tests

- [ ] **Script Execution:** Does `python code/capstone_models.py` run without errors?
- [ ] **Data Integrity:** Check for missing values in output tables
- [ ] **Output Paths:** Are all tables saved to `results/tables/`? All figures to `results/figures/`?
- [ ] **Table Format:** Do CSV outputs match expected columns?
- [ ] **Figure Quality:** Are plots readable at 300 DPI?
- [ ] **Report Completeness:** Does M3 report answer all required sections?
- [ ] **Reproducibility:** Can someone else run the script and get same results?
- [ ] **Git Commit:** Have all new files been added to version control?

---

## Grading Rubric (50 points)

| Criterion | Points | Status |
|-----------|--------|--------|
| **Python Script Quality** | 10 | ⏳ |
| • Code runs without errors | 3 | |
| • Proper structure & comments | 3 | |
| • Uses relative paths & config | 2 | |
| • Handles missing data gracefully | 2 | |
| **Model A: Fixed Effects** | 15 | ⏳ |
| • Correct specification & estimation | 5 | |
| • Proper handling of fixed effects | 3 | |
| • Robust standard errors used | 2 | |
| • Coefficient interpretation | 5 | |
| **Model B: Alternative** | 10 | ⏳ |
| • Appropriate choice for dataset | 3 | |
| • Correct implementation | 4 | |
| • Results clearly explained | 3 | |
| **Diagnostics & Robustness** | 10 | ⏳ |
| • Heteroskedasticity test | 2 | |
| • Multicollinearity (VIF) | 2 | |
| • Residual plots & interpretation | 3 | |
| • Robustness checks (≥3 specs) | 3 | |
| **Findings Report** | 5 | ⏳ |
| • Complete sections with proper depth | 2 | |
| • Statistical & economic interpretation | 2 | |
| • Professional writing | 1 | |

**Total: 50 points**

---

## Timeline & Milestones

| Date | Milestone | Status |
|------|-----------|--------|
| **April 2, 2026** | Create M3 checklist & script drafts | ⏳ IN PROGRESS |
| **April 8, 2026** | Model A (FE) working & tested | ⏳ |
| **April 12, 2026** | Model B & diagnostics complete | ⏳ |
| **April 18, 2026** | Robustness checks & report draft | ⏳ |
| **April 22, 2026** | Final QA & error checking | ⏳ |
| **April 24, 2026 11:59 PM** | ✅ **SUBMISSION DEADLINE** | ⏳ |

---

## Resources & References

### R Documentation
- [linearmodels.panel.PanelOLS](https://bashtage.github.io/linearmodels/doc/source/panel/index.html)
- [statsmodels Fixed Effects](https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html)

### Key Methods
- **Fixed Effects:** Wooldridge, *Econometric Analysis of Cross Section and Panel Data* (Ch. 10-11)
- **DiD:** Angrist & Pischke, *Mostly Harmless Econometrics* (Ch. 5)
- **ARIMA:** Box, Jenkins, Reinsel & Ljung, *Time Series Analysis* (Ch. 3-4)

---

## Notes & Approvals

**Team Preparation:**
- Assigned roles: Who handles Model A? Model B? Diagnostics? Report?
- Data validation: Confirm panel structure before coding
- Dependency check: All required packages installed?

**Instructor Feedback Points:**
- [To be filled by instructor during office hours]

---

**Status Update:** M3 submission checklist created. Ready to implement capstone_models.py.  
**Last Updated:** April 2, 2026  
**Next Action:** Begin Python script development

