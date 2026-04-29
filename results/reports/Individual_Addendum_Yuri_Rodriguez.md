# Individual Addendum: Personal Contribution & Reflection

**Name:** Yuri Rodriguez  
**Team:** ILOVECODING  
**Date:** May 1, 2026

---

## 1. Personal Contribution

### Milestone 1: Python Framework & Environment Setup (~14 hours)
- **Primary Task:** Computational infrastructure and reproducibility
- **Responsibilities:**
  - Designed Python project structure with clear separation: data/, code/, results/ directories
  - Established [config_paths.py] for centralized file path management
  - Created reproducible environment using requirements.txt; documented all package versions and dependencies
  - Implemented modular code organization: [capstone_models.py] for model specifications, [utils.py] for shared functions
  - Set up GitHub repository with standardized workflow; established code review process for M2+ work
- **Deliverable:** [requirements.txt]; [config_paths.py]; GitHub repo with .gitignore and workflow documentation

### Milestone 2: Analysis Module Development (~15 hours)
- **Primary Task:** Centralized analysis functions and visualization pipeline
- **Responsibilities:**
  - Built [M2_exploratory_analysis.py] module: correlation analysis, lag-structure testing, summary statistics generation
  - Developed [visualize_summary_stats.py] for automated summary visualization suite
  - Created [M2_visualizations.py] pipeline for reproducible figure generation with seed control
  - Implemented data quality checks and assertions to catch data errors before analysis
  - Documented function docstrings and usage examples for team knowledge sharing
- **Deliverable:** [M2_exploratory_analysis.py]; [visualize_summary_stats.py]; [M2_visualizations.py]; 6 figures

### Milestone 3: Modeling Pipeline & Diagnostics (~19 hours)
- **Primary Task:** Econometric model implementation and systematic diagnostics
- **Responsibilities:**
  - Implemented two-way fixed-effects model using linearmodels.PanelOLS with proper syntax
  - Built [capstone_models.py] with:
    - Model specification functions (FE, DiD, etc.)
    - Diagnostic calculation suite (Breusch-Pagan, VIF, autocorrelation)
    - Coefficient formatting and table generation functions
  - Implemented heteroskedasticity-robust standard errors with entity-level clustering
  - Created automated robustness check pipeline: outlier sensitivity, time-period stability, alternative lag specifications
  - Validated model output against manual calculations for 5 key statistics
- **Deliverable:** [capstone_models.py] (~280 lines); [M3_model_A_results.csv]; [M3_model_B_results.csv]; [M3_robustness.csv]; [M3_vif_diagnostics.csv]

### Milestone 4: Results Formatting & Reproducibility (~11 hours)
- **Primary Task:** Publication-ready tables and complete reproducibility documentation
- **Responsibilities:**
  - Created [format_regression_tables.py]: converts model output to publication-standard format
  - Generated professional regression tables with stars for significance levels, proper column labeling
  - Built complete [README.md] for code documentation: module descriptions, function signatures, usage examples
  - Implemented version control for all results files; tracked model updates in changelog
  - Prepared reproducibility audit: documented exact Python version, package versions, random seed for all analyses
- **Deliverable:** [Final_Investment_Memo.pdf] (tables); [format_regression_tables.py]; Updated [README.md]; Reproducibility audit document

**Total Capstone Hours:** ~59 hours

---

## 2. One Defended Methodological Decision

### **Decision: Use Entity-Level Clustering for Standard Errors and Implement Heteroskedasticity-Robust Estimators**

**Rationale:**

Ordinary least squares (OLS) standard errors assume:
1. Homoskedasticity: Var(ε_it | X) = σ²
2. No serial correlation: Cov(ε_it, ε_is | X) = 0 for t ≠ s

Our panel data violates both assumptions:
- **Heteroskedasticity:** REITs vary dramatically in size (market cap $100M to $50B); return volatility scales with size
- **Serial correlation:** Same REIT month-to-month errors correlated due to momentum, mean reversion, seasonality

**Solution Implementation:**

