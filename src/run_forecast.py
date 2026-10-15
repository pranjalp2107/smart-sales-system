
import pandas as pd

from data_loader import load_data
from analysis import monthly_series
from forecasting import forecast_future

# Step 1: Load sales data
df = load_data()

# Step 2: Prepare the data
df["order_date"] = pd.to_datetime(df["order_date"])
df["revenue"] = df["quantity"] * df["unit_price"]

df["month_start"] = (
    df["order_date"].dt.to_period("M").dt.to_timestamp()
)

# Step 3: Calculate monthly revenue
monthly = monthly_series(df)

# Step 4: Predict revenue for the next 6 months
forecast, model = forecast_future(
    monthly,
    periods=6
)

# Step 5: Display results
print("\nSelected forecasting model:", model)

print("\n--- SIX-MONTH REVENUE FORECAST ---")
print(forecast.round(2).to_string())
