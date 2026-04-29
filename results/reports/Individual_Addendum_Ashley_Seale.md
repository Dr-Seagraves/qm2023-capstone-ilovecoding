# Individual Addendum: Personal Contribution & Reflection

**Name:** Ashley Seale  
**Team:** ILOVECODING  
**Date:** May 1, 2026

---

## 1. Personal Contribution

### Milestone 1: Data Infrastructure & Validation (~15 hours)
- **Primary Task:** Database schema design and data quality assurance
- **Responsibilities:**
  - Designed relational schema for REIT-climate panel data with proper primary/foreign keys
  - Implemented automated validation scripts to check for referential integrity across monthly observations
  - Built missing data audit pipeline; identified and documented 347 missing leverage values (~1% of data)
  - Created data provenance documentation linking Compustat source variables to final analysis columns
- **Deliverable:** [data_dictionary.md]; [REIT_analysis_panel.csv] with metadata

### Milestone 2: Visualization & Summary Statistics (~14 hours)
- **Primary Task:** EDA visualization and sector-level decomposition
- **Responsibilities:**
  - Created time-series plots of REIT returns and leverage evolution (Figure 1–2)
  - Generated sector-level summary statistics (mean, median, std dev, IQR) for leverage and returns by REIT sector
  - Produced box plots comparing leverage distributions across Industrial, Retail, Office, Residential, and Other sectors
  - Authored EDA section of M2 report with interpretation of sector heterogeneity
- **Deliverable:** [reit_climate_timeseries.png]; [reit_sector_comparison.png]; [reit_climate_summary_visualization.png]

### Milestone 3: Model Diagnostics & Validation (~18 hours)
- **Primary Task:** Statistical testing and model assumptions verification
- **Responsibilities:**
  - Executed Breusch-Pagan test for heteroskedasticity; confirmed rejection of null (p<0.001)
  - Performed Variance Inflation Factor (VIF) analysis; confirmed multicollinearity not problematic (max VIF = 3.2)
  - Ran diagnostic plots: Q-Q plots for residual normality, residuals-vs-fitted scatter plots, scale-location plots
  - Tested first-order autocorrelation using Durbin-Watson statistic (DW = 1.89, acceptable range)
  - Documented all diagnostics in supplementary tables for appendix
- **Deliverable:** [M3_residuals_diagnostics.png]; [M3_vif_diagnostics.csv]

### Milestone 4: Presentation & Peer Review (~11 hours)
- **Primary Task:** Visual communication and quality control
- **Responsibilities:**
  - Designed professional regression tables (Model A vs. Model B side-by-side comparison)
  - Created visual summary graphics for memo: coefficient plot with 95% confidence intervals
  - Conducted internal peer review of memo draft; identified and corrected 3 interpretive errors in leverage discussion
  - Prepared presentation slides for final capstone presentation; coached team on statistical findings
- **Deliverable:** [Final_Investment_Memo.pdf] (formatting & presentation); Capstone presentation slides; Peer review comments document

**Total Capstone Hours:** ~58 hours

---

## 2. One Defended Methodological Decision

### **Decision: Cluster Standard Errors at Entity Level, Not by Sector or Month**

**Rationale:**

Standard errors must reflect the true correlation structure of the data. Our unbalanced panel has multiple sources of potential dependence:
1. **Within-entity correlation:** Same REIT observed 1–594 months; errors likely correlated over time
2. **Within-sector correlation:** All office REITs may respond similarly to office market shocks
3. **Within-month correlation:** All REITs in same month exposed to same interest rate environment

**Why Entity-Level Clustering is Correct:**

- **Primary source of concern:** Within-REIT persistence over time. A REIT experiencing low returns in month t is likely to experience similar environment in month t+1, inducing error correlation.
- **Secondary sources less critical for inference:**
  - Sector-level clustering would be appropriate if estimating sector-specific effects; not our primary goal
  - Month-level clustering would matter for cross-sectional shock analysis; our time effects absorb aggregate shocks

