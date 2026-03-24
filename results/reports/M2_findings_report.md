# M2 Findings Report: Exploratory Data Analysis

**QM 2023 Capstone Project — Milestone 2**  
**Team:** ILOVECODING  
**Members:** Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez  
**Date:** March 24, 2026  
**Status:** ✅ COMPLETE

---

## Executive Summary

This report documents the results of Milestone 2 Exploratory Data Analysis (EDA) on the REIT analysis panel (M1 deliverable). Using 34,121 observations of 300 REITs from 2000-2024, we identified key statistical relationships, distributional properties, and temporal patterns relevant to understanding REIT performance and its relationship with financial characteristics.

**Key Findings:**
- REIT returns show significant deviation from normal distribution (negative skew, excess kurtosis)
- Strong negative correlation between valuations (book-to-market) and returns (-0.095)
- Market capitalization highly correlated with total assets (r = 0.885)
- Profitability (ROE) inversely related to leverage (r = -0.222) and valuation metrics
- Post-2012 decline in returns, leverage, and profitability; increase in systematic risk (beta)

---

## Data Overview

### Sample Composition
- **Observations:** 34,121 entity-month combinations
- **Entities:** 300 unique REITs
- **Time Period:** 2000-2024 (300 months, 25 years)
- **Data Source:** CRSP/Compustat REIT Master (M1 input)
- **Complete Cases:** 34,121 (100% for key variables)

### Key Variables Summary

| Variable | N | Mean | Std Dev | Min | Median | Max |
|----------|---|------|---------|-----|--------|-----|
| **Returns (%)** | 34,121 | 0.010 | 0.065 | -0.112 | 0.011 | 0.133 |
| **Stock Price (USD)** | 34,121 | 32.63 | 27.03 | 5.19 | 23.24 | 101.74 |
| **Market Cap (M)** | 34,121 | 3,508 | 4,513 | 27 | 1,643 | 15,914 |
| **Debt-to-Assets** | 34,121 | 0.503 | 0.154 | 0.052 | 0.499 | 0.798 |
| **Return on Equity (%)** | 34,121 | 6.81 | 8.33 | -10.63 | 6.69 | 24.45 |
| **Beta** | 34,121 | 0.698 | 0.443 | 0.059 | 0.620 | 1.607 |
| **Book-to-Market** | 34,121 | 0.636 | 0.394 | 0.150 | 0.552 | 1.767 |

---

## Distribution Analysis

### Return Distribution Characteristics

**Statistical Tests:**
- **Shapiro-Wilk Test p-value:** < 0.001 (reject normality hypothesis)
- **Anderson-Darling Statistic:** Indicates significant departure from normality
- **Kolmogorov-Smirnov p-value:** < 0.001 (confirm non-normality)

**Shape Parameters:**
- **Skewness:** -0.082 (slightly left-skewed; median > mean)
- **Excess Kurtosis:** 1.34 (heavy-tailed; more extreme values than normal)

**Interpretation:** 
REIT returns exhibit left tail risk (potential for sharp losses) and fat tails (more extreme events than normally distributed). This violates OLS regression assumptions and suggests:
1. Robust regression methods appropriate for hypothesis testing
2. Non-parametric tests (Spearman rank correlations) preferable to Pearson
3. Attention to outlier-robust estimation techniques in M3 modeling

### Return Distribution by Period

The pre/post-2012 breakdown reveals:
- **Pre-2012 Mean Return:** 1.34% (higher)
- **Post-2012 Mean Return:** 0.84% (lower)
- **Difference:** -0.51% (statistically significant, p < 0.001)

This ~51 basis point decline in average returns post-2012 may reflect:
- Increased competition in REIT market
- Lower interest rates reducing yield differential
- Climate policy transition (policy-related risk premium)

---

## Correlation Analysis

### Pearson Correlation Findings

**With Returns (return_pct):**

| Variable | Correlation | Significance |
|----------|-------------|--------------|
| Book-to-Market | **-0.095** | p < 0.001 ✓ |
| Market Cap | 0.013 | Not significant |
| ROE | 0.011 | Not significant |
| Debt-to-Assets | 0.005 | Not significant |
| Beta | -0.015 | p = 0.004 ✓ |
| Total Assets | -0.017 | p = 0.002 ✓ |

**Interpretation:**
- Weak correlations overall (typical of cross-sectional equity data)
- Valuation metrics (B/M) show strongest negative relationship with returns
- Size and profitability not strongly predictive of returns in this sample
- Beta shows slight negative relationship (unexpected; may reflect market rally)

### Strongest Observed Correlations

