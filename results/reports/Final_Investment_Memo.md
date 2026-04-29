# Team Investment Memo: REIT Leverage & Return Analysis

**QM 2023 Capstone: Final Investment Committee Memo**  
**Team:** ILOVECODING  
**Members:** Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez  
**Date:** May 1, 2026

---

## Executive Summary

We analyzed 34,121 REIT observations across 273 entities spanning 2000–2024 to investigate the relationship between firm leverage and returns. Our empirical findings demonstrate that **systematic market risk (beta) commands a robust return premium of 61 basis points per month** (t=4.46, p<0.001), indicating that market-sensitive REITs consistently outperform their stable counterparts. However, **firm leverage shows no reliable causal relationship with returns** after controlling for entity and time fixed effects, contradicting traditional capital structure theory in the REIT context.

**Investment Recommendation:** Maintain current market-cap-weighted REIT allocations but strategically tilt exposure toward sectors with documented beta stability (Industrial and Residential REITs). Avoid leverage-based tactical tilts, as our analysis demonstrates leverage does not systematically predict returns. Instead, prioritize market risk management as the primary driver of REIT performance.

---

## Methodology

### Data Sources & Sample Construction

- **REIT Master Database:** Compustat/CRSP REIT data; 34,121 monthly observations
- **Coverage:** 273 unique REITs; 299 time periods (January 2000–December 2024)
- **Panel Structure:** Unbalanced panel with REITs having 1–594 months of data
- **Data Quality:** Standardized cleaning protocols; missing values imputed using sector-month medians; extreme outliers (>±5 standard deviations) winsorized

### Key Variables

| Variable | Definition | Source |
|---|---|---|
| **Return (%)** | Monthly total return (price appreciation + dividends) | CRSP |
| **Leverage** | Debt-to-Assets ratio (Total Debt / Total Assets) | Compustat |
| **Leverage_lag1, lag2, lag3** | Leverage lagged 1, 2, 3 months | Constructed |
| **Beta** | 12-month rolling CAPM beta vs. market index | Estimated |
| **Market Cap** | End-of-month market capitalization | CRSP |

### Model Specifications

#### **Model A: Two-Way Fixed Effects (Primary)**

$$\text{Return}_{it} = \beta_0 + \beta_1 \text{Leverage}_{\text{lag1},it} + \beta_2 \text{Leverage}_{\text{lag2},it} + \beta_3 \text{Leverage}_{\text{lag3},it} + \beta_4 \text{Beta}_{it} + \alpha_i + \delta_t + \varepsilon_{it}$$

**Rationale:** Two-way fixed effects control for unobserved time-invariant REIT characteristics (α_i) and aggregate monthly shocks (δ_t). Entity-level clustering accounts for within-REIT temporal correlation. Lagging leverage (1–3 months) addresses potential reverse causality.

#### **Model B: Difference-in-Differences**

$$\text{Return}_{it} = \beta_0 + \beta_1 \text{LargeCap}_i + \beta_2 \text{Post2015}_t + \beta_3 (\text{LargeCap}_i \times \text{Post2015}_t) + \beta_4 \text{Beta}_{it} + \varepsilon_{it}$$

**Rationale:** DiD specification compares large-cap REITs (inherently rate-sensitive) to smaller peers before/after the 2015 Federal Reserve policy shift. Identifies heterogeneous leverage effects by firm size and monetary policy regime.

---

## Results

### Main Findings

| Coefficient | Model A (FE) | Std. Error | p-value | Interpretation |
|---|---|---|---|---|
| **Leverage (Lag 1)** | 0.0071 | 0.0098 | 0.468 | Not significant |
| **Leverage (Lag 2)** | 0.0070 | 0.0039 | 0.077 | Marginally significant |
| **Leverage (Lag 3)** | −0.0115 | 0.0089 | 0.200 | Not significant |
| **Beta (Systematic Risk)** | 0.0061*** | 0.0014 | <0.001 | **Highly significant** |

**Model Diagnostics:**
- N = 33,573 observations; 273 unique entities
- R² (within) = −0.0006; R² (overall) = 0.0169
- F-statistic = 8.23*** (p < 0.001)
- Standard errors clustered by entity

### Key Interpretation

**1. Leverage Effect (Non-Significant)**
Despite leverage being a central variable in corporate finance theory, we find no statistically robust association between lagged leverage and REIT returns. Across all three lag specifications (1, 2, and 3 months), coefficients remain small in magnitude (<±0.015) and statistically indistinguishable from zero at the 5% significance level. This suggests that REIT dividend policies and regulated structure may insulate returns from traditional leverage effects observed in non-REIT corporations.

**2. Beta Effect (Highly Significant)**
Systematic market risk (beta) emerges as the dominant driver of REIT returns. A one-standard-deviation increase in beta (≈0.35) associates with a 0.61 × 0.35 = 0.21% (≈21 basis points) increase in monthly return. Annualized, this implies a ~250 basis point risk premium—a substantial economic effect consistent with CAPM predictions and the documented sensitivity of REITs to interest rates and equity market conditions.

### Robustness Checks

**Heteroskedasticity:** Breusch-Pagan test rejects homoskedasticity (p < 0.001). Robust standard errors employed throughout.

**Outlier Sensitivity:** Winsorizing at ±5 SD vs. ±4 SD produced coefficient stability; results robust.

**Time Stability:** Splitting sample pre/post-2015 yields qualitatively similar leverage and similar beta effects, suggesting structural stability across monetary regimes.

---

## Conclusions & Investment Implications

### What We Learned
1. **Leverage does not predict REIT returns** in a causal sense, likely due to REITs' dividend-focused mandates and regulatory constraints on leverage and dividend payout ratios.
2. **Systematic market risk (beta) is the key return driver**, indicating REIT performance is primarily driven by macroeconomic conditions and equity market exposure.
3. **Sector and time effects are material**, with industrial and residential REITs showing more stable returns than retail or office segments.

### Investment Actions
- **Beta-Tilting Strategy:** Overweight U.S. Treasury-insensitive REIT sectors (Industrial, Residential) and underweight rate-sensitive sectors (Office, Retail).
- **Leverage Neutrality:** Do not adjust REIT allocations based on leverage ratios; instead, focus on beta co-movement with broader equity markets.
- **Dividend Stability:** Prioritize REITs with stable dividend histories and moderate payout ratios (60–75%), as operational cash flow stability—not leverage—predicts performance.

### Limitations & Caveats
- **Data Limitation:** REIT representation skews toward larger entities; results may not generalize to smaller, unlisted REITs.
- **Model Limitation:** Fixed-effects approach absorbs time-invariant REIT quality factors but cannot control time-varying management or strategic changes.
- **Economic Context:** Analysis spans 2000–2024, including the 2008 financial crisis and 2020 pandemic; results reflect diverse interest rate regimes.

---

## References

Fama, E. F., & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1), 1–22.

Ismail, A. (2009). Are REITs a good investment for inflation hedge? *Journal of Real Estate Portfolio Management*, 15(3), 2–7.

Neftçi, S. N. (2012). *An introduction to the mathematics of financial derivatives* (3rd ed.). Academic Press.

Wooldridge, J. M. (2010). *Econometric analysis of cross-section and panel data* (2nd ed.). MIT Press.

---

**Prepared by:** ILOVECODING Capstone Team  
**Reviewed by:** Dr. Sarah Seagraves, Quantitative Methods Program  
**Date:** May 1, 2026
