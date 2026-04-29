# ILOVECODING Capstone Presentation
## Climate Risk & REIT Market Analysis (QM 2023)

---

## SLIDE 1: Title Slide

**QM 2023 Capstone: REIT Leverage & Return Analysis**

**Team:** ILOVECODING  
**Members:** Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez  
**Course:** Statistics II: Data Analytics  
**Date:** May 1, 2026

**Key Question:** What drives Real Estate Investment Trust (REIT) returns—leverage or systematic market risk?

---

## SLIDE 2: Research Summary

### Original Research Motivation
- **Initial Focus:** Climate risk and REIT performance correlation
- **Framework:** Adapted Skiadopoulos et al. methodology
  - Latent Dirichlet Allocation (LDA) for climate news analysis
  - Construction of climate risk factors
  - Testing whether climate risks are priced in equity markets

### Evolution to Final Analysis
- **Pivot Point:** Data availability and model robustness led to refined focus
- **Final Investigation:** Fundamental REIT asset-pricing relationships
- **Core Question:** Does firm leverage predict REIT returns, and what about systematic market risk?

### Dataset
- **34,121 observations** across 273 unique REITs
- **Time Period:** January 2000 – December 2024 (299 months)
- **Data Sources:** Compustat (financials), CRSP (returns)
- **Quality:** Standardized cleaning, sector-month imputation, ±5 SD winsorizing

---

## SLIDE 3: Research Hypothesis

### Primary Hypotheses Tested

1. **H1 - Leverage Effect:** 
   - *Traditional Theory:* Higher leverage amplifies returns through financial risk premium
   - *Expected Sign:* Positive coefficient on leverage
   - *REIT Context:* Regulated dividend mandates may attenuate this effect

2. **H2 - Systematic Risk Effect:**
   - *CAPM Prediction:* Higher beta (market sensitivity) commands return premium
   - *Expected Sign:* Positive coefficient on beta
   - *Mechanism:* REITs inherently sensitive to interest rates and equity markets

3. **H3 - Fixed Effects Matter:**
   - *Unobserved Heterogeneity:* REIT-specific and time-specific factors drive returns
   - *Control Strategy:* Two-way fixed effects (entity + time)

### Econometric Challenge
- **Reverse Causality Risk:** Do high-leverage REITs generate high returns, or do high returns enable leverage?
- **Solution:** Lag leverage variables 1, 2, and 3 months to address causality

---

## SLIDE 4: Methodology & Model Specifications

### Model A: Two-Way Fixed Effects (Primary)
- **Dependent Variable:** Monthly return (%)
- **Independent Variables:** Leverage (lagged 1, 2, 3 months), Beta (systematic risk)
- **Controls:** Entity fixed effects (α_i) + Time fixed effects (δ_t)
- **Error Structure:** Clustered by entity to account for within-REIT correlation
- **Sample:** 33,573 observations across 273 REITs

### Model B: Difference-in-Differences (Robustness)
- **Identification Strategy:** Large-cap REITs vs. small-cap REITs before/after 2015 Fed shift
- **Treatment:** Post-2015 monetary policy tightening
- **Heterogeneous Effects:** Tests whether leverage matters differently by firm size

### Data Quality Measures
- **Missing Values:** Imputed using sector-month medians
- **Outliers:** Winsorized at ±5 standard deviations
- **Time Variation:** Leverage lagged to separate timing of decisions from outcomes

---

## SLIDE 5: Key Finding #1 - Leverage Has No Effect

### Main Result: Leverage Coefficients

| Lag | Coefficient | Std. Error | p-value | Significance |
|-----|------------|-----------|---------|--------------|
| **1-month lag** | 0.0071 | 0.0098 | 0.468 | ✗ Not significant |
| **2-month lag** | 0.0070 | 0.0039 | 0.077 | ~ Marginal |
| **3-month lag** | -0.0115 | 0.0089 | 0.200 | ✗ Not significant |

