"""
QM 2023 Capstone Project: M1 - REIT Data Fetch & Clean
Team: [ILOVECODING]
Members: [Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez]

This script fetches/loads REIT (Real Estate Investment Trust) sample data
from data/raw/, cleans it, and saves the cleaned version to data/processed/.

Data Source: REIT_sample_2000_2024_All_Variables.csv
Sample includes REITs from 2000-2024 with financial metrics and returns

Pipeline steps:
  1. Load raw REIT data
  2. Clean missing values (drop/impute with justification)
  3. Handle outliers (winsorize/cap)
  4. Remove duplicates
  5. Apply REIT-specific filters (asset size, data quality)
  6. Save cleaned data to data/processed/

Author: [Ashley]
Date: [2/19/2026]
Last Modified: [2/19/2026]
"""

# ============================================================================
# Section 1: Imports and Config
# ============================================================================

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

# Import centralized path configuration
from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

# ============================================================================
# Section 2: Configuration & Constants
# ============================================================================

# Input/Output file names
RAW_FILENAME = "REIT_sample_2000_2024_All_Variables.csv"  # Raw REIT data
PROCESSED_FILENAME = "REIT_sample_clean.csv"  # Output file for data/processed/

# Data cleaning parameters
MISSING_VALUE_THRESHOLD = 0.5  # Drop columns with >50% missing values
OUTLIER_METHOD = "iqr"  # "iqr" or "zscore"
OUTLIER_THRESHOLD = 1.5  # IQR multiplier or z-score threshold
WINSORIZE_LIMITS = (0.05, 0.05)  # 5% on each tail

# REIT-specific filters
MIN_ASSETS = 100  # Minimum assets in millions (to filter very small REITs)
START_YEAR = 2000  # Analysis period starts
END_YEAR = 2024  # Analysis period ends

# ============================================================================
# Section 3: Load Raw Data
# ============================================================================

def load_raw_data(filename=RAW_FILENAME):
    """
    Load raw CSV data from data/raw/ directory.
    
    Args:
        filename (str): Name of the raw CSV file
        
    Returns:
        pd.DataFrame: Raw dataframe
        
    Raises:
        FileNotFoundError: If raw data file doesn't exist
    """
    raw_path = RAW_DATA_DIR / filename
    
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw data not found at: {raw_path}")
    
    print(f"Loading raw data from: {raw_path}")
    df = pd.read_csv(raw_path)
    
    print(f"✓ Loaded {len(df)} rows × {len(df.columns)} columns")
    print(f"  Columns: {list(df.columns)}")
    
    return df


# ============================================================================
# Section 4: Clean Missing Values
# ============================================================================

def clean_missing_values(df, threshold=MISSING_VALUE_THRESHOLD):
    """
    Handle missing values by dropping columns exceeding threshold
    and imputing remaining missing values.
    
    Justification for strategy:
      - Columns with >50% missing are likely unreliable → DROP
      - Numeric columns: impute with median (robust to outliers)
      - Categorical columns: impute with mode (most frequent)
      - Small amounts of missing are common in real data
    
    Args:
        df (pd.DataFrame): Input dataframe
        threshold (float): Proportion threshold for dropping columns (0-1)
        
    Returns:
        pd.DataFrame: Dataframe with missing values handled
        dict: Summary of actions taken
    """
    summary = {"rows_before": len(df), "cols_before": len(df.columns)}
    
    # Step 1: Calculate missing value percentages
    missing_pct = df.isnull().sum() / len(df)
    print(f"\nMissing Values Summary:")
    print(f"  Columns with >5% missing: {missing_pct[missing_pct > 0.05].to_dict()}")
    
    # Step 2: Drop columns with excessive missing values
    cols_to_drop = missing_pct[missing_pct > threshold].index
    if len(cols_to_drop) > 0:
        print(f"  Dropping {len(cols_to_drop)} columns exceeding {threshold*100}% threshold")
        print(f"    Columns dropped: {list(cols_to_drop)}")
        df = df.drop(columns=cols_to_drop)
    
    # Step 3: Impute remaining missing values
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype in ['float64', 'int64']:
                # Numeric: impute with median
                impute_val = df[col].median()
                impute_method = "median"
            else:
                # Categorical: impute with mode
                mode_result = df[col].mode()
                impute_val = mode_result[0] if len(mode_result) > 0 else "Unknown"
                impute_method = "mode"
            
            missing_count = df[col].isnull().sum()
            df[col] = df[col].fillna(impute_val)
            print(f"  Imputed {missing_count} values in '{col}' with {impute_method}: {impute_val}")
    
    summary["rows_after"] = len(df)
    summary["cols_after"] = len(df.columns)
    summary["cols_dropped"] = len(cols_to_drop)
    
    return df, summary


