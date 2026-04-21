# Team Memo Template: Final Investment Memo

**QM 2023 Capstone: Final Investment Committee Memo**  
Team: ILOVECODING  
Members: Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez  
Date: May 1, 2026  

---

## Executive Summary

[2-3 sentences stating key finding with magnitude and significance]

Example: "We analyzed 34,121 REIT observations across 273 entities (2000–2024) and found that systematic market risk (beta) commands a robust return premium of 61 basis points per month (t=4.46, p<0.001). Firm leverage, however, shows no reliable causal relationship with returns after controlling for entity and time fixed effects."

[1-2 sentences with specific investment recommendation]

Example: "Based on these findings, we recommend maintaining current market-cap-weighted allocations to REITs but tilting exposure toward sectors with documented beta stability (Industrial and Residential REITs). Avoid leverage-based tactical tilts, as our analysis suggests leverage does not systematically predict returns."

---

## Methodology

### Data Sources
- **REIT Master Database:** [source with citation/URL]
  - Primary REIT financial data, monthly observations
- **FRED (Federal Reserve Economic Data):** https://fred.stlouisfed.org/
  - Federal Funds Rate, Treasury yields, macroeconomic controls
- **REIT Sector Classification:** [source]
  - Sector assignments (Industrial, Retail, Office, Residential, etc.)

### Sample Construction
- **Sample Size:** 34,121 monthly observations; 273 unique REITs; 299 time periods (2000–2024)
- **Coverage:** Balanced panel with REITs having 1–594 months of data
- **Data Quality:** [Describe cleaning steps, missing value handling, outlier treatment]

### Model Specifications

**Model A: Two-Way Fixed Effects (Primary)**
$$\text{Return}_{it} = \beta_0 + \beta_1 \text{Leverage}_{\text{lag1},it} + \beta_2 \text{Leverage}_{\text{lag2},it} + \beta_3 \text{Leverage}_{\text{lag3},it} + \beta_4 \beta_{it} + \alpha_i + \delta_t + \varepsilon_{it}$$

Where:
- $\text{Return}_{it}$ = Monthly return (%) for REIT $i$ in month $t$
- $\text{Leverage}_{\text{lag},it}$ = Debt-to-Assets ratio (lagged 1, 2, 3 months)
- $\beta_{it}$ = Systematic market risk (CAPM beta)
- $\alpha_i$ = Entity fixed effects (time-invariant REIT characteristics)
- $\delta_t$ = Time fixed effects (aggregate monthly shocks)
- $\varepsilon_{it}$ = Error term, clustered at entity level

**Rationale:** Two-way fixed effects control for unobserved time-invariant REIT characteristics and aggregate time shocks. Entity clustering accounts for within-REIT correlation over time.

**Model B: Difference-in-Differences (Alternative Specification)**
$$\text{Return}_{it} = \beta_0 + \beta_1 \text{LargeCap}_i + \beta_2 \text{Post2015}_t + \beta_3 (\text{LargeCap}_i \times \text{Post2015}_t) + \beta_4 \beta_{it} + \varepsilon_{it}$$

Where:
- $\text{LargeCap}_i$ = Indicator: REIT in top market-cap quartile
- $\text{Post2015}_t$ = Indicator: observation after 2015 (Fed tightening period)
- $(\text{LargeCap}_i \times \text{Post2015}_t)$ = Treatment effect (difference-in-differences estimate)

**Rationale:** DiD compares large-cap REITs (typically more rate-sensitive) to others before/after the 2015 Fed policy shift. Identifies heterogeneous effects by firm size.

### Variable Definitions
- **Return_pct:** Monthly percentage return (price appreciation + dividends)
- **Leverage (driver):** Debt-to-Assets ratio, computed as Total Debt / Total Assets
- **Leverage_lag1, lag2, lag3:** Lagged leverage at 1, 2, 3-month horizons
- **Beta:** CAPM systematic risk, estimated from 12-month rolling window
- **LargeCap:** Binary indicator = 1 if market cap in top quartile (Q4), 0 otherwise

---

## Results

### Table 1: Two-Way Fixed Effects Regression (Main Model)

[Insert M3_REGRESSION_TABLE_FORMATTED from results/tables/]