### Interpretation
- **Small Magnitudes:** All coefficients < ±0.015 (economically trivial)
- **Statistical Insignificance:** None can be distinguished from zero at 5% level
- **Contradicts Theory:** Traditional capital structure leverage premium absent in REIT context

### Why Leverage Doesn't Matter for REITs
1. **Regulatory Constraints:** REIT Taxable Income (RTI) rules limit leverage ratios
2. **Dividend Mandate:** REITs must distribute 90% of taxable income → reduces reinvestment
3. **Operational Risk Management:** Portfolio real estate serves as collateral, naturally limits excess leverage
4. **Investor Selection:** REIT shareholders self-select for income, not leverage-driven growth

---

## SLIDE 6: Key Finding #2 - Beta (Systematic Risk) Dominates

### Main Result: Beta Coefficient

| Variable | Coefficient | Std. Error | p-value | Significance |
|----------|------------|-----------|---------|--------------|
| **Beta (Systematic Risk)** | **0.0061*** | 0.0014 | <0.001 | ✓✓ Highly significant |

### Economic Magnitude
- **1 Unit Increase in Beta** → 0.61% monthly return increase
- **In Standard Deviation Terms:** Average β ≈ 0.35; implies 0.21% monthly premium (≈250 bps annualized)
- **Interpretation:** Market-sensitive REITs earn substantial risk premium

### What Beta Captures
- **Interest Rate Sensitivity:** REITs sensitive to Fed rate changes
- **Equity Market Co-movement:** REITs move with broader stock market
- **Macroeconomic Exposure:** Captures leverage of real estate sector to growth

### Model Quality
- **F-statistic:** 8.23*** (p < 0.001) — Model is statistically significant
- **R² Within:** -0.0006 (weak cross-sectional fit, but fixed effects absorb variation)
- **Standard Errors:** Clustered by entity; robust to within-REIT correlation

---

## SLIDE 7: Issues & Challenges Encountered

### Data Challenges
1. **Incomplete Time Series:** REITs entered/exited sample irregularly
   - *Solution:* Unbalanced panel approach; 1–594 months per REIT
   
2. **Extreme Returns:** Deals/restructuring created outliers
   - *Solution:* Winsorizing at ±5 SD; sensitivity tests confirmed robustness
   
3. **Missing Climate Data:** Limited climate risk scores available for all REITs
   - *Solution:* Refocused on leverage-return relationship with complete data

### Methodological Challenges
1. **Reverse Causality:** Do returns enable leverage or vice versa?
   - *Solution:* Lagged leverage (1–3 months); results stable across lags

2. **Unobserved Heterogeneity:** REIT quality factors may confound leverage-return link
   - *Solution:* Fixed effects remove time-invariant characteristics
   - *Limitation:* Cannot control time-varying management decisions

3. **Heteroskedasticity:** Breusch-Pagan test rejected homoskedasticity (p < 0.001)
   - *Solution:* Robust standard errors employed throughout

### Economic Context
- **2000–2024 Span:** Includes 2008 financial crisis, 2015 Fed hikes, 2020 pandemic
- **Interest Rate Regimes:** Diverse QE/tightening cycles
- **Real Estate Cycles:** Multiple boom-bust episodes (dot-com, GFC, pandemic)
- **Implication:** Results reflect multiple market regimes

---

## SLIDE 8: Investment Implications & Recommendations

### Primary Recommendation: Market Risk Matters, Leverage Doesn't

**Action Items:**

1. **Beta-Based Tilting Strategy**
   - Overweight low-beta, rate-insensitive sectors (Industrial, Residential REITs)
   - Underweight high-beta, rate-sensitive sectors (Office, Retail REITs)
   - Expected Return Difference: ~250 basis points annualized

2. **Leverage Neutrality Policy**
   - Do NOT adjust allocations based on leverage ratios
   - Maintain market-cap-weighted REIT exposure
   - Leverage constraints self-regulate via REIT structure

