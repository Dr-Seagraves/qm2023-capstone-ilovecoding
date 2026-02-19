"""
QM 2023 Capstone Project: M1 - Climate and Stocks Data Fetch & Clean
Team: [ILOVECODING]
Members: [Aniya Facen, Ashley Seale, Olivia Williamson, Yuri Rodriguez]

This script fetches/loads climate and stock market data, cleans it,
and saves the cleaned version to data/processed/.

Data Source: Climate impact metrics and corresponding stock performance
Combines environmental/climate risk factors with equity returns

This is an alternative pipeline showing:
  - Different data source structure
  - Custom filters for climate/ESG data
  - Z-score outlier handling (alternative to Winsorization)
  - Validation checks for paired observations

Pipeline steps:
  1. Load raw climate and stocks data
  2. Clean missing values (impute/drop)
  3. Handle outliers (z-score method)
  4. Remove duplicates
  5. Align dates between climate and stock datasets
  6. Apply quality & completeness filters
  7. Data validation checks
  8. Save cleaned data

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

# Input/Output file names
RAW_FILENAME = "climate_stocks_raw.csv"  # Raw climate and stocks data
PROCESSED_FILENAME = "climate_stocks_clean.csv"  # Output for data/processed/

# Data quality thresholds
MIN_OBSERVATIONS = 20  # Minimum company-date observations
MISSING_THRESHOLD = 0.6  # Drop columns with >60% missing
DATE_FORMAT = "%Y-%m-%d"  # Expected date format

# Climate and stocks specific filters
MIN_STOCK_PRICE = 1.0  # Filter out penny stocks (<$1)
MIN_CLIMATE_SCORE = 0  # Minimum ESG/climate score
START_DATE = "2000-01-01"  # Analysis period start
END_DATE = "2024-12-31"  # Analysis period end

# Key columns for validation
REQUIRED_COLUMNS = ['date', 'ticker', 'stock_price', 'climate_score', 'returns']


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
    Apply climate and stocks specific filters and validation.
    
    Filters:
      1. Date range: Keep only observations between START_DATE and END_DATE
      2. Stock price: Remove penny stocks (<$MIN_STOCK_PRICE)
      3. Climate score: Remove observations with missing climate scores
      4. Paired data: Keep only rows with both stock price and climate data
      5. Returns validity: Ensure returns are computable
      6. Company observations: Keep only companies with MIN_OBSERVATIONS periods
    """
    logger.info("=" * 50)
    logger.info("APPLYING CLIMATE & STOCKS FILTERS")
    logger.info("=" * 50)
    
    rows_before = len(df)
    
    # FILTER 1: Date range
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df[(df['date'] >= START_DATE) & (df['date'] <= END_DATE)]
        logger.info(f"  Filter 1: Date range {START_DATE} to {END_DATE}")
    
    # FILTER 2: Stock price threshold (remove penny stocks)
    if 'stock_price' in df.columns:
        price_before = len(df)
        df = df[df['stock_price'] >= MIN_STOCK_PRICE]
        price_removed = price_before - len(df)
        logger.info(f"  Filter 2: Stock price >= ${MIN_STOCK_PRICE} (removed {price_removed} rows)")
    
    # FILTER 3: Climate score validity
    if 'climate_score' in df.columns:
        climate_before = len(df)
        df = df[df['climate_score'].notna()]
        climate_removed = climate_before - len(df)
        logger.info(f"  Filter 3: Valid climate scores (removed {climate_removed} rows)")
    
    # FILTER 4: Paired data requirement
    # Only keep rows where we have both stock and climate data
    required_cols = [col for col in REQUIRED_COLUMNS if col in df.columns]
    paired_before = len(df)
    df = df[df[required_cols].notna().all(axis=1)]
    paired_removed = paired_before - len(df)
    logger.info(f"  Filter 4: Paired observations (removed {paired_removed} rows)")
    
    # FILTER 5: Returns validity
    if 'returns' in df.columns:
        returns_before = len(df)
        # Keep only valid numeric returns (not NaN or infinite)
        df = df[(df['returns'].notna()) & (np.isfinite(df['returns']))]
        returns_removed = returns_before - len(df)
        logger.info(f"  Filter 5: Valid returns (removed {returns_removed} rows)")
    
    # FILTER 6: Minimum company observations
    if 'ticker' in df.columns:
        company_counts = df['ticker'].value_counts()
        small_companies = company_counts[company_counts < MIN_OBSERVATIONS].index
        if len(small_companies) > 0:
            df = df[~df['ticker'].isin(small_companies)]
            logger.info(f"  Filter 6: Companies with >={MIN_OBSERVATIONS} obs (removed {len(small_companies)} companies)")
    
    rows_removed = rows_before - len(df)
    if rows_removed > 0:
        pct_removed = (rows_removed / rows_before * 100)
        logger.info(f"  ✓ Total: {rows_removed} rows removed ({pct_removed:.1f}%)")
    
    return df

    return df

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
    """Execute the complete climate and stocks data cleaning pipeline."""
    logger.info("\n" + "=" * 70)
    logger.info("CLIMATE & STOCKS DATA FETCH & CLEAN PIPELINE")
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