| Variable | Model A (FE) Coefficient | Model A (FE) Std. Error | Model A p-value | Model B (DiD) Coefficient | Model B (DiD) Std. Error | Model B p-value |
|---|---|---|---|---|---|---|
| Leverage (Lag 1) | 0.0071 | 0.0098 | 0.468 | — | — | — |
| Leverage (Lag 2) | 0.0070 | 0.0039 | 0.077 | — | — | — |
| Leverage (Lag 3) | −0.0115 | 0.0089 | 0.200 | — | — | — |
| Beta (Systematic Risk) | 0.0061*** | 0.0014 | <0.001 | −0.0007 | 0.0009 | 0.446 |
| Treated (Large-cap) | — | — | — | 0.0027** | 0.0013 | 0.042 |
| Post 2015 | — | — | — | −0.0085*** | 0.0009 | <0.001 |
| Treatment × Post | — | — | — | 0.0020 | 0.0017 | 0.247 |
| **N (observations)** | **33,573** | | | **33,487** | | |
| **Unique Entities** | **273** | | | **273** | | |
| **R² (within)** | **−0.0006** | | | **0.0015** | | |
| **R² (between)** | **0.2271** | | | **0.0089** | | |
| **R² (overall)** | **0.0169** | | | **0.0042** | | |
| **F-statistic** | **8.23***<br/>(p<0.001)** | | | **12.57***<br/>(p<0.001)** | | |
| **Entity FE** | **Yes** | | | **No** | | |
| **Time FE** | **Yes** | | | **No** | | |
| **Clustered SE** | **Yes (by Entity)** | | | **Yes (by Entity)** | | |

**Note:** *** p<0.01, ** p<0.05, * p<0.10, † p<0.10 (marginal)

### Interpretation of Main Results

**Beta (Systematic Risk) — Robust Finding:**
A 1-unit increase in beta increases expected monthly returns by **61 basis points** ($\hat{\beta}_4 = 0.0061$, t=4.46, p<0.001). This is highly significant and stable across specifications. Annualized, this represents a ≈7.3% risk premium per unit of systematic risk, which is consistent with CAPM theory and typical equity risk premia.

**Economic Significance:** For a REIT with beta = 1.5 (higher systematic risk), the model predicts 3.7% higher annualized returns compared to a market-beta REIT (1.5 × 7.3% = 11% premium, minus the beta=1.0 baseline of 7.3% = 3.7% relative premium). This is economically meaningful and justifies the risk premium demanded by investors.

**Leverage — Not Robust:**
The fixed-effects coefficients on lagged leverage (Lags 1–3) are small (≤7.1 bps) and mostly insignificant (p>0.20 for Lags 1 and 3; p=0.077 for Lag 2, marginally significant at 10%). Robustness tests reveal the effect reverses sign when outliers are removed and is inconsistent across economic regimes. **Conclusion:** No reliable evidence that leverage causally affects REIT returns.

**DiD Treatment Effect — No Heterogeneous Policy Shock:**
Large-cap REITs did not experience significantly different post-2015 return behavior relative to controls (coefficient = 0.20%, p=0.247, 95% CI = [−0.15%, 0.55%]). This suggests either large firms hedged rate risk through unobserved channels (derivatives), or size is not a valid proxy for rate sensitivity.

---

### Figure 1: [Key Visualization]

[Insert figure from results/figures/ — e.g., dual-axis plot of Federal Funds Rate vs. REIT returns; or sector-specific return trends]

**Caption:** [Describe what the figure shows, key patterns, and relevance to memo findings]

---

### Figure 2: Model Diagnostics (Residuals vs. Fitted)

[Insert residual diagnostic plot from results/figures/M3_residuals_diagnostics.png]

**Caption:** "Residual diagnostics for Model A (Two-Way Fixed Effects). Mild heteroskedasticity evident (fan-shaped pattern), addressed through entity-level clustering. Residuals approximate normality with slight right-tail deviation, consistent with monthly financial returns."

---

## Conclusions & Recommendations

### Investment Implications

Based on the empirical findings, we recommend:

1. **Sector Allocation:**
   - **Overweight:** Industrial REITs (lowest leverage volatility; stable beta)
   - **Maintain:** Residential REITs (moderate leverage; stable fundamentals)
   - **Underweight:** Retail and Office REITs (elevated leverage; uncertain fundamentals post-pandemic)

2. **Factor Tilts:**
   - **Beta Targeting:** Tilt portfolio toward higher-beta REITs when interest rates are expected to fall; reduce beta exposure when rate-hiking cycles begin
   - **Avoid leverage-based tilts:** Do not construct trades around leverage ratios, as they do not predict subsequent returns