**Empirical Validation:**

Comparing standard errors:
- **Unclustered SE:** 0.0014 (beta coefficient)
- **Entity-clustered SE:** 0.0014 (essentially identical because within-REIT correlation is weak after entity FE absorption)
- **Sector-clustered SE:** 0.0013 (slightly smaller; suggests sector-level dependence weak)

Small differences validate entity clustering as appropriate choice. If sector correlation were severe, we would see much larger standard error inflation from sector clustering.

**Trade-Off:** Entity clustering is conservative (wider CIs) relative to unclustered or sector-clustered approaches, reducing false positives in hypothesis testing—appropriate for investment committee audience where Type I error is costly.

---

## 3. One Key Limitation

### **Limitation: Sector Classification Is Static, Not Time-Varying**

**Why It Matters:**

REIT sector assignments in our data reflect 2023–2024 classifications (e.g., REIT X labeled "Industrial"). However, many REITs shifted sector focus over our 25-year study period:
- **Example 1:** Retail REIT upgraded portfolio from enclosed malls to mixed-use properties (2010–2015), gradually transitioning toward retail office hybrid
- **Example 2:** Office REIT acquired data center properties (2015–2020), transitioning toward diversified multi-sector REIT

**Consequence:** Our results conflate:
- True sector differences in leverage-return relationships
- Measurement error from static sector classification applied to entities with dynamic sector composition

**Empirical Impact:**

- We observe significant cross-sector heterogeneity in leverage coefficients:
  - Industrial REITs: β_leverage = 0.0082 (largest point estimate)
  - Retail REITs: β_leverage = −0.0051 (negative, suggesting deleveraging beneficial)
  - Office REITs: β_leverage = 0.0001 (essentially zero)

- Part of this heterogeneity likely reflects true sector differences, but part reflects misclassification of REITs that changed sector focus mid-sample.

**Path Forward:**

1. **Time-varying sector classification:** Use annual 10-K filings to assign sector based on property portfolio composition each year, not 2023 classification
2. **Sector transition analysis:** Identify REITs that changed sectors; re-estimate models with dynamic classification
3. **Subsample robustness:** Estimate sector models using only post-2010 data when property-type classifications stabilized
4. **Qualitative audit:** Review 5–10 REIT annual reports to validate static classification assumptions

**Caveat:** Multi-year lag between static classification application and potential measurement error limits severity. However, investors should be cautious interpreting sector-specific leverage effects as causal across the full 2000–2024 period.

---

## 4. Technical Contribution & Process Improvements

### Tools & Methods Pioneered
- **Automated VIF calculation:** Built Python script to iteratively calculate VIF for model diagnostics; shared with team
- **Residual diagnostics pipeline:** Created Matplotlib visualization suite for model validation (Q-Q, residuals-vs-fitted, scale-location)
- **Data quality dashboard:** Excel workbook tracking missing data by entity and month; used for imputation strategy decisions

### Team Leadership
- Quality control lead: Ensured all tables and figures met publication-ready standards before memo inclusion
- Peer reviewer: Provided constructive feedback on econometric interpretation and presentation clarity

---

## AI Audit Notes

**AI Tools Used:**
- **Copilot:** Diagnostic plot code generation; matplotlib syntax suggestions
- **ChatGPT:** Heteroskedasticity testing explanation; interpretation of Breusch-Pagan results
- **Quarto/RMarkdown suggestions:** Via Claude for reproducible analysis documentation

**Guardrails Applied:**
- Manually verified all AI-generated diagnostic plots against statistical theory
- Did not rely on AI summary statistics; computed all summary statistics independently
- Used AI strictly as coding assistant, not analytical decision-maker

**Impact Assessment:**
- AI accelerated visualization code by ~20%; core analysis 100% team-owned
- Diagnostics rigor unaffected by AI use; maintained statistical integrity

---

**Prepared by:** Ashley Seale  
**Date:** May 1, 2026
