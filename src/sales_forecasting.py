import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

print("=" * 70)
print("SALES FORECASTING")
print("=" * 70)

# --------------------------------------------------
# 1. Load cleaned data
# --------------------------------------------------

df = pd.read_csv("outputs/cleaned_retail_sales.csv")

df["Date"] = pd.to_datetime(df["Date"])

# --------------------------------------------------
# 2. Create monthly revenue
# --------------------------------------------------

monthly_revenue = (
    df.groupby(df["Date"].dt.to_period("M"))["Revenue"]
      .sum()
      .reset_index()
)

monthly_revenue["Date"] = monthly_revenue["Date"].dt.to_timestamp()

monthly_revenue = monthly_revenue.set_index("Date")

monthly_revenue = monthly_revenue.asfreq("MS")

print("\nMonthly Revenue:")
print(monthly_revenue)

# --------------------------------------------------
# 3. Train-Test Split
# --------------------------------------------------

# Last 6 months are used for testing
train = monthly_revenue.iloc[:-6]
test = monthly_revenue.iloc[-6:]

print("\nTraining Period:")
print(train.index.min(), "to", train.index.max())

print("\nTesting Period:")
print(test.index.min(), "to", test.index.max())

# --------------------------------------------------
# 4. Seasonal Naive Forecast
# --------------------------------------------------

# Forecast each month using the revenue from
# the same month in the previous year.

forecast_values = []

for date in test.index:

    previous_year = date - pd.DateOffset(years=1)

    value = train.loc[previous_year, "Revenue"]

    forecast_values.append(value)

test_forecast = pd.Series(
    forecast_values,
    index=test.index
)

# --------------------------------------------------
# 5. Model Evaluation
# --------------------------------------------------

mae = mean_absolute_error(
    test["Revenue"],
    test_forecast
)

rmse = np.sqrt(
    mean_squared_error(
        test["Revenue"],
        test_forecast
    )
)

# MAPE
mape = (
    np.mean(
        np.abs(
            (test["Revenue"] - test_forecast)
            / test["Revenue"]
        )
    ) * 100
)

print("\n" + "=" * 70)
print("MODEL EVALUATION")
print("=" * 70)

print(f"MAE  : ₹{mae:,.2f}")
print(f"RMSE : ₹{rmse:,.2f}")
print(f"MAPE : {mape:.2f}%")

# --------------------------------------------------
# 6. Actual vs Predicted
# --------------------------------------------------

comparison = pd.DataFrame({
    "Actual_Revenue": test["Revenue"],
    "Forecast_Revenue": test_forecast
})

comparison["Absolute_Error"] = (
    comparison["Actual_Revenue"]
    - comparison["Forecast_Revenue"]
).abs()

comparison["Percentage_Error"] = (
    comparison["Absolute_Error"]
    / comparison["Actual_Revenue"]
) * 100

print("\n" + "=" * 70)
print("ACTUAL VS FORECAST")
print("=" * 70)

print(comparison)

# --------------------------------------------------
# 7. Final Forecast
# --------------------------------------------------

# Use the latest 12 months as the seasonal pattern
latest_year = monthly_revenue.iloc[-12:]

future_dates = pd.date_range(
    start=monthly_revenue.index[-1] + pd.DateOffset(months=1),
    periods=12,
    freq="MS"
)

future_values = latest_year["Revenue"].values

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Forecast_Revenue": future_values
})

print("\n" + "=" * 70)
print("12-MONTH REVENUE FORECAST")
print("=" * 70)

print(forecast_df)

# --------------------------------------------------
# 8. Save Forecast
# --------------------------------------------------

forecast_df.to_csv(
    "outputs/revenue_forecast.csv",
    index=False
)

# --------------------------------------------------
# 9. Create Forecast Chart
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue.index,
    monthly_revenue["Revenue"],
    label="Actual Revenue"
)

plt.plot(
    forecast_df["Date"],
    forecast_df["Forecast_Revenue"],
    label="Forecast Revenue"
)

plt.title("Monthly Revenue Forecast")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.legend()

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/charts/revenue_forecast.png",
    dpi=300
)

plt.close()

# --------------------------------------------------
# 10. Completion
# --------------------------------------------------

print("\n" + "=" * 70)
print("SALES FORECASTING COMPLETED!")
print("=" * 70)

print("\nSaved:")
print("outputs/revenue_forecast.csv")
print("outputs/charts/revenue_forecast.png")