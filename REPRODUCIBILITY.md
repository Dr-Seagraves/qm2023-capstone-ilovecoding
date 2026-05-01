# Reproducibility Checklist & Guide

**Project:** REIT Leverage & Return Analysis  
**Objective:** Verify that all results can be independently reproduced from raw data  
**Last Verified:** May 1, 2026

---

## Pre-Flight Checklist (Before Running Analysis)

### Environment Setup
- [ ] **Python 3.8+ installed**: `python --version` (should show 3.8+)
- [ ] **Virtual environment created**: `python -m venv venv` and activated
- [ ] **Dependencies installed**: `pip install -r requirements.txt` (includes numpy, pandas, statsmodels, matplotlib)
- [ ] **Git repo cloned**: `cd qm2023-capstone-ilovecoding`

### Data Availability
- [ ] **Raw REIT data present**: Check `data/raw/REIT_sample_2000_2024_All_Variables.csv` (should be ~50MB)
- [ ] **Processed data generated**: Run `python code/create_analysis_panel.py` 
  - Expected output: `data/final/REIT_analysis_panel.csv` (2.1MB, 34,121 rows)
- [ ] **Verify data integrity**: 
  ```bash
  python -c "import pandas as pd; df = pd.read_csv('data/final/REIT_analysis_panel.csv'); print(f'Rows: {len(df)}'); print(f'No NaN in returns: {df[\"return_pct\"].isna().sum() == 0}')"
  ```
  Expected: "Rows: 34121" and "No NaN in returns: True" ✓

### Directory Structure
- [ ] **Project directories exist**: 
  ```bash
  ls -d code/ data/raw data/processed data/final results/tables results/figures results/reports
  ```
  Should show all directories without errors

---

## Running the Analysis Pipeline

### Step 1: Generate Regression Models & Tables (5 mins)

```bash
cd /workspaces/qm2023-capstone-ilovecoding
python code/M3_econometric_models.py
```

**Expected Outputs:**
```
✓ Created: results/tables/M3_regression_table.csv
✓ Created: results/tables/M3_diagnostics_summary.csv
✓ Created: results/tables/M3_robustness_checks.csv
✓ Created: results/figures/M3_diagnostics.png
```

**Check file sizes (should be non-zero):**
```bash
ls -lh results/tables/M3_* results/figures/M3_*
```

### Step 2: Format Regression Tables (30 secs)

```bash
python code/format_regression_tables.py
```

**Expected Output:**
```
✓ CSV Table saved: M3_REGRESSION_TABLE_FORMATTED.csv
✓ Formatted table has 8 rows (Leverage_lag1, Leverage_lag2, Leverage_lag3, Beta, then summary stats)
```

### Step 3: Verify All Final Outputs Exist

```bash
# Check regression results
cat results/tables/M3_REGRESSION_TABLE_FORMATTED.csv | head -5

# Check figure was generated
file results/figures/M3_diagnostics.png | grep PNG
# Should output: "PNG image data"

# Check memo exists
wc -l results/reports/Final_Investment_Memo.md
# Should output: ~711 lines
```

---

## Regression Results Validation

### Expected Coefficient Values

| Variable | Expected Coefficient | Acceptable Range | Your Result | Match? |
|---|---|---|---|---|
| **Leverage_lag1** | 0.0071 | [0.0065, 0.0077] | _______ | ☐ |
| **Leverage_lag2** | 0.0070 | [0.0064, 0.0076] | _______ | ☐ |
| **Leverage_lag3** | −0.0115 | [−0.0121, −0.0109] | _______ | ☐ |
| **Beta** | 0.0061 | [0.0057, 0.0065] | _______ | ☐ |

### Expected p-Values

| Variable | Expected p-value | Your p-value | Match? |
|---|---|---|---|
| Leverage_lag1 | ~0.468 | _______ | ☐ |
| Leverage_lag2 | ~0.077 | _______ | ☐ |
| Leverage_lag3 | ~0.200 | _______ | ☐ |
| Beta | <0.001 | _______ | ☐ |

### Expected Model Diagnostics

| Statistic | Expected | Your Result | Match? |
|---|---|---|---|
| N observations | 33,573 | _______ | ☐ |
| Unique entities | 273 | _______ | ☐ |
| Time periods | 299 | _______ | ☐ |
| F-statistic | 8.23 | _______ | ☐ |
| R² (overall) | 0.0169 | _______ | ☐ |

---

## Data Integrity Validation

### Check 1: Sample Size

```bash
python << 'EOF'
import pandas as pd
df = pd.read_csv('data/final/REIT_analysis_panel.csv')
print(f"Total observations: {len(df)}")
print(f"Unique REITs: {df['ric_code'].nunique()}")
print(f"Time periods: {df['period_date'].nunique()}")
assert len(df) == 34121, "Sample size mismatch!"
assert df['ric_code'].nunique() == 273, "Entity count mismatch!"
print("✓ Sample size verified")
EOF
```

**Expected output:**
```
Total observations: 34121
Unique REITs: 273
Time periods: 299
✓ Sample size verified
```

### Check 2: No Missing Values in Key Variables

```bash
python << 'EOF'
import pandas as pd
df = pd.read_csv('data/final/REIT_analysis_panel.csv')
print("Missing values in key variables:")
print(f"  return_pct: {df['return_pct'].isna().sum()}")
print(f"  leverage: {df['leverage'].isna().sum()}")
print(f"  leverage_lag2: {df['leverage_lag2'].isna().sum()}")
print(f"  beta: {df['beta'].isna().sum()}")
assert df['return_pct'].isna().sum() == 0, "Return has NaNs!"
assert df['leverage'].isna().sum() == 0, "Leverage has NaNs!"
print("✓ Data completeness verified")
EOF
```

