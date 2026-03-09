
import pandas as pd
import numpy as np
from utils.logger import logger


def clean_data(df):
    """Clean the dataframe: deduplicate, handle missing values, and parse dates."""
    original_len = len(df)

    # Drop exact duplicate rows
    df = df.drop_duplicates()
    dropped = original_len - len(df)
    if dropped:
        logger.info(f"Dropped {dropped} duplicate rows")

    # Parse date column
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        null_dates = df["Date"].isna().sum()
        if null_dates:
            logger.warning(f"{null_dates} rows have unparseable dates — dropping them")
            df = df.dropna(subset=["Date"])

    # Fill numeric columns with median (more robust than 0)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        na_count = df[col].isna().sum()
        if na_count > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            logger.info(f"Filled {na_count} NaN in '{col}' with median ({median_val})")

    # Fill categorical columns with 'Unknown'
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in cat_cols:
        na_count = df[col].isna().sum()
        if na_count > 0:
            df[col] = df[col].fillna("Unknown")
            logger.info(f"Filled {na_count} NaN in '{col}' with 'Unknown'")

    # Remove rows where key financial columns are non-positive
    for col in ["Revenue", "Cost"]:
        if col in df.columns:
            bad = (df[col] < 0).sum()
            if bad:
                logger.warning(f"Found {bad} negative values in '{col}' — setting to 0")
                df[col] = df[col].clip(lower=0)

    logger.info(f"Cleaning complete: {len(df)} rows remaining")
    return df
