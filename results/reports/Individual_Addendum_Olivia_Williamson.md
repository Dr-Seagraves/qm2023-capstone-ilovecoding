# Individual Addendum: Personal Contribution & Reflection

**Name:** Olivia Williamson  
**Team:** ILOVECODING  
**Date:** May 1, 2026

---

## 1. Personal Contribution

### Milestone 1: Data Integration & Sourcing (~17 hours)
- **Primary Task:** Multi-source data acquisition and reconciliation
- **Responsibilities:**
  - Coordinated data requests with Compustat, CRSP, and FRED; navigated access permissions
  - Merged REIT financial data (Compustat) with return data (CRSP) using SIC code and company name matching
  - Integrated Federal Funds Rate and Treasury yield data from FRED as macroeconomic controls
  - Resolved 8 date-mismatch issues between sources; standardized all data to end-of-month frequency
  - Documented data provenance and variable construction in [data_dictionary.md]
- **Deliverable:** [REIT_analysis_panel.csv] (master dataset, 34,121 observations)

### Milestone 2: Sector Analysis & Comparative EDA (~12 hours)
- **Primary Task:** Sector-level heterogeneity analysis
- **Responsibilities:**
  - Calculated sector-specific summary statistics for leverage, returns, market cap, and dividend yield
  - Created [reit_sector_analysis.csv] with sector breakdown: mean leverage by sector (Retail 35.2%, Industrial 32.1%, Office 38.9%)
  - Performed Kruskal-Wallis test comparing leverage distributions across sectors (H = 127.3, p<0.001)
  - Generated bar charts and violin plots comparing sector distributions
  - Identified high-performing sector (Industrial) and underperforming sector (Office); integrated into M2 narrative
- **Deliverable:** [reit_sector_analysis.csv]; M2 sector analysis section

### Milestone 3: Alternative Model Development (~17 hours)
- **Primary Task:** Difference-in-Differences specification and interpretation
- **Responsibilities:**
  - Specified DiD model comparing large-cap REITs (top market-cap quartile) to peers before/after 2015 Fed tightening
  - Estimated parallel-trends assumption visually; created pre-treatment trend plot confirming validity
  - Interpreted treatment effect (interaction coefficient): β_treat = 0.0020, not significant (p=0.247)
  - Calculated heterogeneous treatment effects by REIT maturity (established vs. newer)
  - Documented robustness: results stable when using 2014 or 2016 as alternative treatment date
- **Deliverable:** [M3_model_B_results.csv]; Model B interpretation section of memo

### Milestone 4: Final Memo & Recommendations (~13 hours)
- **Primary Task:** Business translation and strategic recommendations
- **Responsibilities:**
  - Drafted Methodology section with lay-friendly variable definitions
  - Wrote Conclusions & Investment Implications: converted econometric findings into actionable recommendations
  - Created 3-part investment strategy: beta-tilting approach, leverage neutrality, dividend stability focus
  - Incorporated limitations discussion; advised committee on appropriate caution in interpreting non-causal results
  - Edited and refined all sections for clarity, consistency, tone
- **Deliverable:** [Final_Investment_Memo.pdf] (Methodology, Conclusions, Investment Recommendations sections)

**Total Capstone Hours:** ~59 hours

---

## 2. One Defended Methodological Decision

### **Decision: Use Difference-in-Differences Specification to Test Heterogeneous Effects, Not Just Overall Model**

**Rationale:**

Traditional two-way FE model estimates average leverage effect across all REITs and time periods. But leverage-return relationship may differ by firm size and macroeconomic regime:
- **Large-cap REITs:** Greater access to debt markets; leverage increases may signal strong capital allocation discipline
- **Small-cap REITs:** Limited refinancing options; high leverage may signal financial distress
- **Low-rate environment (pre-2015):** Leverage-induced risk justified by low risk-free rate; high leverage economically rational
- **High-rate environment (post-2015):** Leverage costs rise sharply; high leverage becomes risky

**Model Design:**

$$\text{Return}_{it} = \beta_0 + \beta_1 \text{LargeCap}_i + \beta_2 \text{Post2015}_t + \beta_3 (\text{LargeCap}_i \times \text{Post2015}_t) + \beta_4 \text{Beta}_{it} + \varepsilon_{it}$$

- **LargeCap_i = 1** if market cap in top quartile (≥$3.2B); 0 otherwise
- **Post2015_t = 1** if observation after December 2014; 0 otherwise
- **Interaction term:** Captures whether large-cap REITs experienced different returns post-2015