**Expected output:**
```
Missing values in key variables:
  return_pct: 0
  leverage: 0
  leverage_lag2: 0
  beta: 0
✓ Data completeness verified
```

### Check 3: Variable Distributions are Reasonable

```bash
python << 'EOF'
import pandas as pd
df = pd.read_csv('data/final/REIT_analysis_panel.csv')
print("Variable Ranges:")
print(f"  return_pct: [{df['return_pct'].min():.1f}, {df['return_pct'].max():.1f}]")
print(f"  leverage: [{df['leverage'].min():.1f}, {df['leverage'].max():.1f}]")
print(f"  beta: [{df['beta'].min():.2f}, {df['beta'].max():.2f}]")
assert -100 < df['return_pct'].min() < 0, "Return min out of range!"
assert 0 < df['return_pct'].max() < 200, "Return max out of range!"
assert 0 < df['leverage'].min() < 100, "Leverage min out of range!"
print("✓ Variable ranges verified")
EOF
```

**Expected output:**
```
Variable Ranges:
  return_pct: [-62.5, 85.3]
  leverage: [5.0, 85.0]
  beta: [0.21, 3.21]
✓ Variable ranges verified
```

---

## Multi-Run Stability Test (Optional, ~10 mins)

To ensure robustness, run analysis 3 times and check coefficients are identical:

```bash
# Run 1
python code/M3_econometric_models.py
cp results/tables/M3_REGRESSION_TABLE_FORMATTED.csv /tmp/run1.csv

# Run 2
python code/M3_econometric_models.py
cp results/tables/M3_REGRESSION_TABLE_FORMATTED.csv /tmp/run2.csv

# Run 3
python code/M3_econometric_models.py
cp results/tables/M3_REGRESSION_TABLE_FORMATTED.csv /tmp/run3.csv

# Compare
diff /tmp/run1.csv /tmp/run2.csv
diff /tmp/run2.csv /tmp/run3.csv

# Expected: No output (files identical)
```

**If files differ:** There is a source of randomness in the analysis (bad – reproducibility failed)  
**If files identical:** Excellent reproducibility ✓

---

## Comparison to Published Results

### Final Investment Memo Checks

- [ ] **Memo file exists and is readable**: `results/reports/Final_Investment_Memo.md`
- [ ] **Memo references correct coefficients**: Search memo for "61 basis points" for beta
- [ ] **Memo references correct sample size**: Search memo for "34,121" observations
- [ ] **Memo length ~18 pages**: Should have ~711 lines (11 lines/page average)

```bash
grep "61 basis" results/reports/Final_Investment_Memo.md && echo "✓ Memo references correct beta coefficient"
grep "34,121" results/reports/Final_Investment_Memo.md && echo "✓ Memo references correct sample size"
wc -l results/reports/Final_Investment_Memo.md | grep -E "7[0-1][0-9]" && echo "✓ Memo is approximately 18 pages"
```

### Executive Summary Checks

- [ ] **Executive Summary exists**: `results/reports/EXECUTIVE_SUMMARY_ONE_PAGE.md`
- [ ] **Summary contains key findings**: Look for "beta", "leverage", "beta premium"
- [ ] **Summary contains sector recommendations**: Look for "Industrial", "Residential", "Office"

---

## Troubleshooting Guide

### Issue: "ModuleNotFoundError: No module named 'statsmodels'"
**Solution:**
```bash
pip install statsmodels
# Then verify:
python -c "import statsmodels; print('OK')"
```

### Issue: "FileNotFoundError: data/final/REIT_analysis_panel.csv"
**Solution:** Run preprocessing step
```bash
python code/create_analysis_panel.py
# Check output:
ls -la data/final/REIT_analysis_panel.csv
```

### Issue: Regression coefficients don't match expected values ±0.0005
**Checks:**
1. Verify you're using same sample (34,121 obs, 273 entities)
2. Verify no recent changes to `M3_econometric_models.py`
3. Check random seed/random state not set differently
4. Re-run: `python code/M3_econometric_models.py`

### Issue: Figures not generated (M3_diagnostics.png missing)
**Solution:**
```bash
# Check matplotlib installed:
python -c "import matplotlib; print(matplotlib.get_backend())"

# Regenerate:
python code/M3_econometric_models.py
```

---

## Post-Reproduction Verification Checklist

After running full pipeline, verify:

- [ ] **All regression coefficients within ±0.0005 of expected values** (5 significant digits)
- [ ] **All p-values accurate to 3 decimal places** (matches expected)
- [ ] **Sample size exactly 33,573 observations** (Model A) and 33,487 (Model B)
- [ ] **All figures generated and non-empty** (check filesizes >100KB)
- [ ] **Investment memo loads and renders** without errors
- [ ] **Executive summary contains sector recommendations** (Industrial, Residential, etc.)

### Final Sign-Off

If all checks pass, you have successfully reproduced the ILOVECODING capstone:

```
✅ REPRODUCIBILITY VERIFIED
   Sample: 34,121 REIT-months (273 entities, 2000–2024)
   Models: Two-Way FE + DiD specifications
   Key Finding: Beta = 61 bps/month (highly significant); Leverage = 0 (not significant)
   Status: Ready for investor/committee review
   Date: [Your run date]
```

---

## Questions?

- **Methodology questions:** See `METHODOLOGY_BRIEF.md`
- **Result interpretation:** See `results/RESULTS_SUMMARY.md`
- **Investment application:** See `results/reports/Final_Investment_Memo.md`
- **Code questions:** See docstrings in `code/M3_econometric_models.py`

---

**Last Updated:** May 1, 2026  
**Status:** ✅ FINAL VERIFICATION PROTOCOL
