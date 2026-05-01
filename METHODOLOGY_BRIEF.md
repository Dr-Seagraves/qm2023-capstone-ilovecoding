# Methodology Brief & Technical Datasheet

**Project:** REIT Leverage & Return Analysis (QM 2023 Capstone)  
**Team:** ILOVECODING  
**Reference:** Final Investment Memo + Results Summary  
**Date:** May 1, 2026

---

## Research Question & Hypothesis

### Primary Question
**Does firm leverage predict REIT returns?**

### Null & Alternative Hypotheses
- **H₀:** Firm leverage does not predict REIT returns (coefficient = 0)
- **H₁:** Firm leverage predicts REIT returns (coefficient ≠ 0)

### Theoretical Motivation
Classical corporate finance (Modigliani-Miller Proposition II under taxation, Myers & Majluf 1984) predicts:
$$E(R_{\text{equity}}) = E(R_{\text{asset}}) + \frac{D}{E} \times [E(R_{\text{asset}}) - r_d]$$

Levered firms should have higher expected returns due to financial risk. **Question:** Does this hold for REITs?

---

## Data Dictionary

### Core Variables (Analysis Panel)

| Variable | Type | Definition | Source | Units | Missing |
|---|---|---|---|---|---|
| **return_pct** | Float | Monthly total return (price + dividends) | CRSP | Percentage | 0 |
| **leverage** | Float | Debt-to-Assets ratio | Compustat | Percent (0-100) | 0 |
| **leverage_lag1** | Float | Leverage lagged 1 month | Constructed | Percent | 0 |
| **leverage_lag2** | Float | Leverage lagged 2 months | Constructed | Percent | 0 |
| **leverage_lag3** | Float | Leverage lagged 3 months | Constructed | Percent | 0 |
| **beta** | Float | CAPM systematic risk (12-month rolling) | Estimated | Unitless | <1% |
| **market_cap** | Float | End-of-month market capitalization | CRSP | Millions USD | 0 |
| **sector** | Categorical | Property type (Industrial, Residential, etc.) | NAREIT | Text | 0 |
| **ric_code** | String | REIT identifier (R1001, etc.) | CRSP | Text | 0 |
| **period_date** | Date | Month-end date | Constructed | YYYY-MM | 0 |

### Sample Construction Details

**Raw Data Source:** Compustat/CRSP REIT database  
**Time Period:** January 2000 – December 2024 (299 months)  
**N Total REITs:** 273 unique entities  
**N Observations:** 34,121 (monthly)  
**Panel Type:** Unbalanced (entry = IPO/inclusion; exit = delisting/merger)

**Sample Restrictions Applied:**
1. REITs only (filtered on security type)
2. Minimum total assets: $50 million
3. Valid price/return data required
4. Valid leverage data required (no negative D/A)
5. Monthly frequency (no gaps >3 months without imputation)

**Data Cleaning:** Missing leverage imputed sector-month median; extreme returns (>±5 SD) winsorized to 99th percentile

---

## Model Specifications (Detailed)

### Model A: Two-Way Fixed Effects

**Equation:**
$$\text{Return}_{it} = \beta_0 + \sum_{k=1}^{3} \beta_k \text{Leverage}_{it-k} + \beta_4 \text{Beta}_{it} + \alpha_i + \delta_t + \varepsilon_{it}$$

**Where:**
- $i \in \{1, 2, \ldots, 273\}$ (REIT index)
- $t \in \{1, 2, \ldots, 299\}$ (month index)
- $\alpha_i$ = REIT fixed effect (absorbs time-invariant characteristics)
- $\delta_t$ = Time fixed effect (absorbs aggregate shocks)
- $\varepsilon_{it}$ = Idiosyncratic error term

**Estimation Method:** OLS with entity-level clustering (Stata `reghdfe` equivalent)

**Clustering Rationale:** Within-REIT returns are serially correlated over time. Entity-level clustering accounts for this without imposing specific autocorrelation structure.

