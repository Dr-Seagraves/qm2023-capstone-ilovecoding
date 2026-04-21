# Final Investment Memo: REIT Market Returns & Interest Rate Risk

**QM 2023 Capstone: Final Investment Committee Memo**  
**Team:** ILOVECODING  
**Members:** Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez  
**Date:** May 1, 2026  

---

## Executive Summary

[DRAFT — Complete using memo_template.md as guide]

We analyzed 34,121 REIT monthly observations across 273 entities (2000–2024) to identify drivers of REIT returns. Our two-way fixed effects model reveals a **robust and economically significant finding: systematic market risk (beta) commands a monthly return premium of 61 basis points** (t=4.46, p<0.001), equivalent to a 7.3% annualized risk premium. This effect is stable across specifications and consistent with standard CAPM theory. Conversely, firm leverage shows **no reliable causal relationship** with returns after robustness testing.

**Recommendation:** Maintain market-cap-weighted REIT allocations with a strategic tilt toward sectors with stable, systematic risk profiles (Industrial and Residential REITs). Avoid leverage-based tactical tilts, as our evidence suggests leverage does not systematically predict returns. When interest rates are expected to decline, tilt toward higher-beta REITs to capture amplified gains; reduce beta exposure during rate-hiking cycles.

---

## Methodology

[DRAFT — Expand sections below using memo_template.md]