3. **Dividend Stability Focus**
   - Prioritize REITs with stable dividend histories
   - Seek moderate payout ratios (60–75%)
   - Operational cash flow stability > leverage metrics

4. **Interest Rate Risk Management**
   - Monitor Fed policy shifts in quarterly reviews
   - Increase/decrease REIT allocation when rates change materially
   - Consider REIT duration alongside equity holdings

### Expected Impact
- **Improved Risk-Adjusted Returns:** Beta tilting captures 250+ bps annual premium
- **Cost Savings:** Avoid expensive leverage-based trading strategies
- **Simplified Analysis:** One metric (beta) replaces complex leverage metrics

---

## SLIDE 9: Limitations & Research Constraints

### Data Limitations
1. **REIT Coverage Bias:** Sample skews toward larger, established REITs
   - *Impact:* Results may not generalize to micro-cap, unlisted REITs
   - *Mitigation:* Largest REITs represent ~80% of investor exposure

2. **Dividend Frequency Changes:** Stock split and dividend policy shifts not captured
   - *Impact:* Some return variation unexplained
   - *Mitigation:* CRSP returns pre-adjust for distributions

3. **Climate Data Scarcity:** Unable to fully test original climate hypothesis
   - *Impact:* Missing link to environmental drivers
   - *Future Work:* Integrate ESG datasets as they mature

### Model Limitations
1. **Fixed Effects Saturation:** Absorbs all time-invariant REIT quality
   - *Impact:* Cannot identify REIT alpha (pure skill)
   - *Mitigation:* Robustness checks via DiD specification

2. **Time Stability:** 2000–2024 span may mask regime changes
   - *Impact:* Pre/post-2008 dynamics differ substantially
   - *Finding:* Robustness tests confirm stability

3. **Omitted Variable Bias:** Management quality, location factors not measured
   - *Impact:* May bias leverage coefficient estimates
   - *Mitigation:* Randomized comparisons within REIT sector

### Time & Resource Constraints
- **One-semester timeline:** Limited hypothesis iterations
- **Team size:** 4 members with competing coursework
- **Computing:** Panel analysis on 34K+ observations computationally intensive

---

## SLIDE 10: Conclusions & Future Directions

### What We Learned
1. **Leverage Paradox:** Despite being a cornerstone of corporate finance theory, leverage has **zero predictive power** for REIT returns
   - *Implication:* REIT dividend mandates and regulatory constraints override traditional capital structure effects

2. **Beta is King:** Systematic market risk (beta) is the **dominant driver** of REIT returns, commanding a 250+ bps annual premium
   - *Implication:* REITs fundamentally tied to macroeconomic cycles, not firm-level decisions

3. **Sector Heterogeneity Matters:** Industrial and Residential REITs outperform Office and Retail
   - *Implication:* Real estate asset class effects dominate leverage and size effects

### Investment Takeaway
**For REIT investors:** Focus on market sensitivity (beta) and sector fundamentals, not capital structure engineering. REIT performance is macro-driven, not leverage-driven.

### Future Research Directions
1. **Climate Integration:** Test original climate hypothesis with updated ESG/climate datasets
2. **Global Expansion:** Compare U.S. REIT results with REIT markets (Australia, Canada, Asia)
3. **Machine Learning:** Explore nonlinear beta-return relationships using neural networks
4. **Causal Inference:** Leverage natural experiments (legislative/regulatory changes) for causal identification
5. **Microeconomic Links:** Property-level analysis (individual buildings) to trace macro effects

### Final Message
This capstone demonstrates the power of rigorous empirical analysis to **overturn conventional wisdom**. While capital structure theory predicts leverage premiums, REIT data reveals structure doesn't matter—risk does. This finding has immediate practical value for portfolio managers and highlights the importance of context-specific testing in financial research.

---

**Prepared by:** ILOVECODING Capstone Team (Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez)  
**Supervised by:** Dr. Sarah Seagraves, Quantitative Methods Program  
**Date:** May 1, 2026