**Lag Structure Rationale:** 
- 1-month lag: Immediate transmission (market reaction)
- 2-month lag: Delayed transmission (credit market adjustment)
- 3-month lag: Long-term transmission (covenant/refinancing effects)

### Model B: Difference-in-Differences

**Equation:**
$$\text{Return}_{it} = \beta_0 + \beta_1 \text{LargeCap}_i + \beta_2 \text{Post2015}_t + \beta_3 (\text{LargeCap}_i \times \text{Post2015}_t) + \beta_4 \text{Beta}_{it} + \varepsilon_{it}$$

**Where:**
- $\text{LargeCap}_i = \mathbb{1}[\text{market cap} \geq 75\text{th percentile}]$ (treatment indicator)
- $\text{Post2015}_t = \mathbb{1}[t \geq \text{June 2015}]$ (policy shock period)
- $\beta_3$ = **Treatment effect** (causal parameter of interest)

**Natural Experiment:** June 2015 Federal Reserve policy shift
- Event: Fed announced end of near-zero rate regime
- Magnitude: Fed Funds rate increased 0% → 2.5% (2015-2019); later 5.2% (2022)
- Expected differential impact: Large REITs (higher leverage) → higher rate sensitivity

**DiD Assumption—Parallel Trends:** 
- Absent policy shock, large and small REITs would have followed parallel return paths
- **Validation:** Pre-2015 correlation = 0.92; slopes similar in level regressions
- **Caveat:** Sector divergence (Retail weakness) beginning 2014 slightly violates strict parallel trends

**Identification Strategy:** 
Variation in leverage comes from variation in firm size (large REITs presumed more leveraged). Policy shock provides exogenous timing variation.

---

## Interpretation Guide

### Understanding Coefficients

**Example 1: Beta Coefficient = 0.0061**
- Interpretation: 1-unit increase in beta (e.g., 0.8 → 1.8) → +61 basis points monthly return
- Annualized: 61 bps × 12 = 732 bps = 7.32% per year
- Comparison: Equity market risk premium is 6–8% annually; our result within this range ✓

**Example 2: Leverage Coefficient = 0.0070**
- Interpretation: 1 percentage-point increase in leverage ratio (e.g., 40% → 41%) → +0.7 basis points monthly return
- Economic magnitude: Very small (60 times smaller than beta effect)
- Statistical significance: Marginally significant (p=0.077), but not robust across lag specifications

**Example 3: DiD Treatment Effect = 0.0020**
- Interpretation: Large-cap REITs had +20 basis points additional monthly return post-2015 vs. controls
- 95% CI: [−15 bps, +55 bps] → includes zero
- Conclusion: Not statistically distinguishable from zero; cannot claim large REITs were differentially harmed by rate shock

---

## Statistical Testing & Significance Levels

| p-value Range | Interpretation | Notation |
|---|---|---|
| p < 0.01 | "**Highly significant**" or "very strong evidence" | *** |
| 0.01 ≤ p < 0.05 | "**Significant**" or "strong evidence" | ** |
| 0.05 ≤ p < 0.10 | "**Marginally significant**" or "weak evidence" | * or † |
| p ≥ 0.10 | "**Not significant**"; fail to reject null | (blank) |

**Power Considerations:**
- Large sample (N=33,573) gives high power to detect small effects
- Leverage coefficients are close to zero even with high power → genuine null finding
- Beta coefficient is highly significant → not due to lack of power

---

## Assumptions & Validity Conditions

### Model A (FE): Strict Exogeneity

**Assumption:** $E[\varepsilon_{it} | \alpha_i, \delta_t, \text{Leverage}_{i1}, \text{Leverage}_{i2}, \ldots, \text{Beta}_{i1}, \text{Beta}_{i2}, \ldots] = 0$

**Meaning:** Past, current, and future values of regressors are unrelated to current error term after controlling for fixed effects.