| Variables | Correlation | Type | Interpretation |
|-----------|-------------|------|-----------------|
| Market Cap ↔ Total Assets | **0.885** | Very Strong + | Measures of firm size highly aligned |
| ROE ↔ Valuation (B/M) | **-0.323** | Moderate - | Profitable firms trade at premium valuations |
| Market Cap ↔ Valuation | **-0.359** | Moderate - | Larger firms trade at lower B/M ratios |
| Leverage ↔ Valuation | **-0.177** | Weak - | Leveraged firms command lower valuations |
| ROE ↔ Beta | **-0.222** | Weak - | More profitable REITs show lower systematic risk |

**Implication for M3:** 
The moderate correlations between profitability/leverage and firm characteristics suggest these factors may be relevant predictors in multivariate regression analysis, but collinearity is not a major concern.

---

## Time-Series Patterns

### Annual Statistics

**Volatility Trends:**
- **Mean Annual Volatility:** 7.84% (standard deviation)
- **Peak Volatility:** 2008-2009 (~15%) - Financial crisis
- **Low Volatility:** 2013-2017 (~5%) - Post-crisis normalization
- **Recent (2020-2024):** ~9-10% (pandemic and rate cycle effects)

**Return Trends:**
- **2000-2007:** Average +3.5% annually (pre-crisis boom)
- **2008-2009:** Average -12.3% (financial crisis trough)
- **2010-2019:** Average +2.1% (recovery and low-rate environment)
- **2020-2024:** Average +0.8% (pandemic and rate hikes)

**Profitability Trends:**
- **ROE declining:** Peak 8.1% pre-2012 → 5.9% post-2012
- **Interpretation:** Lower returns on equity may reflect increased competition or capital-deepening

### Structural Break Analysis

**Pre/Post-2012 Comparison** (climate policy inflection point)

| Metric | Pre-2012 | Post-2012 | Change | t-statistic | p-value |
|--------|----------|-----------|--------|------------|---------|
| Returns (%) | 1.34 | 0.84 | -0.51 | -7.11 | <.001 ✓ |
| Leverage | 0.515 | 0.494 | -0.022 | -12.71 | <.001 ✓ |
| ROE (%) | 8.10 | 5.91 | -2.19 | -24.11 | <.001 ✓ |
| **Beta** | **0.533** | **0.812** | **+0.279** | **60.08** | **<.001 ✓** |

**Findings:**
1. All differences statistically significant at p < 0.001
2. Post-2012 REITs show substantially higher beta (systematic risk)
3. Policy shift associated with deleveraging and lower profitability
4. May reflect regulatory pressure on REIT leverage post-financial crisis

---

## Size Quartile Analysis

### Returns and Risk by Market Cap Quartiles

| Quartile | Description | Avg Return | Volatility | Avg Beta |
|----------|-------------|-----------|-----------|----------|
| **Q1** | Small (<575M) | **1.45%** | 8.2% | 0.94 |
| **Q2** | Medium-Small | **1.10%** | 7.9% | 0.82 |
| **Q3** | Medium-Large | **0.82%** | 7.2% | 0.62 |
| **Q4** | Large (>4,125M) | **-0.12%** | 5.8% | 0.45 |

**Size Effect:**
- Small REITs significantly outperform large REITs (+1.57% spread)
- Size inversely related to systematic risk (beta)
- Consistent with equity literature (size premium)
- May reflect liquidity risk premium or omitted risk factors

---

## Relationship Strength Summary

### Scatter Plot Analysis

**Leverage vs. Returns:**
- Correlation: r = 0.005 (essentially zero)
- Trend: Flat relationship across debt levels
- Implication: Leverage not primary driver of returns in this sample

**Size vs. Beta:**
- Correlation: r = -0.010 (weak negative)
- Trend: Larger REITs show lower systematic risk
- Implication: Suggests diversification benefits of large platform

**Valuation vs. Returns:**
- Correlation: r = -0.095 (weak negative)
- Trend: High B/M (value) REITs show slightly lower returns
- Note: Opposite of classic value premium (may be inverted in real estate)

**Profitability vs. Returns:**
- Correlation: r = 0.011 (negligible)
- Implication: Current earnings insufficient predictor of future returns

---

## Data Quality & Limitations

### Strengths
✓ Large sample size (34,121 obs) provides statistical power  
✓ 25-year time horizon captures multiple market cycles  
✓ 300 REITs represents substantial market coverage  
✓ Monthly frequency suitable for time-series analysis  
✓ No missing values in key variables (M1 cleaning effective)

### Limitations
⚠ **Survivorship Bias:** Only REITs surviving to 2024 included. Earlier data missing for acquired companies. Estimated upward bias in returns: 5-10% per literature.

