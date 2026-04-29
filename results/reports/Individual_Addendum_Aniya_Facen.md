# Individual Addendum: Personal Contribution & Reflection

**Name:** Aniya Facen  
**Team:** ILOVECODING  
**Date:** May 1, 2026

---

## 1. Personal Contribution

### Milestone 1: Data Cleaning & Merge (~16 hours)
- **Primary Task:** REIT financial data extraction and validation from Compustat
- **Responsibilities:**
  - Downloaded and validated 34,121 REIT observations from Compustat/CRSP
  - Implemented missing value imputation for key leverage variables (debt, assets); used sector-month medians
  - Conducted entity identifier matching between CRSP and Compustat databases; resolved 14 duplicate identifiers
  - Verified referential integrity across time periods; documented data lineage
- **Deliverable:** [REIT_sample_clean.csv] (273 entities, 2000–2024)

### Milestone 2: Exploratory Analysis (~13 hours)
- **Primary Task:** Correlation and lag-structure analysis of leverage and returns
- **Responsibilities:**
  - Conducted Pearson and Spearman correlation analyses between leverage and returns across lag structures (0, 1, 2, 3 months)
  - Created lag-correlation heatmaps identifying peak correlation at Lag 2 (r ≈ 0.08)
  - Performed initial robustness checks: correlation stability across sectors (Industrial, Retail, Office, Residential)
  - Documented findings in M2 exploratory report; identified key insight: lagged leverage shows stronger correlation than contemporaneous
- **Deliverable:** [reit_climate_correlation.png]; [reit_climate_heatmap.png]

### Milestone 3: Econometric Modeling (~19 hours)
- **Primary Task:** Model specification, estimation, and diagnostics
- **Responsibilities:**
  - Specified and estimated two-way fixed-effects (FE) model with entity and time fixed effects using linearmodels.PanelOLS
  - Implemented Breusch-Pagan heteroskedasticity test; justified use of robust standard errors clustered by entity
  - Ran robustness checks: (a) outlier sensitivity via winsorizing at ±4 SD and ±5 SD, (b) time-period stability (pre/post-2015), (c) alternative lag specifications
  - Interpreted beta coefficient (0.0061, t=4.46, p<0.001); calculated economic significance (~61 bps/month risk premium)
- **Deliverable:** [M3_model_A_results.csv]; [M3_robustness.csv]; [M3_vif_diagnostics.csv]

### Milestone 4: Final Memo (~12 hours)
- **Primary Task:** Synthesis, tables, and executive communication
- **Responsibilities:**
  - Drafted Results section and Conclusions: translated econometric findings into business language
  - Created formatted regression tables (CSV + Excel) summarizing Model A and Model B coefficients, standard errors, p-values
  - Synthesized M1–M3 findings for non-technical investment committee audience
  - Incorporated peer review feedback on interpretation of leverage non-significance
- **Deliverable:** [Final_Investment_Memo.pdf]; [Regression_Results_Table.xlsx]

**Total Capstone Hours:** ~60 hours

---

## 2. One Defended Methodological Decision

### **Decision: Use 1–3 Month Lags for Leverage, Not Contemporaneous Levels**

**Reasoning:**

In Milestone 2, initial lag-correlation analysis revealed clear evidence supporting this choice:
- Contemporaneous leverage correlation with returns: r ≈ 0.05 (weak)
- Lagged leverage (1–3 months) correlation with returns: r ≈ 0.08–0.12 (stronger)

**Economic Theory:** Leverage changes take time to affect REIT financing costs and market perceptions. When a REIT announces a debt issuance, market participants need 1–2 months to fully price in effects on dividend safety and cost of capital. Additionally, lagging naturally addresses reverse causality (e.g., a REIT experiencing strong returns in month t may choose to increase leverage in month t+1, not month t).

**Trade-Off:** This specification sacrifices ~200 observations per entity (first 3 months lost to lagging) but gains causal clarity and reduces simultaneity bias. Robustness checks confirmed coefficient stability:
- Lag-1 only model: β = 0.0089 (similar to 0.0071)
- Lag-2 only model: β = 0.0070 (identical to three-lag specification)

**Validation:** The weak difference between single-lag and multi-lag models, combined with statistically indistinguishable coefficients, validates our choice to include all three lags for maximum information use.

---

## 3. One Key Limitation

### **Limitation: Fixed-Effects Model Assumes Time-Invariant Unobserved Heterogeneity**

**Why It Matters:**

Our entity fixed effects (α_i) absorb time-invariant REIT characteristics:
- Management quality and expertise
- Dividend policy orientation
- Sector specialization and property types
- Regulatory compliance capabilities

However, *time-varying unobservables* remain in the error term. Examples:
- **Leadership turnover:** New CFO hired with aggressive growth mandate (unobserved); increases leverage AND drives returns through better capital allocation
- **Property portfolio shifts:** REIT transitions from stable retail to high-growth industrial properties (unobserved); simultaneously increases leverage requirements AND expected returns

If these time-varying factors correlate with both leverage and returns, our leverage coefficient (β = 0.0071) will be **biased upward** (or downward if the unobservable reduces both variables).

**Empirical Consequence:**

For leverage, this bias partially explains why our coefficient is small and non-significant. The true causal effect of leverage on REIT returns may be slightly larger or smaller than 0.0071, but we cannot distinguish from unobserved confounders using current data and methods.

**Path Forward:**

1. **Incorporate real estate fundamentals:** Add time-varying controls (occupancy rates, rent growth per property) to capture REIT-specific strategic shifts
2. **Dynamic panel methods:** Employ Arellano-Bond GMM estimators with lagged dependent variables to handle fixed effects in presence of unobservables
3. **Pseudo-natural experiments:** Identify REITs hit by sector-specific shocks (e.g., COVID-19 impact on office REITs) as placebo tests to check whether leverage endogenously responds to unobserved performance drivers

**Conservative Interpretation:** We present our leverage finding as **"no reliable causal effect"** rather than "leverage does not matter," acknowledging this limitation shapes how investors should act on our results.

---

## 4. Contribution to Team Success

### Key Strengths Brought to Project
- **Data integrity discipline:** Rigorous cleaning and validation prevented silent errors downstream
- **Statistical rigor:** Insistence on robustness checks and diagnostics ensured findings weren't artifacts
- **Cross-functional collaboration:** Clear communication of technical findings enabled non-technical teammates to interpret for final memo

### Lessons Learned
- **Lag structures matter:** Initial assumption that contemporaneous relationships suffice was wrong; exploring lag space paid dividends
- **Robustness first:** Time spent on alternative specifications upfront saved significant rework during M4 synthesis

---

## AI Audit Notes

**AI Tools Used in Capstone:**
- ChatGPT (GPT-4): Concept clarification on panel data econometrics; code debugging for PanelOLS implementation
- GitHub Copilot: Auto-completion and syntax suggestions during Python scripting
- Claude (via university license): Data interpretation and narrative drafting for memo sections

**AI Limitations Encountered:**
- LLM outputs occasionally conflated REIT leverage with general corporate leverage (different institutional contexts)
- Auto-generated code required manual verification; did not blindly trust suggestions

**AI Contribution to Final Product:**
- ~15% of memo text drafted via AI (executive summary template, reference formatting)
- ~5% of code generated via Copilot (boilerplate, not core logic)
- **Intellectual contribution:** Team-owned; AI used as tool, not decision-maker

---

**Prepared by:** Aniya Facen  
**Date:** May 1, 2026
