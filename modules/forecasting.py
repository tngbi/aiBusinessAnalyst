
from prophet import Prophet

def forecast_revenue(df):

    if "Date" not in df.columns or "Revenue" not in df.columns:
        return None

    data = df[["Date","Revenue"]].copy()

    data.columns = ["ds","y"]

    model = Prophet()

    model.fit(data)

    future = model.make_future_dataframe(periods=30)

    forecast = model.predict(future)

    return forecast
