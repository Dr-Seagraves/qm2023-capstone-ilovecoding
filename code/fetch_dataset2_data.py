"""
QM 2023 Capstone Project: M1 - Dataset2 Data Fetch & Clean
Team: [Your Team Name]
Members: [List names]

This script fetches/loads the secondary dataset, cleans it, and saves
the cleaned version to data/processed/.

This is an alternative example showing:
  - Different data source (could be from API, database, etc.)
  - Custom filters specific to dataset2
  - Alternative outlier handling approach
  - Validation checks

Pipeline steps:
  1. Load raw data
  2. Clean missing values
  3. Handle outliers
  4. Remove duplicates
  5. Apply size/volume filters
  6. Data validation checks
  7. Save cleaned data

Author: [Your Names]
Date: [Date Created]
Last Modified: [Date]
"""

# ============================================================================
# Section 1: Imports and Config
# ============================================================================

import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Import centralized path configuration
from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Section 2: Configuration & Constants
# ============================================================================

RAW_FILENAME = "dataset2_raw.csv"
PROCESSED_FILENAME = "dataset2_clean.csv"

# Data quality thresholds
MIN_OBSERVATIONS = 10  # Minimum samples per group
MISSING_THRESHOLD = 0.7  # Drop columns with >70% missing
DATE_FORMAT = "%Y-%m-%d"  # Expected date format

# ============================================================================
# Section 3: Load Raw Data
# ============================================================================

def load_raw_data(filename=RAW_FILENAME):
    """Load raw CSV data with type inference."""
    raw_path = RAW_DATA_DIR / filename
    
    if not raw_path.exists():
        logger.error(f"Raw data not found at: {raw_path}")
        raise FileNotFoundError(f"Raw data not found at: {raw_path}")
    
    logger.info(f"Loading raw data from: {raw_path}")
    
    df = pd.read_csv(raw_path)
    
    logger.info(f"Loaded {len(df):,} rows × {len(df.columns)} columns")
    logger.info(f"Data types:\n{df.dtypes}")
    
    return df


# ============================================================================
# Section 4: Clean Missing Values
# ============================================================================

def clean_missing_values(df, threshold=MISSING_THRESHOLD):
    """
    Handle missing values with logging of strategy.
    """
    logger.info("=" * 50)
    logger.info("CLEANING MISSING VALUES")
    logger.info("=" * 50)
    
    rows_before = len(df)
    cols_before = len(df.columns)
    
    # Identify columns with excessive missing values
    missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    
    if len(missing_pct[missing_pct > 0]) > 0:
        logger.info(f"\nMissing value percentages (>0%):")
        for col, pct in missing_pct[missing_pct > 0].items():
            logger.info(f"  {col}: {pct:.1f}%")
    
    # Drop columns exceeding threshold
    cols_to_drop = missing_pct[missing_pct > threshold * 100].index.tolist()
    if cols_to_drop:
        logger.info(f"\nDropping {len(cols_to_drop)} columns exceeding {threshold*100}% threshold:")
        for col in cols_to_drop:
            logger.info(f"  - {col}")
        df = df.drop(columns=cols_to_drop)
    
    # Impute remaining missing values
    logger.info("\nImputing remaining missing values:")
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                fill_value = df[col].median()
                df[col].fillna(fill_value, inplace=True)
                logger.info(f"  {col}: imputed with median ({fill_value:.2f})")
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                fill_value = df[col].mode()[0] if not df[col].mode().empty else df[col].max()
                df[col].fillna(fill_value, inplace=True)
                logger.info(f"  {col}: imputed with date mode")
            else:
                fill_value = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                df[col].fillna(fill_value, inplace=True)
                logger.info(f"  {col}: imputed with mode ({fill_value})")
    
    logger.info(f"\nResult: {len(df):,} rows × {len(df.columns)} columns")
    logger.info(f"  (removed {cols_before - len(df.columns)} columns)")
    
    return df


# ============================================================================
# Section 5: Handle Outliers (Alternative: Z-score method)
# ============================================================================

def handle_outliers_zscore(df, threshold=3.0):
    """
    Handle outliers using Z-score method.
    
    Justification for Z-score:
      - More suitable for normally distributed data
      - Removes extreme outliers (>3σ ≈ 0.3%)
      - Alternative to Winsorization when data is normally distributed
    """
    logger.info("=" * 50)
    logger.info("HANDLING OUTLIERS (Z-score method)")
    logger.info("=" * 50)
    
    outliers_count = 0
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        # Calculate z-scores
        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
        outlier_mask = z_scores > threshold
        col_outliers = outlier_mask.sum()
        
        if col_outliers > 0:
            # Remove rows with extreme outliers
            df = df[~outlier_mask]
            outliers_count += col_outliers
            logger.info(f"  {col}: removed {col_outliers} outliers (|z| > {threshold})")
    
    if outliers_count == 0:
        logger.info("  No extreme outliers detected")
    
    logger.info(f"Result: {len(df):,} rows remaining")
    
    return df


# ============================================================================
# Section 6: Remove Duplicates
# ============================================================================