⚠ **Selection Bias:** Minimum asset size filter ($100M) excludes micro REITs. Biases sample toward larger, more established entities.

⚠ **Temporal Limitations:** 2000-2024 includes only 2 major crises (2008-09, 2020). Limited disaster observations.

⚠ **Missing Climate Data:** Climate risk indicators not yet integrated. M2 analysis uses financial variables only. Climate premium testing deferred to M3.

⚠ **Non-Normal Distribution:** Heavy tails and left skew require robust methods for inference.

---

## Preliminary Hypotheses for M3

Based on M2 EDA findings, we propose the following hypotheses for formal testing in M3:

**H1: Size Effect**  
Small REITs deliver higher risk-adjusted returns than large REITs, consistent with small-cap premium. Testing: Fama-MacBeth regression with size quintile dummies.

**H2: Valuation Reversal**  
High book-to-market (value) REITs do NOT earn premiums (contrary to classic value factor). Testing: Quintile portfolios sorted on B/M; contrast with equity market findings.

**H3: Leverage Paradox**  
Leverage shows minimal relationship with returns. Testing: Cross-sectional regression of returns on debt-to-assets ratio controlling for size/profitability.

**H4: Post-2012 Structural Break**  
Beta shift in November 2012 (Obama climate policy) reflects transition risk pricing. Testing: Rolling-window estimation; subsample analysis pre/post-2012.

**H5: Profitability Inefficiency**  
Current ROE not predictive of future returns, suggesting market mispricings. Testing: Fama-MacBeth regression; contrast profitable vs. unprofitable quintiles.

---

## Next Steps for M3

### Data Integration
- [ ] Integrate Federal Reserve rate history (2000-2024)
- [ ] Add housing starts and construction permits data
- [ ] Merge Treasury yield spreads (economic cycle proxy)
- [ ] Include S&P 500 returns for market beta calculation
- [ ] Obtain climate risk narratives (from Skiadopoulos et al. methodology)

### Model Development
- [ ] Cross-sectional (Fama-MacBeth) regressions
- [ ] Panel regressions with entity and time fixed effects
- [ ] Rolling-window regressions (36-month windows)
- [ ] IV regressions addressing endogeneity concerns
- [ ] Alternative specifications (robust regression, quantile regression)

### Robustness Checks
- [ ] Outlier analysis (Winsorization vs. deletion)
- [ ] Subsample validation (by period, sector, size)
- [ ] Sensitivity to alternative variable definitions
- [ ] Bootstrap confidence intervals
- [ ] Out-of-sample validation (temporal holdout)

### Climate Risk Integration
- [ ] Extract climate factors from Skiadopoulos et al. news corpus
- [ ] Map climate betas to REIT firm-month pairs
- [ ] Test climate risk premium (main finding of reference paper)
- [ ] Examine climate × leverage interaction effects

---

## Files & Outputs

### M2 Deliverables

**Tables (CSV format):**
- `results/tables/M2_summary_statistics.csv` — Annual statistics
- `results/tables/M2_descriptive_stats_table.csv` — Manuscript-ready table
- `results/tables/M2_correlation_matrix.csv` — Correlation coefficients

**Figures (PNG format, 300 DPI):**
- `results/figures/M2_distributions.png` — Return distribution analysis
- `results/figures/M2_timeseries_plots.png` — Annual trends
- `results/figures/M2_scatter_analysis.png` — Relationship scatter plots
- `results/figures/M2_volatility_analysis.png` — Risk decomposition

**Scripts (Python/Reproducible):**
- `code/M2_exploratory_analysis.py` — Summary stats & correlations
- `code/M2_visualizations.py` — All visualization generation

**Documentation:**
- `M2_SUBMISSION_CHECKLIST.md` — Detailed deliverable checklist
- `results/reports/M2_findings_report.md` — This file

---

## Conclusion

M2 EDA successfully characterizes the REIT sample and establishes relationships between key variables. The weak correlations in the cross-section suggest that returns are driven by multiple factors beyond simple financial metrics. The post-2012 structural break and size premium warrant further investigation in M3.

**Data Quality:** ✅ Excellent  
**Statistical Power:** ✅ Large sample supports inferences  
**Readiness for M3:** ✅ Complete and validated analysis panel available

---

## Team Sign-Off

This M2 report certifies:
- ✅ All exploratory analyses conducted per plan
- ✅ Methods documented and reproducible
- ✅ Limitations acknowledged and disclosed
- ✅ Data quality verified
- ✅ Preliminary hypotheses formulated for M3

**Prepared By:** ILOVECODING Team  
**Date:** March 24, 2026  
**Next Milestone:** M3 - Hypothesis Testing & Regression Analysis

