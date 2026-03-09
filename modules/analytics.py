
import numpy as np
from utils.logger import logger
from utils.helpers import safe_divide


def compute_kpis(df):
    """Compute a comprehensive set of business KPIs."""
    kpis = {}

    # Revenue metrics
    if "Revenue" in df.columns:
        kpis["Total Revenue"] = float(df["Revenue"].sum())
        kpis["Avg Revenue"] = float(df["Revenue"].mean())
        kpis["Max Revenue"] = float(df["Revenue"].max())

    # Profit metrics
    if "Profit" in df.columns:
        kpis["Total Profit"] = float(df["Profit"].sum())
        kpis["Avg Profit"] = float(df["Profit"].mean())

    # Profit margin
    if "Total Revenue" in kpis and "Total Profit" in kpis:
        kpis["Profit Margin %"] = round(
            safe_divide(kpis["Total Profit"], kpis["Total Revenue"]) * 100, 2
        )

    # Cost metrics
    if "Cost" in df.columns:
        kpis["Total Cost"] = float(df["Cost"].sum())

    # Customer metrics
    if "Customer_ID" in df.columns:
        kpis["Customers"] = int(df["Customer_ID"].nunique())
        if "Revenue" in df.columns:
            kpis["Revenue per Customer"] = round(
                safe_divide(kpis["Total Revenue"], kpis["Customers"]), 2
            )

    # Transaction volume
    kpis["Transactions"] = len(df)

    # Time-range
    if "Date" in df.columns and len(df) > 0:
        kpis["Date Range"] = f"{df['Date'].min().date()} → {df['Date'].max().date()}"

    # Monthly trend direction
    if "Date" in df.columns and "Revenue" in df.columns and len(df) > 1:
        monthly = df.set_index("Date")["Revenue"].resample("M").sum()
        if len(monthly) >= 2:
            recent = monthly.iloc[-1]
            prior = monthly.iloc[-2]
            change = safe_divide(recent - prior, prior) * 100
            kpis["MoM Revenue Change %"] = round(change, 2)

    logger.info(f"Computed {len(kpis)} KPIs")
    return kpis
