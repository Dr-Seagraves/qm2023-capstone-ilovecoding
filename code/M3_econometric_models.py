"""
QM 2023 Capstone Project: M3 - Econometric Models
Team: ILOVECODING

This script estimates the milestone 3 regression models using the analysis panel
created in M1 and the exploratory findings from M2.

Outputs:
  - results/tables/M3_regression_table.csv
  - results/tables/M3_diagnostics_summary.csv
  - results/tables/M3_robustness_checks.csv
  - results/figures/M3_diagnostics.png
"""

from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

from config_paths import FIGURES_DIR, TABLES_DIR
from utils import load_analysis_panel

warnings.filterwarnings("ignore")

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (14, 8)

ANALYSIS_PANEL = "REIT_analysis_panel.csv"
OUTPUT_REGRESSION_TABLE = "M3_regression_table.csv"
OUTPUT_DIAGNOSTICS = "M3_diagnostics_summary.csv"
OUTPUT_ROBUSTNESS = "M3_robustness_checks.csv"
OUTPUT_FIGURE = "M3_diagnostics.png"

MODEL_CONTROLS = [
    "log_market_cap_m",
    "debt_to_assets",
    "return_on_equity",
    "book_to_market",
]


def prepare_data() -> pd.DataFrame:
    """Load and prepare the analysis panel for regression analysis."""
    df = load_analysis_panel(ANALYSIS_PANEL).copy()

    needed_cols = [
        "entity_id",
        "year_month",
        "year",
        "return_pct",
        "market_cap_m",
        "debt_to_assets",
        "return_on_equity",
        "book_to_market",
        "beta",
    ]

    missing_cols = [col for col in needed_cols if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing required columns for M3 models: {missing_cols}")

    df["log_market_cap_m"] = np.log(df["market_cap_m"].clip(lower=1e-6))
    df["post_2012"] = (df["year"] >= 2012).astype(int)

    beta_by_entity = df.groupby("entity_id")["beta"].mean()
    high_beta_threshold = beta_by_entity.quantile(0.75)
    df["treated_high_beta"] = df["entity_id"].map(beta_by_entity >= high_beta_threshold).astype(int)
    df["high_beta_post_2012"] = df["treated_high_beta"] * df["post_2012"]

    df = df.dropna(subset=["return_pct"] + MODEL_CONTROLS + ["beta", "treated_high_beta", "high_beta_post_2012"])
    df = df.sort_values(["entity_id", "date_obs"] if "date_obs" in df.columns else ["entity_id", "year_month"])
    if "date_obs" in df.columns:
        df["date_obs"] = pd.to_datetime(df["date_obs"])

    print(f"Prepared analysis sample: {len(df):,} rows × {len(df.columns)} columns")
    print(f"High-beta threshold (75th percentile of entity-average beta): {high_beta_threshold:.4f}")
    return df


def fit_clustered_ols(formula: str, data: pd.DataFrame):
    """Fit an OLS model with entity-clustered standard errors."""
    model = smf.ols(formula=formula, data=data).fit(
        cov_type="cluster",
        cov_kwds={"groups": data["entity_id"]},
    )
    return model


def pooled_diagnostics_data(data: pd.DataFrame) -> pd.DataFrame:
    """Create a pooled sample for diagnostics that exclude fixed effects."""
    return data[["return_pct", "beta"] + MODEL_CONTROLS].dropna().copy()


def fit_model_a(data: pd.DataFrame):
    """Baseline two-way fixed effects model."""
    formula = (
        "return_pct ~ beta + log_market_cap_m + debt_to_assets + return_on_equity "
        "+ book_to_market + C(entity_id) + C(year_month)"
    )
    return fit_clustered_ols(formula, data)


def fit_model_b(data: pd.DataFrame):
    """DiD-style model using high-beta REITs and the post-2012 period."""
    formula = (
        "return_pct ~ high_beta_post_2012 + log_market_cap_m + debt_to_assets "
        "+ return_on_equity + book_to_market + C(entity_id) + C(year_month)"
    )
    return fit_clustered_ols(formula, data)


def significance_stars(pvalue: float) -> str:
    """Return significance stars for table formatting."""
    if pvalue < 0.01:
        return "***"
    if pvalue < 0.05:
        return "**"
    if pvalue < 0.1:
        return "*"
    return ""


def format_coefficient(result, term: str) -> str:
    """Format a coefficient and standard error in one cell."""
    if term not in result.params.index:
        return ""
    coef = result.params[term]
    se = result.bse[term]
    pvalue = result.pvalues[term]
    return f"{coef:.4f}{significance_stars(pvalue)}\n({se:.4f})"


def build_regression_table(model_a, model_b) -> pd.DataFrame:
    """Build a publication-style side-by-side regression table."""
    rows = [
        ("beta", "Beta"),
        ("high_beta_post_2012", "High beta x Post-2012"),
        ("log_market_cap_m", "Log(Market Cap)"),
        ("debt_to_assets", "Debt-to-Assets"),
        ("return_on_equity", "Return on Equity"),
        ("book_to_market", "Book-to-Market"),
    ]

    table_rows = []
    for term, label in rows:
        table_rows.append(
            {
                "Variable": label,
                "Model A: FE": format_coefficient(model_a, term),
                "Model B: DiD-style": format_coefficient(model_b, term),
            }
        )

    summary_rows = [
        {
            "Variable": "Entity FE",
            "Model A: FE": "Yes",
            "Model B: DiD-style": "Yes",
        },
        {
            "Variable": "Time FE",
            "Model A: FE": "Yes",
            "Model B: DiD-style": "Yes",
        },
        {
            "Variable": "Clustered SE (entity)",
            "Model A: FE": "Yes",
            "Model B: DiD-style": "Yes",
        },
        {
            "Variable": "Observations",
            "Model A: FE": f"{int(model_a.nobs):,}",
            "Model B: DiD-style": f"{int(model_b.nobs):,}",
        },
        {
            "Variable": "Adjusted R-squared",
            "Model A: FE": f"{model_a.rsquared_adj:.4f}",
            "Model B: DiD-style": f"{model_b.rsquared_adj:.4f}",
        },
    ]

    regression_table = pd.DataFrame(table_rows + summary_rows)
    return regression_table


def calculate_vif(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate VIF for the core economic predictors."""
    x = sm.add_constant(data[["beta"] + MODEL_CONTROLS])
    vif_rows = []
    for index, column in enumerate(x.columns):
        if column == "const":
            continue
        vif_rows.append(
            {
                "variable": column,
                "vif": variance_inflation_factor(x.values, index),
            }
        )
    return pd.DataFrame(vif_rows)


def residual_diagnostics(model, output_path: Path) -> dict:
    """Create residual plots and return Shapiro-Wilk and skewness metrics."""
    fitted = np.asarray(model.fittedvalues)
    resid = np.asarray(model.resid)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    axes[0, 0].scatter(fitted, resid, alpha=0.25, color="#315a8c", edgecolors="none")
    axes[0, 0].axhline(0, color="black", linewidth=1)
    axes[0, 0].set_title("Residuals vs. Fitted")
    axes[0, 0].set_xlabel("Fitted values")
    axes[0, 0].set_ylabel("Residuals")

    axes[0, 1].hist(resid, bins=50, color="#d67f3d", alpha=0.7, edgecolor="white")
    axes[0, 1].set_title("Residual Distribution")
    axes[0, 1].set_xlabel("Residual")
    axes[0, 1].set_ylabel("Count")

    stats.probplot(resid, dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title("Q-Q Plot of Residuals")

    axes[1, 1].axis("off")
    rng = np.random.default_rng(42)
    shapiro_sample = resid if len(resid) <= 5000 else rng.choice(resid, 5000, replace=False)
    shapiro_stat, shapiro_p = stats.shapiro(shapiro_sample)
    skewness = stats.skew(resid)
    kurtosis = stats.kurtosis(resid)
    note = (
        "Residual diagnostics\n\n"
        f"Shapiro-Wilk p-value: {shapiro_p:.4g}\n"
        f"Skewness: {skewness:.4f}\n"
        f"Excess kurtosis: {kurtosis:.4f}\n\n"
        "Heavy tails are expected in REIT returns, so the focus is on robust inference."
    )
    axes[1, 1].text(0.05, 0.5, note, fontsize=11, family="monospace", va="center")

    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return {
        "shapiro_stat": shapiro_stat,
        "shapiro_p": shapiro_p,
        "skewness": skewness,
        "kurtosis": kurtosis,
    }


def breusch_pagan_test(model) -> dict:
    """Run a Breusch-Pagan test on the pooled diagnostic model."""
    residuals = model.resid
    exog = model.model.exog
    lm_stat, lm_pvalue, f_stat, f_pvalue = het_breuschpagan(residuals, exog)
    return {
        "bp_lm_stat": lm_stat,
        "bp_lm_pvalue": lm_pvalue,
        "bp_f_stat": f_stat,
        "bp_f_pvalue": f_pvalue,
    }


def fit_pooled_diagnostic_model(data: pd.DataFrame):
    """Fit a pooled OLS model used for heteroskedasticity diagnostics."""
    formula = "return_pct ~ beta + log_market_cap_m + debt_to_assets + return_on_equity + book_to_market"
    return smf.ols(formula=formula, data=data).fit()


def build_diagnostics_summary(data: pd.DataFrame, model_a) -> pd.DataFrame:
    """Build a diagnostics summary table."""
    pooled = pooled_diagnostics_data(data)
    pooled_model = fit_pooled_diagnostic_model(pooled)
    bp = breusch_pagan_test(pooled_model)
    vif = calculate_vif(pooled)

    diagnostics_rows = [
        {
            "diagnostic": "Breusch-Pagan test",
            "value": f"LM p = {bp['bp_lm_pvalue']:.4g}; F p = {bp['bp_f_pvalue']:.4g}",
            "interpretation": "Rejecting homoskedasticity supports clustered standard errors.",
        },
        {
            "diagnostic": "Residual normality",
            "value": "See M3_diagnostics.png",
            "interpretation": "Q-Q plot and histogram show heavy tails; inference should stay robust.",
        },
    ]

    vif_records = []
    for _, row in vif.iterrows():
        vif_records.append(
            {
                "diagnostic": f"VIF: {row['variable']}",
                "value": f"{row['vif']:.3f}",
                "interpretation": (
                    "Acceptable multicollinearity" if row["vif"] < 5 else "Potential multicollinearity concern"
                ),
            }
        )

    summary = pd.DataFrame(diagnostics_rows + vif_records)
    summary["model_a_adj_r2"] = model_a.rsquared_adj
    return summary


def fit_robustness_models(data: pd.DataFrame) -> pd.DataFrame:
    """Run robustness checks for milestone 3."""
    robustness_rows = []

    def summarize(label: str, result, coefficient_name: str = "beta"):
        robustness_rows.append(
            {
                "check": label,
                "sample": f"{int(result.nobs):,}",
                "target_term": coefficient_name,
                "coef": result.params.get(coefficient_name, np.nan),
                "se": result.bse.get(coefficient_name, np.nan),
                "pvalue": result.pvalues.get(coefficient_name, np.nan),
                "adj_r2": result.rsquared_adj,
            }
        )

    summarize("Baseline FE model", fit_model_a(data))

    lagged = data.sort_values(["entity_id", "date_obs"]).copy()
    for col in ["beta"] + MODEL_CONTROLS:
        lagged[f"{col}_lag1"] = lagged.groupby("entity_id")[col].shift(1)
        lagged[f"{col}_lag3"] = lagged.groupby("entity_id")[col].shift(3)

    lag1_formula = (
        "return_pct ~ beta_lag1 + log_market_cap_m_lag1 + debt_to_assets_lag1 + "
        "return_on_equity_lag1 + book_to_market_lag1 + C(entity_id) + C(year_month)"
    )
    lag3_formula = lag1_formula.replace("lag1", "lag3")

    lag1_data = lagged.dropna(subset=["return_pct", "beta_lag1", "log_market_cap_m_lag1", "debt_to_assets_lag1", "return_on_equity_lag1", "book_to_market_lag1"])
    lag3_data = lagged.dropna(subset=["return_pct", "beta_lag3", "log_market_cap_m_lag3", "debt_to_assets_lag3", "return_on_equity_lag3", "book_to_market_lag3"])

    summarize("Alternative lag structure (1-month)", fit_clustered_ols(lag1_formula, lag1_data), "beta_lag1")
    summarize("Alternative lag structure (3-month)", fit_clustered_ols(lag3_formula, lag3_data), "beta_lag3")

    covid_data = data[(data["year"] < 2020) | (data["year"] > 2021)].copy()
    summarize("Exclude COVID years (2020-2021)", fit_model_a(covid_data))

    median_market_cap = data["market_cap_m"].median()
    small = data[data["market_cap_m"] <= median_market_cap]
    large = data[data["market_cap_m"] > median_market_cap]
    summarize("Small REIT subsample", fit_model_a(small))
    summarize("Large REIT subsample", fit_model_a(large))

    return pd.DataFrame(robustness_rows)


def save_outputs(regression_table: pd.DataFrame, diagnostics: pd.DataFrame, robustness: pd.DataFrame):
    """Persist all M3 outputs to the results folders."""
    regression_path = TABLES_DIR / OUTPUT_REGRESSION_TABLE
    diagnostics_path = TABLES_DIR / OUTPUT_DIAGNOSTICS
    robustness_path = TABLES_DIR / OUTPUT_ROBUSTNESS

    regression_table.to_csv(regression_path, index=False)
    diagnostics.to_csv(diagnostics_path, index=False)
    robustness.to_csv(robustness_path, index=False)

    print(f"✓ Saved regression table: {regression_path}")
    print(f"✓ Saved diagnostics summary: {diagnostics_path}")
    print(f"✓ Saved robustness checks: {robustness_path}")


def main() -> dict:
    """Run the M3 econometric analysis pipeline."""
    print("\n" + "=" * 80)
    print("M3 ECONOMETRIC MODELS")
    print("=" * 80)

    data = prepare_data()

    print("\nFitting Model A: two-way fixed effects baseline")
    model_a = fit_model_a(data)

    print("Fitting Model B: DiD-style high-beta / post-2012 specification")
    model_b = fit_model_b(data)

    print("Building comparison table")
    regression_table = build_regression_table(model_a, model_b)

    print("Running diagnostics")
    diagnostics_path = FIGURES_DIR / OUTPUT_FIGURE
    residual_stats = residual_diagnostics(model_a, diagnostics_path)
    diagnostics = build_diagnostics_summary(data, model_a)
    diagnostics["residual_shapiro_p"] = residual_stats["shapiro_p"]
    diagnostics["residual_skewness"] = residual_stats["skewness"]
    diagnostics["residual_kurtosis"] = residual_stats["kurtosis"]

    print("Running robustness checks")
    robustness = fit_robustness_models(data)

    save_outputs(regression_table, diagnostics, robustness)

    print("\nModel A summary")
    print(model_a.summary().tables[1])
    print("\nModel B summary")
    print(model_b.summary().tables[1])

    print("\nM3 analysis complete")
    return {
        "model_a": model_a,
        "model_b": model_b,
        "regression_table": regression_table,
        "diagnostics": diagnostics,
        "robustness": robustness,
    }


if __name__ == "__main__":
    results = main()
