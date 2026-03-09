
# Configuration settings for AI Business Analyst App

APP_NAME = "AI Business Analyst"
FORECAST_PERIOD_DAYS = 30

# Revenue thresholds for recommendations
REVENUE_LOW_THRESHOLD = 100_000
REVENUE_HIGH_THRESHOLD = 1_000_000

# Profit margin targets
PROFIT_MARGIN_HEALTHY = 20  # percent
PROFIT_MARGIN_WARNING = 10  # percent

# Supported upload formats
SUPPORTED_FILE_TYPES = ["xlsx", "xls", "csv"]

# Numeric columns that should NOT be filled with 0
NULLABLE_NUMERIC_COLS = ["Discount", "Tax"]

# Expected columns (used for validation warnings)
EXPECTED_COLUMNS = ["Date", "Revenue", "Cost", "Customer_ID"]

# Dashboard colour palette
CHART_COLOR_PRIMARY = "#1f77b4"
CHART_COLOR_SECONDARY = "#ff7f0e"
CHART_COLOR_POSITIVE = "#2ca02c"
CHART_COLOR_NEGATIVE = "#d62728"
