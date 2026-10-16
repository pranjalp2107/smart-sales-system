
import pandas as pd

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]


# 1. Calculate KPIs
def kpi_summary(df):

    total_revenue = df["revenue"].sum()
    total_orders = df["order_id"].nunique()
    units_sold = df["quantity"].sum()
    unique_customers = df["customer_id"].nunique()

    order_totals = df.groupby("order_id")["revenue"].sum()

    if len(order_totals) > 0:
        avg_order_value = order_totals.mean()
    else:
        avg_order_value = 0

    result = {
        "total_revenue": float(total_revenue),
        "total_orders": int(total_orders),
        "units_sold": int(units_sold),
        "avg_order_value": float(avg_order_value),
        "unique_customers": int(unique_customers)
    }

    return result


# 2. Calculate monthly revenue
def monthly_revenue(df):

    result = df.groupby("month_start").agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique")
    )

    result = result.reset_index()

    return result


# 3. Prepare monthly revenue for forecasting
def monthly_series(df):

    series = df.groupby("month_start")["revenue"].sum()
    series = series.sort_index()
    series = series.asfreq("MS", fill_value=0)

    return series


# 4. Find top products
def top_products(df, n=10):

    result = df.groupby("product").agg(
        revenue=("revenue", "sum"),
        units=("quantity", "sum")
    )

    result = result.sort_values("revenue", ascending=False)
    result = result.head(n)
    result = result.reset_index()

    return result


# 5. Calculate revenue by category, region, or product
def revenue_by(df, column):

    result = df.groupby(column)["revenue"].sum()
    result = result.sort_values(ascending=False)
    result = result.reset_index()

    total = result["revenue"].sum()

    if total != 0:
        result["share_pct"] = (
            result["revenue"] / total * 100
        ).round(1)
    else:
        result["share_pct"] = 0

    return result


# 6. Compare revenue with the previous month
def growth_vs_previous(df):

    monthly = monthly_revenue(df)
    monthly = monthly.sort_values("month_start")

    if len(monthly) < 2:
        return None

    last_month = monthly.iloc[-1]
    previous_month = monthly.iloc[-2]

    last_revenue = last_month["revenue"]
    previous_revenue = previous_month["revenue"]

    if previous_revenue != 0:
        growth = (
            (last_revenue - previous_revenue)
            / previous_revenue * 100
        )
    else:
        growth = 0

    result = {
        "month": last_month["month_start"],
        "revenue": float(last_revenue),
        "previous_revenue": float(previous_revenue),
        "growth_pct": float(growth)
    }

    return result


# 7. Create weekday and month revenue table
def weekday_month_matrix(df):

    result = df.pivot_table(
        index="weekday_name",
        columns="month",
        values="revenue",
        aggfunc="sum",
        fill_value=0
    )

    result = result.reindex(
        index=WEEKDAYS,
        columns=range(1, 13),
        fill_value=0
    )

    return result


# 8. Create customer RFM table
def rfm_table(df):

    snapshot = df["order_date"].max() + pd.Timedelta(days=1)

    result = df.groupby("customer_id").agg(
        last_order_date=("order_date", "max"),
        frequency=("order_id", "nunique"),
        monetary=("revenue", "sum")
    )

    result = result.reset_index()

    result["recency"] = (
        snapshot - result["last_order_date"]
    ).dt.days

    result = result.drop(columns=["last_order_date"])

    result["r_score"] = pd.qcut(
        result["recency"].rank(method="first"),
        4,
        labels=[4, 3, 2, 1]
    ).astype(int)

    result["f_score"] = pd.qcut(
        result["frequency"].rank(method="first"),
        4,
        labels=[1, 2, 3, 4]
    ).astype(int)

    result["m_score"] = pd.qcut(
        result["monetary"].rank(method="first"),
        4,
        labels=[1, 2, 3, 4]
    ).astype(int)

    result["rfm_score"] = (
        result["r_score"]
        + result["f_score"]
        + result["m_score"]
    )

    result["segment"] = pd.cut(
        result["rfm_score"],
        bins=[0, 5, 8, 10, 12],
        labels=["At risk", "Regular", "Loyal", "Champion"]
    ).astype(str)

    return result


# 9. Detect unusual weekly revenue
def detect_anomalies(df, window=8, threshold=2.5):

    weekly = df.set_index("order_date")["revenue"]
    weekly = weekly.resample("W").sum()

    previous_weeks = weekly.shift(1)

    average = previous_weeks.rolling(window).mean()
    standard_deviation = previous_weeks.rolling(window).std()

    z_score = (weekly - average) / standard_deviation

    result = pd.DataFrame({
        "revenue": weekly,
        "z_score": z_score
    })

    result["is_anomaly"] = result["z_score"].abs() > threshold

    return result.dropna()




from src.data_loader import load_data

df = load_data()

# Calculate revenue
df["revenue"] = df["quantity"] * df["unit_price"]

# Prepare dates
df["order_date"] = pd.to_datetime(df["order_date"])
df["month_start"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
df["month"] = df["order_date"].dt.month
df["weekday_name"] = df["order_date"].dt.day_name()

# Show analysis results
print("\n--- SALES KPIs ---")
print(kpi_summary(df))

print("\n--- MONTHLY REVENUE ---")
print(monthly_revenue(df).to_string(index=False))

print("\n--- TOP 10 PRODUCTS ---")
print(top_products(df).to_string(index=False))

print("\n--- REVENUE BY CATEGORY ---")
print(revenue_by(df, "category").to_string(index=False))