**Findings:**

- **LargeCap effect:** β_1 = 0.0027** (p=0.042): Large-cap REITs higher returns by ~27 bps/month on average
- **Post-2015 effect:** β_2 = −0.0085*** (p<0.001): All REITs lower returns post-2015 (~85 bps/month decline)
- **Treatment effect (DiD):** β_3 = 0.0020 (p=0.247): Large-caps did NOT experience differential impact; parallel trends hold

**Economic Interpretation:** Fed tightening 2015+ affected all REITs equally; large-cap advantage persists unchanged. This suggests leverage-rate sensitivity is not size-dependent during monetary policy shifts.

**Why This Specification Matters:** Simple FE model would miss this key insight. DiD adds statistical power to detect differential effects, improving confidence in "no interaction found" conclusion.

---

## 3. One Key Limitation

### **Limitation: Unbalanced Panel with Differential Coverage Across Entities**

**Why It Matters:**

Our 273 REITs have highly unequal time coverage:
- **Longest entity:** 594 months (nearly full 2000–2024 sample)
- **Shortest entity:** 1 month (single observation in database)
- **Median entity:** 71 months (~6 years)

**Consequence:** Estimation gives equal weight to each observation, implying:
- Long-standing, stable REITs (594 observations) weighted equally per observation as startup REITs (1 observation)
- Survivor bias: REITs that entered and exited sample may differ systematically from continuously operating REITs
- Time-varying composition of REIT universe may induce time-varying omitted variable bias

**Empirical Impact:**

- **Composition effects:** In 2000, sample includes 87 REITs; by 2024, sample includes 182 REITs. Newer REITs tend smaller and riskier; leverage-return relationship may differ
- **Survivor bias:** REITs exiting sample likely performed poorly (bankruptcy, merger, delisting). Excluding their negative returns during exit period could bias results upward
- **Unbalanced power:** Large-cap REITs overrepresented in sample (more months of data); results may skew toward large-cap patterns

**Illustration with Numbers:**

Among 33,573 observations in main model:
- Top 25% of REITs by tenure account for ~60% of observations
- Bottom 25% of REITs by tenure account for ~5% of observations

This weight concentration could be attenuating coefficients on REITs entering late or exiting early.

**Path Forward:**

1. **Balanced subsample:** Estimate models using only balanced panel of 47 REITs with complete 2000–2024 data; compare coefficients to unbalanced main results
2. **Weighted regression:** Employ probability-weighted estimation giving equal weight to each REIT-year (not each REIT-month), reducing influence of long-tenure REITs
3. **Cohort analysis:** Stratify by REIT entry year; test whether leverage-return relationship differs for 1990s entrants vs. 2010s entrants
4. **Sensitivity analysis:** Re-estimate dropping bottom quartile of short-tenure REITs; verify findings robust

**Caveat:** Balanced subsample n=47 REITs may be too small for precise inference; unbalanced approach is standard practice. However, robustness checks recommended before publishing findings.

---

## 4. Cross-Functional Impact & Project Organization

### Strategic Contributions
- **Data governance:** Established standardized data protocols used throughout project
- **Sector expertise:** Drove sector-level analysis; identified Office REIT underperformance as key finding
- **Stakeholder communication:** Translated econometric results into plain English for investment committee audience

### Key Accomplishments
- Resolved complex data reconciliation issues early; prevented cascading errors in M2/M3
- Championed DiD specification; added nuance to findings by testing heterogeneous effects
- Wrote investment recommendations in business language; made capstone accessible to practitioners

---

## AI Audit Notes

**AI Tools Used:**
- **ChatGPT (GPT-4):** Data source guidance; help drafting methodology descriptions
- **GitHub Copilot:** Data reshaping code for sector analysis; pandas operations
- **Claude:** Business-language translation of econometric terms; memo writing structure

**Responsible AI Use:**
- Independently verified all sector statistics before incorporation
- Did not rely on AI for numerical results; AI used for writing and coding only
- Kept all analytical decisions team-owned

**AI Value-Add:**
- Accelerated memo drafting by ~25%; freed time for substantive analysis
- Code suggestions reduced debugging time for data reshaping tasks
- Writing suggestions improved clarity without changing interpretation

---

**Prepared by:** Olivia Williamson  
**Date:** May 1, 2026