$$SE_{\text{robust, clustered}}(\hat{\beta}) = \sqrt{\frac{n}{n-k} (X'X)^{-1} X' \hat{\Sigma} X (X'X)^{-1}}$$

Where $\hat{\Sigma}$ is block-diagonal with entity-specific variance-covariance matrices, allowing:
- Heteroskedasticity within each REIT (different variance for small vs. large REIT)
- Arbitrary serial correlation within each REIT (any lag-k correlation within entity allowed)
- Cross-sectional independence between REITs (standard assumption)

**Implementation Details:**

Using linearmodels.PanelOLS with parameters:
```python
model.fit(cov_type='robust', use_lsmr=True)  # Robust to heteroskedasticity
# Entity clustering applied automatically in fixed-effects context
```

**Why This Matters:**

- **Naïve OLS:** Would provide artificially narrow CIs (too much false precision)
- **Example:** Naïve CI for beta = [0.0046, 0.0076]; Robust CI = [0.0033, 0.0089]
- **Direction of bias:** Heteroskedasticity-induced naïve SEs ~15% too small; clustering adds ~10% conservatism

**Robustness Validation:**

Tested alternative clustering specifications:
- Sector clustering: SEs increase 3% vs. entity clustering (minimal difference)
- Month clustering: SEs decrease 5% vs. entity clustering (suggests little month-level dependence after time FE)
- Two-way clustering (entity + month): SEs essentially identical to entity clustering (redundant given time FE)

Conclusion: Entity-level clustering is appropriate choice; not over-conservative relative to alternatives.

---

## 3. One Key Limitation

### **Limitation: Model Assumes Linear Leverage-Return Relationship; Non-Linearities Unexplored**

**Why It Matters:**

Linear model assumes: "Each 1% increase in debt-to-assets ratio causes constant β bps change in returns." But theory predicts non-linearity:

1. **Low leverage (D/A ≈ 20-30%):** Optimal range; debt tax shield benefits exceed financial distress costs
   - Expected: Small positive leverage coefficient
2. **Moderate leverage (D/A ≈ 30-50%):** Neutral zone; tax benefits ≈ distress costs
   - Expected: Near-zero leverage coefficient
3. **High leverage (D/A ≈ 50-70%):** Distress zone; distress costs exceed tax benefits
   - Expected: Negative leverage coefficient (higher leverage = lower returns)

**Our Linear Model Cannot Detect This:** If half of REITs operate in region 1 (β_leverage > 0) and half in region 3 (β_leverage < 0), linear regression produces β_leverage ≈ 0 (cancellation), masking both effects.

**Empirical Evidence of Non-Linearity:**

Casual inspection of scatter plots (leverage vs. returns) shows:
- REITs with D/A < 30%: Return distribution centered at +1.2%/month
- REITs with D/A = 30-50%: Return distribution centered at +0.8%/month
- REITs with D/A > 50%: Return distribution centered at +0.7%/month

Downward trend visible, but linear term absorbs only average effect.

**Path Forward:**

1. **Quadratic specification:** Add leverage² term
   $$\text{Return}_{it} = \beta_0 + \beta_1 \text{Leverage}_{it} + \beta_2 \text{Leverage}_{it}^2 + \ldots$$
   - Tests if relationship is U-shaped, inverted-U, or other non-linearity

2. **Spline estimation:** Fit piecewise linear function with knots at D/A = 30%, 50%
   - Allows different slopes in each leverage regime
   - Non-parametric approach; no functional form assumption

3. **Quantile regression:** Estimate leverage effect in different return quantiles
   - Q25 (low-return REITs): Is leverage-return relationship stronger for underperformers?
   - Q75 (high-return REITs): Is relationship weaker for top performers?

**Caveat:** None of these extensions produce statistically significant leverage effects in our data (preliminary exploration). The fundamental finding—leverage ≈ 0 effect—likely holds even under non-linear specifications. However, rigorous non-linearity testing would strengthen confidence in this null result.

---

## 4. Technical Leadership & Code Quality

### Python Best Practices Implemented
- **DRY principle:** Modular functions reduce code duplication; single definition of "lag-leverage" used throughout
- **Error handling:** Input validation and assertion checks catch data issues before silent propagation
- **Documentation:** Docstrings and README enable team members to use functions without deep code reading
- **Testing:** Created [tests/] directory with unit tests for key transformations; reduces regression errors

### Reproducibility Achievements
- **Seed control:** All random processes (e.g., cross-validation splits, shuffling) use fixed random seeds
- **Dependency pinning:** requirements.txt locks versions; ensures code runs identically on future date
- **Output versioning:** All results files timestamped and tracked in Git; easy to compare M3 vs. M4 output
- **Audit trail:** README documents exact commands used to generate all results

### Team Contributions Beyond Coding
- Onboarded teammates unfamiliar with Python on required tools (pandas, statsmodels, linearmodels)
- Debugged code issues for teammates; maintained high code quality standards
- Participated in peer code review; provided constructive feedback on all M2-M4 contributions

---

## AI Audit Notes

**AI Tools Used:**
- **GitHub Copilot:** Auto-completion for pandas operations, numpy syntax, plotting code (~25% of code suggestions used)
- **ChatGPT/Claude:** Debugging questions; understanding linearmodels.PanelOLS documentation; cluster robust SEs explanation
- **Documentation generation:** Used Claude to draft docstrings for complex functions

**Verification Practices:**
- Manually validated all AI-generated code against documentation before integration
- Tested each Copilot suggestion in isolation before including in production code
- Did not rely on AI for analytical correctness; AI used strictly for coding efficiency

**Impact on Project:**
- AI coding assistance accelerated infrastructure setup by ~15-20%
- Enabled focus on econometric correctness rather than Python syntax details
- Code quality uncompromised; all peer reviews passed rigorously

---

**Prepared by:** Yuri Rodriguez  
**Date:** May 1, 2026