# ============================================================================
# Section 5: Handle Outliers
# ============================================================================

def identify_outliers_iqr(series, k=OUTLIER_THRESHOLD):
    """
    Identify outliers using Interquartile Range (IQR) method.
    Outliers = values outside Q1 - k*IQR and Q3 + k*IQR
    
    Args:
        series (pd.Series): Numeric series
        k (float): IQR multiplier (1.5 is standard)
        
    Returns:
        pd.Series: Boolean series indicating outliers
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - k * IQR
    upper_bound = Q3 + k * IQR
    return (series < lower_bound) | (series > upper_bound)


def identify_outliers_zscore(series, threshold=OUTLIER_THRESHOLD):
    """
    Identify outliers using Z-score method.
    Outliers = |z-score| > threshold (typically 3)
    
    Args:
        series (pd.Series): Numeric series
        threshold (float): Z-score threshold (3 = 99.7% of data)
        
    Returns:
        pd.Series: Boolean series indicating outliers
    """
    z_scores = np.abs(stats.zscore(series.dropna()))
    return np.abs(stats.zscore(series)) > threshold


def handle_outliers(df, method=OUTLIER_METHOD, numeric_only=True):
    """
    Handle outliers in numeric columns using specified method.
    Default: cap outliers using Winsorization (preserve data while reducing extremes)
    
    Justification for Winsorization:
      - Preserves data points (important for statistical power)
      - Reduces extreme values' influence without removal
      - Better than deletion for small datasets
      - More robust than mean/median imputation
    
    Args:
        df (pd.DataFrame): Input dataframe
        method (str): "iqr" or "zscore"
        numeric_only (bool): Only process numeric columns
        
    Returns:
        pd.DataFrame: Dataframe with outliers handled
        dict: Summary of outliers found
    """
    summary = {"outliers_found": 0, "columns_processed": 0}
    
    print(f"\nHandling Outliers ({method.upper()} method):")
    
    if numeric_only:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
    else:
        numeric_cols = df.columns
    
    for col in numeric_cols:
        # Identify outliers
        if method == "iqr":
            outlier_mask = identify_outliers_iqr(df[col], k=OUTLIER_THRESHOLD)
        elif method == "zscore":
            outlier_mask = identify_outliers_zscore(df[col], threshold=OUTLIER_THRESHOLD)
        else:
            raise ValueError(f"Unknown outlier method: {method}")
        
        outlier_count = outlier_mask.sum()
        if outlier_count > 0:
            summary["outliers_found"] += outlier_count
            summary["columns_processed"] += 1
            
            # Cap outliers using Winsorization
            limits = WINSORIZE_LIMITS
            df[col] = stats.mstats.winsorize(df[col], limits=limits)
            
            print(f"  '{col}': {outlier_count} outliers → winsorized")
    
    return df, summary


# ============================================================================
# Section 6: Remove Duplicates
# ============================================================================

def remove_duplicates(df):
    """
    Remove duplicate rows (completely identical rows).
    
    Justification:
      - Duplicate records represent data entry errors or redundant observations
      - Removing ensures each unit is counted once
      - Keeps first occurrence (can be changed with keep='last')
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Deduplicated dataframe
        dict: Summary of duplicates removed
    """
    summary = {
        "rows_before": len(df),
        "duplicates_found": df.duplicated().sum(),
        "rows_after": 0
    }
    
    if summary["duplicates_found"] > 0:
        print(f"\nRemoving Duplicates:")
        print(f"  Found {summary['duplicates_found']} duplicate rows")
        df = df.drop_duplicates(keep='first')
        print(f"  ✓ Duplicates removed")
    
    summary["rows_after"] = len(df)
    
    return df, summary


# ============================================================================
# Section 7: Apply Filters
# ============================================================================

def apply_filters(df):
    """
    Apply REIT-specific filters for data quality and minimum size requirements.
    
    Filters applied:
      1. Time period: Only include observations from START_YEAR to END_YEAR
      2. Asset size: Only REITs with assets >= MIN_ASSETS million
      3. Data quality: Only keep observations with valid returns and prices
      4. REIT type: Filter for actual REIT types (rtype=2.0 or equivalent)
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Filtered dataframe
        dict: Summary of filters applied
    """
    summary = {
        "rows_before": len(df),
        "rows_after": 0,
        "filters_applied": []
    }
    
    print(f"\nApplying REIT-Specific Filters:")
    
    # FILTER 1: Date/Year range
    if 'date' in df.columns:
        df['year'] = pd.to_datetime(df['date']).dt.year
        df = df[(df['year'] >= START_YEAR) & (df['year'] <= END_YEAR)]
        summary["filters_applied"].append(f"year_filter_{START_YEAR}_{END_YEAR}")
        print(f"  Filter 1: Year range {START_YEAR}-{END_YEAR}")
    
    # FILTER 2: Minimum assets threshold
    if 'assets' in df.columns:
        valid_assets = df['assets'].notna().sum()
        df = df[df['assets'] >= MIN_ASSETS]
        assets_removed = valid_assets - df['assets'].notna().sum()
        summary["filters_applied"].append(f"min_assets_{MIN_ASSETS}M")
        print(f"  Filter 2: Assets >= ${MIN_ASSETS}M (removed {assets_removed} rows)")
    
    # FILTER 3: Valid returns (non-null and non-zero)
    if 'usdret' in df.columns:
        returns_before = df['usdret'].notna().sum()
        df = df[df['usdret'].notna()]
        summary["filters_applied"].append("valid_returns")
        returns_removed = returns_before - df['usdret'].notna().sum()
        print(f"  Filter 3: Valid returns data (removed {returns_removed} rows)")
    
    # FILTER 4: Valid prices
    if 'usdprc' in df.columns:
        price_before = df['usdprc'].notna().sum()
        df = df[(df['usdprc'].notna()) & (df['usdprc'] > 0)]
        summary["filters_applied"].append("valid_prices")
        price_removed = price_before - df['usdprc'].notna().sum()
        print(f"  Filter 4: Valid prices (removed {price_removed} rows)")
    
    # FILTER 5: REIT type (if rtype column exists)
    if 'rtype' in df.columns:
        # Keep rtype = 2.0 (common REIT type code)
        rtype_before = len(df)
        df = df[df['rtype'] == 2.0]
        summary["filters_applied"].append("rtype_2.0")
        rtype_removed = rtype_before - len(df)
        print(f"  Filter 5: REIT type = 2.0 (removed {rtype_removed} rows)")
    
    summary["rows_after"] = len(df)
    rows_removed = summary["rows_before"] - summary["rows_after"]
    
    if rows_removed > 0:
        pct_removed = (rows_removed / summary["rows_before"] * 100)
        print(f"  ✓ Total: {rows_removed} rows removed ({pct_removed:.1f}%)")
    
    return df, summary


# ============================================================================
# Section 8: Save Cleaned Data
# ============================================================================

def save_cleaned_data(df, filename=PROCESSED_FILENAME):
    """
    Save cleaned dataframe to data/processed/ directory.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe
        filename (str): Output filename
        
    Returns:
        Path: Path to saved file
    """
    output_path = PROCESSED_DATA_DIR / filename
    
    print(f"\nSaving cleaned data:")
    print(f"  Output file: {output_path}")
    
    df.to_csv(output_path, index=False)
    
    print(f"  ✓ Saved {len(df)} rows × {len(df.columns)} columns")
    
    # Verify save
    if output_path.exists():
        file_size = output_path.stat().st_size / 1024  # KB
        print(f"  ✓ File verified ({file_size:.1f} KB)")
    
    return output_path


# ============================================================================
# Section 9: Main Pipeline
# ============================================================================

def main():
    """
    Execute the complete REIT data cleaning pipeline.
    """
    print("=" * 70)
    print("REIT Data Fetch & Clean Pipeline")
    print("=" * 70)
    
    # Load raw data
    df = load_raw_data()
    
    # Clean missing values
    df, missing_summary = clean_missing_values(df)
    
    # Handle outliers
    df, outlier_summary = handle_outliers(df)
    
    # Remove duplicates
    df, duplicate_summary = remove_duplicates(df)
    
    # Apply filters
    df, filter_summary = apply_filters(df)
    
    # Save cleaned data
    output_path = save_cleaned_data(df)
    
    # Print final summary
    print("\n" + "=" * 70)
    print("Pipeline Complete - REIT Sample Summary")
    print("=" * 70)
    print(f"Initial rows: {missing_summary['rows_before']:,}")
    print(f"Final rows: {len(df):,} ({(len(df)/missing_summary['rows_before']*100):.1f}% retained)")
    print(f"Final columns: {len(df.columns)}")
    print(f"\nData Quality Metrics:")
    print(f"  - Columns dropped: {missing_summary['cols_before'] - missing_summary['cols_after']}")
    print(f"  - Outliers handled: {outlier_summary['outliers_found']}")
    print(f"  - Duplicates removed: {duplicate_summary['duplicates_found']}")
    print(f"  - Rows removed by REIT filters: {filter_summary['rows_before'] - filter_summary['rows_after']}")
    print(f"\nOutputting to: {output_path}")
    print("=" * 70)
    
    return df, output_path


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    df_clean, path = main()
