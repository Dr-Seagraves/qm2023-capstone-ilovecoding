# Econometric Hypotheses for REIT Panel Models

## Objective
Define clear, testable hypotheses for monthly REIT return models using your panel data (1986–2024).

## Baseline Model Framework
Use firm and time fixed effects as the default specification:

\[
usdret_{i,t} = \alpha + \beta_1 debt\_at_{i,t-1} + \beta_2 beta_{i,t-1} + \beta_3 roe_{i,t-1} + \beta_4 btm_{i,t-1} + \mu_i + \tau_t + \varepsilon_{i,t}
\]

Where:
- \(i\): REIT (`permno`)
- \(t\): month (`date`)
- \(\mu_i\): REIT fixed effects
- \(\tau_t\): time fixed effects (year-month)

Use robust (clustered-by-REIT) standard errors.

## Hypotheses

### H1: Leverage Sensitivity
- **Null (H0):** \(\beta_1 = 0\)
- **Alternative (H1):** \(\beta_1 < 0\)
- **Interpretation:** Higher debt ratios reduce next-period REIT returns.

### H2: Market Risk Pricing
- **Null (H0):** \(\beta_2 = 0\)
- **Alternative (H1):** \(\beta_2 \neq 0\)
- **Interpretation:** Systematic risk exposure (`beta`) is priced in REIT returns.

### H3: Profitability Premium
- **Null (H0):** \(\beta_3 = 0\)
- **Alternative (H1):** \(\beta_3 > 0\)
- **Interpretation:** More profitable REITs earn higher subsequent returns.

### H4: Value Effect
- **Null (H0):** \(\beta_4 = 0\)
- **Alternative (H1):** \(\beta_4 > 0\)
- **Interpretation:** Higher book-to-market REITs earn higher returns (value premium).

## Dynamic (Lagged) Hypotheses

### H5: Delayed Leverage Effect
Estimate distributed lags for debt ratio:

\[
usdret_{i,t} = \alpha + \sum_{k=0}^{12} \theta_k\, debt\_at_{i,t-k} + \mu_i + \tau_t + \varepsilon_{i,t}
\]

- **Null (H0):** \(\theta_1=\theta_2=\dots=\theta_{12}=0\)
- **Alternative (H1):** At least one \(\theta_k \neq 0\)
- **Joint test:** Wald/F-test on lag block.

### H6: Lag Persistence Window
- **Null (H0):** Cumulative medium-run effect is zero, \(\sum_{k=3}^{12}\theta_k = 0\)
- **Alternative (H1):** \(\sum_{k=3}^{12}\theta_k \neq 0\)
- **Interpretation:** Financial channel effects persist beyond immediate month impact.

## Sector Heterogeneity Hypotheses

Let `Sensitive_i` = 1 for sectors classified as sensitive (from your segmentation analysis), 0 otherwise.

### H7: Stronger Leverage Penalty in Sensitive Sectors

\[
usdret_{i,t} = \alpha + \beta_1 debt\_at_{i,t-1} + \beta_2 (debt\_at_{i,t-1}\times Sensitive_i) + \mu_i + \tau_t + \varepsilon_{i,t}
\]

- **Null (H0):** \(\beta_2 = 0\)
- **Alternative (H1):** \(\beta_2 < 0\)
- **Interpretation:** Debt hurts sensitive sectors more than resilient sectors.

### H8: Crisis Amplification
Define `Crisis_t` for stress windows (e.g., 2007–2009, 2020, 2022–2023).

\[
usdret_{i,t} = \alpha + \beta_1 debt\_at_{i,t-1} + \beta_2 Crisis_t + \beta_3 (debt\_at_{i,t-1}\times Crisis_t) + \mu_i + \tau_t + \varepsilon_{i,t}
\]

- **Null (H0):** \(\beta_3 = 0\)
- **Alternative (H1):** \(\beta_3 < 0\)
- **Interpretation:** Leverage penalties are larger during crisis periods.

## Recommended Estimation Sequence
1. Baseline FE model (H1–H4)
2. Add distributed lags and joint lag tests (H5–H6)
3. Add sector interactions (H7)
4. Add crisis interactions (H8)
5. Robustness: winsorize extremes, alternate lag lengths (6/12/18), subperiod tests

## Variable Mapping (Current Dataset)
- Outcome: `usdret`
- Firm ID: `permno`
- Time: `date`, `ym`
- Core regressors: `debt_at`, `beta`, `roe`, `btm`
- Controls for extensions: `market_equity`, `assets`, `cash_at`, `ocf_at`

## Reporting Template (Per Hypothesis)
For each hypothesis, report:
- Coefficient estimate and sign
- Cluster-robust standard error
- p-value and 95% confidence interval
- Economic magnitude (effect size)
- Accept/reject decision on H0
