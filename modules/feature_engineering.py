
import numpy as np
from utils.logger import logger


def create_features(df):
    """Derive additional business features from raw data."""

    # Profit
    if "Revenue" in df.columns and "Cost" in df.columns:
        df["Profit"] = df["Revenue"] - df["Cost"]
        df["Profit_Margin"] = np.where(
            df["Revenue"] > 0,
            (df["Profit"] / df["Revenue"]) * 100,
            0,
        )
        logger.info("Created Profit and Profit_Margin features")

    # Time-based features
    if "Date" in df.columns:
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
        df["Day_of_Week"] = df["Date"].dt.dayofweek
        df["Quarter"] = df["Date"].dt.quarter
        df["Is_Weekend"] = df["Day_of_Week"].isin([5, 6]).astype(int)
        logger.info("Created time-based features (Year, Month, Quarter, Day_of_Week, Is_Weekend)")

    # Revenue per customer (if groupable)
    if "Revenue" in df.columns and "Customer_ID" in df.columns:
        cust_rev = df.groupby("Customer_ID")["Revenue"].transform("sum")
        df["Customer_Lifetime_Value"] = cust_rev
        logger.info("Created Customer_Lifetime_Value feature")

    return df
