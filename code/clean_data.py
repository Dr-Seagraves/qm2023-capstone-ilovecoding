"""
Data Cleaning Script for REIT Dataset
Removes rows with missing values to ensure complete dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from code.config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, FINAL_DATA_DIR
except ImportError:
    # Fallback paths if config_paths doesn't define these
    RAW_DATA_DIR = project_root / "data" / "raw"
    PROCESSED_DATA_DIR = project_root / "data" / "processed"
    FINAL_DATA_DIR = project_root / "data" / "final"

def load_data(filename):
    """Load the raw data file"""
    filepath = RAW_DATA_DIR / filename
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Original data shape: {df.shape}")
    return df

def analyze_missing_values(df):
    """Analyze and report missing values in the dataset"""
    print("\n" + "="*60)
    print("MISSING VALUES ANALYSIS")
    print("="*60)
    
    # Count missing values per column
    missing_counts = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Missing Count': missing_counts.values,
        'Missing %': missing_pct.values
    })
    
    # Filter to show only columns with missing values
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    
    if len(missing_df) > 0:
        print(f"\nColumns with missing values:")
        print(missing_df.to_string(index=False))
        print(f"\nTotal rows with any missing values: {df.isnull().any(axis=1).sum()}")
    else:
        print("\nNo missing values found in the dataset!")
    
    return missing_df

def clean_data(df):
    """Clean the data by removing rows with missing values"""
    print("\n" + "="*60)
    print("CLEANING DATA")
    print("="*60)
    
    # Count rows before cleaning
    rows_before = len(df)
    
    # Remove rows with any missing values
    df_clean = df.dropna()
    
    rows_after = len(df_clean)
    rows_removed = rows_before - rows_after
    
    print(f"\nRows before cleaning: {rows_before}")
    print(f"Rows after cleaning: {rows_after}")
    print(f"Rows removed: {rows_removed} ({(rows_removed/rows_before)*100:.2f}%)")
    
    return df_clean

def save_cleaned_data(df, filename):
    """Save the cleaned data to the processed directory"""
    output_path = PROCESSED_DATA_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")
    return output_path

def verify_no_missing_values(df):
    """Verify that the cleaned data has no missing values"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    total_missing = df.isnull().sum().sum()
    
    if total_missing == 0:
        print("\n✓ SUCCESS: No missing values in cleaned dataset!")
        return True
    else:
        print(f"\n✗ WARNING: Still {total_missing} missing values found!")
        return False

def main():
    """Main data cleaning pipeline"""
    print("="*60)
    print("REIT DATA CLEANING PIPELINE")
    print("="*60)
    
    # Input and output filenames
    input_filename = "REIT_sample_2000_2024_All_Variables.csv"
    output_filename = "REIT_sample_2000_2024_All_Variables_cleaned.csv"
    
    # Load data
    df = load_data(input_filename)
    
    # Analyze missing values
    missing_analysis = analyze_missing_values(df)
    
    # Clean data
    df_clean = clean_data(df)
    
    # Verify no missing values
    verify_no_missing_values(df_clean)
    
    # Save cleaned data
    output_path = save_cleaned_data(df_clean, output_filename)
    
    print("\n" + "="*60)
    print("CLEANING COMPLETE")
    print("="*60)
    print(f"\nCleaned dataset shape: {df_clean.shape}")
    print(f"Output location: {output_path}")
    
    return df_clean

if __name__ == "__main__":
    df_cleaned = main()
