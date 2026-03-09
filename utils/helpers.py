
import pandas as pd


def safe_divide(a, b):
    """Return a/b, or 0 when b is zero."""
    if b == 0:
        return 0
    return a / b


def format_currency(value):
    """Format a number as a currency string."""
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:,.1f}K"
    return f"${value:,.2f}"


def format_percent(value):
    """Format a number as a percentage string."""
    return f"{value:+.1f}%"


def dataframe_summary(df):
    """Return a concise text summary of a DataFrame."""
    lines = [
        f"Rows: {len(df):,}",
        f"Columns: {len(df.columns)}",
        f"Numeric columns: {len(df.select_dtypes(include='number').columns)}",
        f"Missing values: {int(df.isna().sum().sum()):,}",
    ]
    return " | ".join(lines)