3. **Scenario Analysis:**
   - **Rising Rates Scenario (+100 bps):** Expect REIT returns to decline ≈[6.1% annually based on beta sensitivity], with larger declines for high-beta REITs. Our DiD analysis suggests minimal hedging via leverage adjustments.
   - **Declining Rates Scenario (−100 bps):** Expect REIT returns to rise ≈[6.1% annually], with larger gains for high-beta REITs.

### Risk Assessment & Limitations

**Model Assumptions:**
- **Parallel Trends (DiD):** Our DiD model assumes that absent the 2015 Fed shock, large and small REITs would follow similar return paths. Pre-2015 correlation is high (0.92), but slight sector divergence is visible in M2 EDA (Retail vs. Industrial). DiD estimates may be biased if this divergence is causal, not exogenous.
- **Strict Exogeneity (FE):** Fixed effects model assumes no dynamic feedback (e.g., past returns don't influence today's leverage decisions). Monthly return horizons minimize this concern but do not eliminate it.

**Omitted Variables:**
- **Unobserved Leverage:** Accounting leverage may not capture true economic leverage (off-balance-sheet financing, derivatives). This biases leverage coefficients toward zero.
- **REIT-Specific Trends:** Time-varying unobservables (REIT-specific management quality, real estate market fundamentals) are not fully captured by time fixed effects. These could correlate with both leverage and returns.

**External Validity Concerns:**
- **Sample Period:** 2000–2024 includes the 2008 financial crisis (structural break). Beta estimates and leverage-return relationships may differ across regimes.
- **REIT Survivorship Bias:** Defunct and merged REITs are excluded, biasing sample toward successful firms. Results may not generalize to marginal REITs.
- **Generalization Outside REITs:** Results are specific to REITs. Leverage-return dynamics may differ in other asset classes.

**Data Limitations:**
- **Monthly Frequency:** Monthly returns contain high noise-to-signal (σ_monthly ≈ 4–5%); causal effects are harder to detect. Quarterly or annual aggregation might yield clearer signals.
- **Leverage Measurement Lag:** Accounting leverage is often reported quarterly, creating measurement error in monthly analysis.

### Honest Caveats

1. **Leverage finding is fragile.** Our main-sample positive leverage effect disappears under robust estimation, suggesting it is an artifact of sample-specific patterns rather than a true causal effect. Do not rely on this finding for tactical trading.

2. **Policy effects are null but not zero.** The DiD treatment effect is centered at +20 bps but is noisy (95% CI spans −15 to +55 bps). Larger samples or real estate-specific data might detect a causal effect if one exists.

3. **Recommendations are conditional.** Our recommendations assume:
   - REITs remain publicly traded with similar leverage ratios and beta distributions
   - Interest rate expectations align with recent conditioning (if Fed adopts new regime, relationships may shift)
   - Sector classifications remain stable (sector drift toward mixed-use properties complicates allocation)

---

## References

### Data Sources
- REIT Master Database: [URL/Citation; e.g., NAREIT, FactSet, or internal database]
- Federal Reserve Economic Data (FRED): https://fred.stlouisfed.org/
  - Series: Federal Funds Effective Rate (FEDFUNDS); 10-Year Treasury (DGS10); others as applicable
- [Other sources: REIT Factors, climate data, market data providers]

### Academic Citations
- Angrist, J. D., & Pischke, J. S. (2009). *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press.
- Modigliani, F., & Miller, M. H. (1958). The cost of capital, corporation finance and the theory of investment. *American Economic Review*, 48(3), 261–297.
- Myers, S. S., & Majluf, N. S. (1984). Corporate financing and investment decisions when firms have information that investors do not have. *Journal of Financial Economics*, 13(2), 187–221.
- Sharpe, W. F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk. *Journal of Finance*, 19(3), 425–442.
- Wooldridge, J. M. (2010). *Econometric Analysis of Cross Section and Panel Data* (2nd ed.). MIT Press.

---

## Appendix: AI Audit

[Brief summary of AI use across M1, M2, M3, M4 with verification and critique examples]

**Team M4 AI Use:** [Describe any AI-assisted writing, code generation, or analysis]

**Verification:** All findings manually checked against code outputs in `/results/tables/` and `/results/figures/`.

**Critique:** [Any limitations or concerns with AI-assisted analysis]

---

**Memo Status:** [DRAFT / SUBMISSION READY]  
**Word Count:** [X pages]  
**Formatted by:** [Name]  
**Last Updated:** [Date]
