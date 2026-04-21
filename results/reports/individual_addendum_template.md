# Individual Addendum Template: Personal Contribution & Reflection

**Name:** [Your Name]  
**Team:** ILOVECODING  
**Date:** May 1, 2026  

---

## 1. Personal Contribution

Provide 2–4 bullets describing your contributions across Milestones 1–4. Be specific: include tasks, hours, and deliverables you owned.

**Example:**
- **Milestone 1 (Data Cleaning & Merge):** Led REIT financial data cleaning; implemented missing value imputation for leverage variables; merged FRED Federal Funds Rate with REIT panel using year_month keys. Handled duplicate entity matches and verified referential integrity. **15 hours**
- **Milestone 2 (EDA & Visualization):** Conducted exploratory analysis of leverage-return correlations; created lag-correlation heatmaps (Figure 3); drafted methodology section of M2 findings report; identified lag-2 as strongest predictor. **12 hours**
- **Milestone 3 (Econometric Modeling):** Implemented two-way fixed effects model in PanelOLS; ran Breusch-Pagan heteroskedasticity test; conducted robustness checks (outlier sensitivity, time-period stability); interpreted beta coefficient. **18 hours**
- **Milestone 4 (Final Memo):** Drafted Executive Summary and Results section; created formatted regression tables (CSV + Excel); synthesized M1–M3 findings for business audience; incorporated peer feedback. **10 hours**

**Total Capstone Hours:** ~55 hours

---

## 2. One Defended Methodological Decision

Choose one methodological choice you made or strongly advocated for. Explain your reasoning with evidence from prior milestones.

**Example:**

*Decision: Use 1–3 month lags for leverage, not contemporaneous levels.*

**Reasoning:** In Milestone 2, initial lag-correlation analysis showed that contemporaneous leverage has weak correlation with returns (r ≈ 0.05), while 1–3 month lagged leverage exhibits stronger correlation (r ≈ 0.08–0.12). This pattern is consistent with economic theory: leverage changes take 1–2 months to affect REIT financing costs and market perceptions. Additionally, we wanted to avoid reverse causality (returns affecting same-month leverage decisions), which lagging naturally prevents. The choice sacrifices some sample size (loss of first 3 months per entity) but gains causal identification and interpretability. Robustness checks (dropping Lag 1, dropping Lag 3) confirmed estimates are stable to lag specification, validating this choice.

---

## 3. One Key Limitation

Identify the most important limitation or caveat of your analysis. Explain why it matters and how it could affect conclusions.

**Example:**

*Limitation: Fixed Effects model assumes unobserved heterogeneity is time-invariant.*

**Why It Matters:** Our entity fixed effects (α_i) absorb time-invariant REIT characteristics (management quality, sector specialization, dividend policy), but time-varying unobservables (e.g., REIT-specific leadership changes, property portfolio shifts) remain in the error term. If these time-varying factors correlate with both leverage and returns, our leverage coefficient will be biased. For instance, if a REIT's leverage increases because it recently hired a growth-focused CFO (unobserved), and this same CFO drives higher returns, we would overestimate the causal effect of leverage on returns.

**How To Address:** Placebo tests using pre-shock periods, or incorporating real estate fundamentals (property occupancy rates, rent growth) would help isolate the leverage effect from unobserved quality changes. This is a limitation of our current analysis and suggests conservative interpretation of leverage findings (which is why our memo appropriately discounts the leverage result).

---

## 4. AI Audit Notes (If Applicable)

If you used AI (ChatGPT, Claude, GitHub Copilot, etc.) for any specific work, document it here. Include:
- **What task:** (e.g., "Drafted initial memo structure")
- **What prompt:** (brief description of what you asked)
- **What output:** (what the AI produced)
- **How you verified:** (how you checked the output wasn't hallucinating or wrong)
- **What you changed:** (manual edits or corrections you made)

**Example:**

*Task:* Formatting regression table for publication-ready presentation

*Prompt:* "Generate a Python script to format regression output with coefficients, standard errors in parentheses, significance stars, and summary statistics."

*Output:* AI produced `format_regression_tables.py` with mostly correct structure, but had errors in significance-star logic (was checking t-stats instead of p-values).

*Verification:* Ran the script on actual M3 output; compared coefficients manually against statsmodels summary output to ensure no copy errors; checked significance calls against known p-value thresholds.

*Changes:* Fixed p-value threshold logic (changed `if t_stat > 2` to `if p_value < 0.05`); added manual verification of a few key coefficients (beta = 0.0061, p<0.001) against original statistical output.

---

**Status:** ✓ COMPLETE

**Submission Date:** May 1, 2026 by 11:59 PM
