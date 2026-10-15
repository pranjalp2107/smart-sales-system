
# Convert numbers into simple English sentences
import analysis
import pandas as pd


def generate_insights(df):

    # Create an empty list to store sentences
    lines = []

    # 1. Get total revenue, orders, and customers
    kpis = analysis.kpi_summary(df)

    total_revenue = kpis["total_revenue"]
    total_orders = kpis["total_orders"]
    total_customers = kpis["unique_customers"]

    sentence = (
        f"Total revenue is ${total_revenue:,.0f} from "
        f"{total_orders:,} orders and "
        f"{total_customers:,} customers."
    )

    lines.append(sentence)

    # 2. Find the best-selling product by revenue
    products = analysis.top_products(df, 1)
    best_product = products.iloc[0]

    product_name = best_product["product"]
    product_revenue = best_product["revenue"]

    sentence = (
        f"{product_name} is the top product, earning "
        f"${product_revenue:,.0f}."
    )

    lines.append(sentence)

    # 3. Find the strongest region
    regions = analysis.revenue_by(df, "region")
    best_region = regions.iloc[0]

    region_name = best_region["region"]
    region_share = best_region["share_pct"]

    sentence = (
        f"{region_name} is the strongest region with "
        f"{region_share}% of all revenue."
    )

    lines.append(sentence)

    # 4. Find the leading product category
    categories = analysis.revenue_by(df, "category")
    best_category = categories.iloc[0]

    category_name = best_category["category"]
    category_share = best_category["share_pct"]

    sentence = (
        f"{category_name} is the leading category "
        f"({category_share}% share)."
    )

    lines.append(sentence)

    # 5. Find the month with the highest revenue
    monthly = analysis.monthly_revenue(df)

    highest_revenue = monthly["revenue"].max()

    peak = monthly[
        monthly["revenue"] == highest_revenue
    ].iloc[0]

    peak_month = peak["month_start"]
    peak_revenue = peak["revenue"]

    sentence = (
        f"The best month was {peak_month:%B %Y} "
        f"with ${peak_revenue:,.0f}."
    )

    lines.append(sentence)

    # 6. Compare revenue with the previous month
    growth = analysis.growth_vs_previous(df)

    if growth is not None:

        growth_percentage = growth["growth_pct"]
        month = growth["month"]

        if growth_percentage >= 0:
            direction = "grew"
        else:
            direction = "dropped"

        sentence = (
            f"In {month:%B %Y}, revenue {direction} "
            f"{abs(growth_percentage):.1f}% "
            f"compared with the previous month."
        )

        lines.append(sentence)

    # 7. Find unusual sales weeks
    anomalies = analysis.detect_anomalies(df)

    unusual_weeks = anomalies["is_anomaly"].sum()

    if unusual_weeks > 0:

        sentence = (
            f"{int(unusual_weeks)} unusual week(s) were detected "
            f"where sales were far from normal."
        )

        lines.append(sentence)

    # Return all insight sentences
    return lines



if __name__ == "__main__":
    from data_loader import load_data

    df = load_data()
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["revenue"] = df["quantity"] * df["unit_price"]

    df["month_start"] = (
        df["order_date"].dt.to_period("M").dt.to_timestamp()
    )

    print("\n--- SALES INSIGHTS ---")

    for sentence in generate_insights(df):
        print("-", sentence)