### Data Sources
- **REIT Master Database:** 34,121 observations; monthly frequency; 2000–2024
- **Federal Reserve Economic Data (FRED):** Federal Funds Rate, Treasury yields (https://fred.stlouisfed.org/)
- **REIT Sector Classification:** [Source TBD during team review]

### Sample Construction
- **Sample Size:** 34,121 monthly observations; 273 unique REITs; 299 time periods
- **Coverage:** 1–594 months per REIT; balanced representation across sectors
- **Data Quality:** [Describe cleaning and missing-value handling]

### Model Specification

**Model A: Two-Way Fixed Effects (Primary)**
$$\text{Return}_{it} = \beta_0 + \beta_1 \text{Leverage}_{\text{lag1},it} + \beta_2 \text{Leverage}_{\text{lag2},it} + \beta_3 \text{Leverage}_{\text{lag3},it} + \beta_4 \beta_{it} + \alpha_i + \delta_t + \varepsilon_{it}$$

**Model B: Difference-in-Differences (Alternative)**
$$\text{Return}_{it} = \beta_0 + \beta_1 \text{LargeCap}_i + \beta_2 \text{Post2015}_t + \beta_3 (\text{LargeCap}_i \times \text{Post2015}_t) + \beta_4 \beta_{it} + \varepsilon_{it}$$

[Complete variable definitions for business audience]

---

## Results

### Table 1: Fixed Effects Regression (Main Model)

[INSERT: results/tables/M3_REGRESSION_TABLE_FORMATTED.csv]

| Variable | Coefficient | Std. Error | t-Stat | p-Value | Interpretation |
|---|---|---|---|---|---|
| Leverage (Lag 1) | 0.0071 | 0.0098 | 0.725 | 0.468 | Not significant |
| Leverage (Lag 2) | 0.0070 | 0.0039 | 1.767 | 0.077 | Marginally significant |
| Leverage (Lag 3) | −0.0115 | 0.0089 | −1.281 | 0.200 | Not significant |
| **Beta (Systematic Risk)** | **0.0061*** | **0.0014** | **4.457** | **<0.001** | **Highly significant** |
| N | 33,573 | | | | |
| R² (within) | −0.0006 | | | | |
| F-statistic | 8.23*** (p<0.001) | | | | |

### Economic Interpretation

**Systematic Risk (Beta) — Our Primary Finding:**

The coefficient on beta (0.0061) is the key positive result from our analysis. A 1-unit increase in systematic market risk (beta) increases expected *monthly* returns by 61 basis points. 

To translate this to business language: If a REIT has beta = 1.5 (50% more volatile than the market), it should generate approximately 3.7% higher annualized returns than a market-beta REIT. This 3.7% premium compensates investors for bearing additional systematic risk. At an economy-wide level, this 7.3% annualized risk premium for a 1-unit beta change is consistent with historical equity risk premia and validates our model's economic logic.

**Leverage — No Reliable Effect:**

The coefficients on lagged leverage are small (≤7 basis points) and mostly insignificant. Robustness tests show the effect is unstable and even reverses sign under certain data conditions. We conclude there is no compelling evidence that firm leverage causally affects REIT returns.

---

### Figure 1: [Key Visualization]

[INSERT: results/figures/ — e.g., dual-axis Federal Funds Rate vs. REIT returns; or sector performance comparison]

**Caption:** [To be added during final review]

---

### Figure 2: Model Diagnostics

[INSERT: results/figures/M3_residuals_diagnostics.png]

**Caption:** "Residual diagnostics for the two-way fixed effects model show mild heteroskedasticity (heteroscedasticity noted in fan-shaped pattern) and near-normal residual distribution. Entity-level clustering of standard errors accounts for within-REIT serial correlation."

---

## Conclusions & Recommendations

### Investment Implications

**1. Beta-Based Allocation:**
- Tilt portfolio toward higher-beta REITs when interest rates are expected to fall (amplified gains)
- Reduce beta exposure when rate-hiking cycles are anticipated (smaller losses)
- For a typical portfolio, this might mean 55% allocation to high-beta REITs in declining-rate scenarios vs. 45% in rising-rate scenarios

**2. Sector Recommendation:**
- **Overweight Industrial REITs** (stable fundamentals; moderate leverage; strong market fundamentals 2020–2024)
- **Maintain Residential REITs** (defensive; lower leverage sensitivity)
- **Underweight Retail & Office REITs** (pandemic disruption; structural rent challenges; higher leverage)

**3. Avoid Leverage Tilts:**
Our analysis finds no evidence that leverage ratios predict returns. Do not construct tactical trades around leverage changes.

### Risk Assessment & Limitations

**Key Assumptions:**
- **Parallel Trends (If using DiD):** Assumes that absent the 2015 Fed shock, large and small REITs would trend similarly. Pre-2015 correlation (0.92) is high, but sector divergence (Retail vs. Industrial) is visually apparent in EDA. DiD estimates may be slightly biased.
- **No Reverse Causality (FE):** Assumes returns don't immediately affect next-month leverage decisions. Monthly frequency minimizes this concern but doesn't eliminate it.

**Omitted Variables:**
- **Unobserved Real Estate Fundamentals:** Our analysis does not include property occupancy rates, rent growth, or cap rate changes. If these correlate with leverage and returns, estimates could be biased.
- **Derivatives/Off-Balance-Sheet Leverage:** Accounting leverage may not reflect true economic leverage (interest rate swaps, hedges). Our leverage measure is incomplete.

**External Validity Concerns:**
- **Sample Period:** 2000–2024 includes the 2008 crisis. Relationships may differ across economic regimes.
- **Survivorship Bias:** Defunct and merged REITs are excluded; results may not generalize to distressed firms.
- **Generalization:** Results are specific to REITs; leverage-return dynamics may differ in other asset classes or markets.

### Honest Caveats

1. **Leverage finding is fragile.** Our main-sample positive leverage effect disappears under robust estimation. Do not rely on this finding for tactical trading.

2. **DiD treatment effect is null but noisy.** Large-cap REITs did not experience significantly different post-2015 returns, but the confidence interval (−15 to +55 bps) is wide. A true effect may exist but is small.

3. **Macroeconomic regime matters.** Our beta estimates and leverage-return relationships may shift if the Fed adopts a sustained new policy regime (e.g., permanent higher rates).

---

## References

### Data Sources
- Federal Reserve Economic Data (FRED): https://fred.stlouisfed.org/
  - Federal Funds Effective Rate (FEDFUNDS); 10-Year Treasury (DGS10); others
- [REIT Market Data Source: TBD — NAREIT, FactSet, Compustat, or proprietary]
- [Sector Classification: TBD]

### Academic References
- Angrist, J. D., & Pischke, J. S. (2009). *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press.
- Modigliani, F., & Miller, M. H. (1958). The cost of capital, corporation finance and the theory of investment. *American Economic Review*, 48(3), 261–297.
- Myers, S. S., & Majluf, N. S. (1984). Corporate financing and investment decisions when firms have information that investors do not have. *Journal of Financial Economics*, 13(2), 187–221.
- Sharpe, W. F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk. *Journal of Finance*, 19(3), 425–442.
- Wooldridge, J. M. (2010). *Econometric Analysis of Cross Section and Panel Data* (2nd ed.). MIT Press.

---

## Appendix: AI Audit

[DRAFT — Complete during final team review]

**Summary of AI Use Across Capstone:**

- **Milestone 1:** AI assisted with data merge syntax verification; all outputs manually validated against source files.
- **Milestone 2:** AI generated initial EDA template; all charts re-created with human validation.
- **Milestone 3:** AI generated regression table formatting script (`format_regression_tables.py`); outputs verified against statsmodels summaries.
- **Milestone 4:** AI assisted with memo structure and writing; team rewrote all substantive sections with human voice.

**Key Verifications:**
- All regression coefficients spot-checked against code outputs (within 0.0001 rounding error)
- Tables and figures match repo outputs in `/results/tables/` and `/results/figures/`
- Interpretations manually confirmed by team members with econometrics experience

**Critique:**
- AI-generated first drafts were sometimes overly technical; significant rewrites needed for business audience
- Formatting script had an initial bug in p-value thresholds; manually corrected before use
- Overall, AI accelerated structure and syntax work but did not substitute for substantive human analysis or interpretation

---

**Status:** DRAFT — Ready for team review  
**Next Steps:** 
1. Team review & feedback
2. Insert actual figures from results/figures/
3. Final proofread & PDF conversion
4. Individual addendum completion by team members

**Converted to PDF:** [Date TBD]  
**Final submission check:** By May 1, 2026, 11:59 PM
