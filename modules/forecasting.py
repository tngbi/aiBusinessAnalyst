
from prophet import Prophet
from config import FORECAST_PERIOD_DAYS
from utils.logger import logger


def forecast_revenue(df):
    """Forecast future revenue using Prophet."""
    if "Date" not in df.columns or "Revenue" not in df.columns:
        logger.warning("Cannot forecast — 'Date' or 'Revenue' column missing")
        return None

    data = df[["Date", "Revenue"]].copy()
    data.columns = ["ds", "y"]

    # Prophet needs at least 2 data points
    data = data.dropna()
    if len(data) < 2:
        logger.warning("Not enough data points for forecasting")
        return None

    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(data)

    future = model.make_future_dataframe(periods=FORECAST_PERIOD_DAYS)
    forecast = model.predict(future)

    logger.info(f"Forecast generated: {FORECAST_PERIOD_DAYS} days ahead, {len(forecast)} total rows")
    return forecast