def remove_duplicates(df):
    """Remove exact duplicate rows."""
    logger.info("=" * 50)
    logger.info("REMOVING DUPLICATES")
    logger.info("=" * 50)
    
    dup_count = df.duplicated().sum()
    
    if dup_count > 0:
        logger.info(f"  Found {dup_count} duplicate rows")
        df = df.drop_duplicates(keep='first')
        logger.info(f"  ✓ Duplicates removed")
    else:
        logger.info("  No duplicates found")
    
    logger.info(f"Result: {len(df):,} rows")
    
    return df


# ============================================================================
# Section 7: Apply Filters & Validation
# ============================================================================

def apply_filters(df):
    """
    Apply dataset2-specific filters and validation.
    
    Example: If this is time-series data, transaction data, or group data,
    add filters relevant to that domain.
    """
    logger.info("=" * 50)
    logger.info("APPLYING FILTERS & VALIDATION")
    logger.info("=" * 50)
    
    rows_before = len(df)
    
    # EXAMPLE: Filter by data quality
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        # Remove rows where all numeric values are zero
        all_zero_rows = (df[numeric_cols] == 0).all(axis=1)
        logger.info(f"  All-zero rows found: {all_zero_rows.sum()}")
        if all_zero_rows.sum() > 0:
            df = df[~all_zero_rows]
            logger.info(f"  Removed {all_zero_rows.sum()} all-zero rows")
    
    # EXAMPLE: Group size filter (if you have grouping columns)
    # Uncomment and adapt if dataset has groups/categories:
    # if 'group_id' in df.columns:
    #     group_counts = df['group_id'].value_counts()
    #     small_groups = group_counts[group_counts < MIN_OBSERVATIONS].index
    #     df = df[~df['group_id'].isin(small_groups)]
    #     logger.info(f"  Removed {len(small_groups)} groups with <{MIN_OBSERVATIONS} observations")
    
    rows_removed = rows_before - len(df)
    if rows_removed > 0:
        logger.info(f"  Total rows removed: {rows_removed} ({rows_removed/rows_before*100:.1f}%)")
    
    logger.info(f"Result: {len(df):,} rows")
    
    return df


# ============================================================================
# Section 8: Final Data Validation
# ============================================================================

def validate_cleaned_data(df):
    """Perform final validation checks on cleaned data."""
    logger.info("=" * 50)
    logger.info("DATA VALIDATION")
    logger.info("=" * 50)
    
    # Check 1: No remaining nulls in critical columns
    critical_cols = [col for col in df.columns if 'id' in col.lower()]
    if critical_cols:
        null_check = df[critical_cols].isnull().sum()
        if null_check.sum() == 0:
            logger.info(f"  ✓ No nulls in critical columns: {critical_cols}")
        else:
            logger.warning(f"  ⚠ Nulls found in: {null_check[null_check > 0].to_dict()}")
    
    # Check 2: Reasonable row count
    if len(df) > 0:
        logger.info(f"  ✓ Final dataset has {len(df):,} rows")
    else:
        logger.error("  ✗ Dataset is empty!")
        return False
    
    # Check 3: Data type summary
    logger.info(f"  ✓ Data types: {dict(df.dtypes.astype(str).value_counts())}")
    
    return True


# ============================================================================
# Section 9: Save Cleaned Data
# ============================================================================

def save_cleaned_data(df, filename=PROCESSED_FILENAME):
    """Save cleaned dataframe."""
    output_path = PROCESSED_DATA_DIR / filename
    
    logger.info("=" * 50)
    logger.info("SAVING CLEANED DATA")
    logger.info("=" * 50)
    
    df.to_csv(output_path, index=False)
    
    logger.info(f"  Output: {output_path}")
    logger.info(f"  Size: {len(df):,} rows × {len(df.columns)} columns")
    
    if output_path.exists():
        file_size = output_path.stat().st_size / 1024
        logger.info(f"  File size: {file_size:.1f} KB ✓")
    
    return output_path


# ============================================================================
# Section 10: Main Pipeline
# ============================================================================

def main():
    """Execute the complete data cleaning pipeline."""
    logger.info("\n" + "=" * 70)
    logger.info("DATASET2 DATA FETCH & CLEAN PIPELINE")
    logger.info("=" * 70 + "\n")
    
    try:
        # Step 1: Load
        df = load_raw_data()
        logger.info("\n")
        
        # Step 2: Clean missing values
        df = clean_missing_values(df)
        logger.info("\n")
        
        # Step 3: Handle outliers
        df = handle_outliers_zscore(df)
        logger.info("\n")
        
        # Step 4: Remove duplicates
        df = remove_duplicates(df)
        logger.info("\n")
        
        # Step 5: Apply filters
        df = apply_filters(df)
        logger.info("\n")
        
        # Step 6: Validate
        is_valid = validate_cleaned_data(df)
        if not is_valid:
            logger.error("Data validation failed!")
            return None, None
        logger.info("\n")
        
        # Step 7: Save
        output_path = save_cleaned_data(df)
        logger.info("\n")
        
        logger.info("=" * 70)
        logger.info("✓ PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 70 + "\n")
        
        return df, output_path
        
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        raise


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    df_clean, path = main()
