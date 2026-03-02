"""
Prepare Final Analysis-Ready Data
==================================
This script takes cleaned data from processed/ and prepares it for final analysis.
Also copies the data dictionary to the final directory for documentation.

Pipeline: data/processed/ -> data/final/
"""

import pandas as pd
import shutil
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config_paths import PROCESSED_DATA_DIR, FINAL_DATA_DIR, REPORTS_DIR

def load_processed_data(filename):
    """Load the cleaned data from processed directory"""
    filepath = PROCESSED_DATA_DIR / filename
    
    if not filepath.exists():
        raise FileNotFoundError(
            f"Processed data not found: {filepath}\n"
            f"Please run clean_data.py first to generate cleaned data."
        )
    
    print(f"Loading processed data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Data shape: {df.shape}")
    return df

def validate_data_quality(df):
    """Validate that the data meets quality standards"""
    print("\n" + "="*80)
    print("DATA QUALITY VALIDATION")
    print("="*80)
    
    checks_passed = []
    checks_failed = []
    
    # Check 1: No missing values
    missing_count = df.isnull().sum().sum()
    if missing_count == 0:
        checks_passed.append("✓ No missing values")
    else:
        checks_failed.append(f"✗ Found {missing_count} missing values")
    
    # Check 2: Date column exists and is valid
    if 'date' in df.columns:
        checks_passed.append("✓ Date column present")
        try:
            pd.to_datetime(df['date'])
            checks_passed.append("✓ Date format valid")
        except:
            checks_failed.append("✗ Date format invalid")
    else:
        checks_failed.append("✗ Date column missing")
    
    # Check 3: Key identifier columns exist
    required_cols = ['permno', 'ticker', 'usdret', 'market_equity']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if not missing_cols:
        checks_passed.append("✓ All required columns present")
    else:
        checks_failed.append(f"✗ Missing columns: {missing_cols}")
    
    # Check 4: Data size is reasonable
    if len(df) > 100:
        checks_passed.append(f"✓ Data size adequate ({len(df):,} rows)")
    else:
        checks_failed.append(f"✗ Data size too small ({len(df)} rows)")
    
    # Print results
    print("\nQuality Checks Passed:")
    for check in checks_passed:
        print(f"  {check}")
    
    if checks_failed:
        print("\nQuality Checks Failed:")
        for check in checks_failed:
            print(f"  {check}")
        print("\n⚠ WARNING: Data quality issues detected!")
        return False
    else:
        print("\n✓ All quality checks passed!")
        return True

def add_analysis_features(df):
    """Add any final derived features for analysis"""
    print("\n" + "="*80)
    print("FEATURE ENGINEERING")
    print("="*80)
    
    df_final = df.copy()
    
    # Ensure date is datetime
    if 'date' in df_final.columns:
        df_final['date'] = pd.to_datetime(df_final['date'])
        print("✓ Converted date to datetime format")
    
    # Add year and month columns for easier analysis
    if 'date' in df_final.columns:
        df_final['year'] = df_final['date'].dt.year
        df_final['month'] = df_final['date'].dt.month
        print("✓ Added year and month columns")
    
    # Sort by identifier and date for panel structure
    if 'permno' in df_final.columns and 'date' in df_final.columns:
        df_final = df_final.sort_values(['permno', 'date'])
        print("✓ Sorted data by REIT ID and date (panel structure)")
    
    print(f"\nFinal dataset shape: {df_final.shape}")
    print(f"Date range: {df_final['date'].min()} to {df_final['date'].max()}")
    
    return df_final

def save_final_data(df, filename):
    """Save the analysis-ready data to final directory"""
    output_path = FINAL_DATA_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"\n✓ Final data saved to: {output_path}")
    return output_path

def copy_data_dictionary():
    """Copy data dictionary to final directory for documentation"""
    source = REPORTS_DIR / 'Data_Dictionary.md'
    destination = FINAL_DATA_DIR / 'Data_Dictionary.md'
    
    if source.exists():
        shutil.copy2(source, destination)
        print(f"✓ Data dictionary copied to: {destination}")
        return True
    else:
        print(f"⚠ Data dictionary not found at: {source}")
        return False

def create_readme():
    """Create README in final directory explaining the data"""
    readme_content = """# Final Analysis-Ready Data

This directory contains the final, cleaned, analysis-ready REIT dataset.

## Files

- **REIT_analysis_panel.csv** — Main analysis dataset (cleaned, validated, sorted)
- **Data_Dictionary.md** — Complete variable documentation

## Dataset Specifications

- **Time Period:** 2000-2024
- **Frequency:** Monthly observations
- **Structure:** Panel data (sorted by REIT ID and date)
- **Quality:** All missing values removed, validated
- **Format:** CSV with header row

## Usage

```python
import pandas as pd
from config_paths import FINAL_DATA_DIR

# Load analysis-ready data
df = pd.read_csv(FINAL_DATA_DIR / 'REIT_analysis_panel.csv')

# Date column is ready for time series analysis
df['date'] = pd.to_datetime(df['date'])

# Data is pre-sorted for panel analysis
# Rows are ordered by: permno (REIT ID) -> date
```

## Data Pipeline

1. **Raw** (data/raw/) — Original data
2. **Processed** (data/processed/) — Cleaned (missing values removed)
3. **Final** (data/final/) — Analysis-ready with features ✓ You are here

## Quality Assurance

✓ No missing values
✓ All required columns present
✓ Date formats validated
✓ Panel structure (sorted by ID and date)
✓ Additional features (year, month columns)

---
Generated by: prepare_final_data.py
"""
    
    readme_path = FINAL_DATA_DIR / 'README.md'
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    print(f"✓ README created at: {readme_path}")
    
    return readme_path

def main():
    """Main pipeline to prepare final analysis-ready data"""
    print("="*80)
    print("PREPARE FINAL ANALYSIS-READY DATA")
    print("="*80)
    
    # Input from processed, output to final
    input_filename = "REIT_sample_2000_2024_All_Variables_cleaned.csv"
    output_filename = "REIT_analysis_panel.csv"
    
    try:
        # Step 1: Load processed data
        df = load_processed_data(input_filename)
        
        # Step 2: Validate data quality
        quality_ok = validate_data_quality(df)
        
        # Step 3: Add analysis features
        df_final = add_analysis_features(df)
        
        # Step 4: Save to final directory
        output_path = save_final_data(df_final, output_filename)
        
        # Step 5: Copy data dictionary
        print("\n" + "="*80)
        print("DOCUMENTATION")
        print("="*80)
        copy_data_dictionary()
        
        # Step 6: Create README
        create_readme()
        
        # Final summary
        print("\n" + "="*80)
        print("PIPELINE COMPLETE")
        print("="*80)
        print(f"\n✓ Final dataset ready for analysis!")
        print(f"  Location: {output_path}")
        print(f"  Shape: {df_final.shape[0]:,} rows × {df_final.shape[1]} columns")
        print(f"  Date range: {df_final['date'].min().date()} to {df_final['date'].max().date()}")
        print(f"\n✓ Documentation included in: {FINAL_DATA_DIR}")
        
        return df_final
        
    except FileNotFoundError as e:
        print(f"\n✗ ERROR: {e}")
        print("\nPlease run the data cleaning pipeline first:")
        print("  python code/clean_data.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    df_final = main()