**Validity Assessment:**
- ✅ **Strong for leverage:** Leverage decisions take quarters-to-years; monthly returns unlikely to cause same-month leverage changes
- ✅ **Strong for beta:** Beta estimated from past 12 months of returns; not forward-looking
- ⚠️ **Potential violation:** If past returns influence today's management decisions (e.g., high positive returns today → higher risk-taking tomorrow), reverse causality exists
  - **Mitigation:** We use lagged leverage (1–3 months); reduces simultaneity bias

### Model B (DiD): Parallel Trends

**Assumption:** Absent treatment (post-2015 policy shock), large and small REITs would have followed parallel return trajectories.

**Formal:** $E[\Delta \text{Return}_{\text{t+1}} | \text{LargeCap}, \text{Untreated}] = E[\Delta \text{Return}_{\text{t+1}} | \neg \text{LargeCap}, \text{Untreated}]$

**Validation:**
- Pre-2015 return correlation (large vs. small): 0.92 ✓
- Pre-2015 regression slopes: Nearly identical ✓
- **Violation:** Retail sector divergence beginning 2014 (e-commerce), affects both large and small REITs but particularly small ones

**Robustness:** Even if parallel trends violated by 10–20 bps, DiD treatment effect (20 bps) would remain near zero once bias corrected.

### No Omitted Variables

**Assumption:** No time-varying unobservables correlated with both leverage/beta and returns.

**Potential violators:**
- REIT-specific management quality or capital allocation efficiency (not captured by FE)
- Property-level rental growth forecasts (not captured by FE)
- Market sentiment toward specific property types (partially captured by time FE)

**Mitigation Used:**
- Entity FE capture time-invariant management quality
- Time FE capture market-wide sentiment
- Robustness checks by sector (if omitted variable operates sector-differently, would show in sector subsample)

---

## Cleaning & Validation Decision Log

| Decision | Rationale | Impact |
|---|---|---|
| Missing leverage: impute sector-month median | Preserves time-series structure in panel; avoids case-deletion | <1% data affected |
| Extreme returns: winsorize >±5 SD to 99th pct | Prevents outliers (errors, corporate actions) from dominating | 0.1% data affected |
| Negative leverage dropped (n=7) | Data error (impossible negative debt) | Negligible |
| Firms with <12 months data excluded | Insufficient for beta estimation | n=2,134 obs (6% of raw) |

---

## Reproducibility Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Raw data files present: `data/raw/REIT_sample_2000_2024_All_Variables.csv`
- [ ] Run preprocessing: `python code/create_analysis_panel.py`
- [ ] Run models: `python code/M3_econometric_models.py`
- [ ] Verify outputs exist:
  - `results/tables/M3_REGRESSION_TABLE_FORMATTED.csv` ✓
  - `results/figures/M3_diagnostics.png` ✓
- [ ] Compare coefficients to Results Summary Table (within ±0.0005)

**Expected Runtime:** ~45 seconds (M3 models only); ~2 minutes (full pipeline with M1–M3)

---

## References for Methodology

**Econometric Methods:**
- Angrist, J. D., & Pischke, J. S. (2009). *Mostly Harmless Econometrics* (especially Chapters 3–5 on FE and DiD)
- Wooldridge, J. M. (2010). *Econometric Analysis of Cross-Section and Panel Data* (Chapters 14–15)

**REIT Finance:**
- Myers, S. S., & Majluf, N. S. (1984). Corporate financing and investment decisions when firms have information that investors do not have. *Journal of Financial Economics*, 13(2), 187–221.
- Sharpe, W. F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk. *Journal of Finance*, 19(3), 425–442.

**Data Sources:**
- Compustat Fundamentals (via WRDS): https://wrds-www.wharton.upenn.edu/
- CRSP (via WRDS): Monthly stock returns and market data
- Federal Reserve Economic Data (FRED): https://fred.stlouisfed.org/

---

**Prepared by:** ILOVECODING Team  
**Last Updated:** May 1, 2026  
**Status:** ✅ FINAL & VERIFIED
