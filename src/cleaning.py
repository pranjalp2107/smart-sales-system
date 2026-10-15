
import pandas as pd


def clean_sales(raw_df):
    """Clean raw sales data and create useful analysis columns."""

    df = raw_df.copy()

    # 1. Remove duplicate records.
    df = df.drop_duplicates().copy()

    # 2. Standardize text columns.
    text_columns = ["product", "category", "region", "customer_id"]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()

    # Standardize product and category names.
    for column in ["product", "category"]:
        if column in df.columns:
            df[column] = df[column].str.title()

    if "region" in df.columns:
        df["region"] = df["region"].str.title()
        df["region"] = df["region"].fillna("Unknown")
        df.loc[df["region"] == "", "region"] = "Unknown"

    # 3. Convert numeric columns.
    for column in ["quantity", "unit_price"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # 4. Convert dates and remove invalid records.
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )

    df = df.dropna(
        subset=[
            "order_id",
            "order_date",
            "customer_id",
            "product",
            "category",
            "quantity",
            "unit_price",
        ]
    ).copy()

    # 5. Remove invalid quantities and prices.
    df = df[
        (df["quantity"] > 0) &
        (df["unit_price"] > 0)
    ].copy()

    # 6. Remove duplicate order IDs.
    df = df.drop_duplicates(subset=["order_id"]).copy()

    # 7. Calculate revenue.
    df["revenue"] = df["quantity"] * df["unit_price"]

    # 8. Add date information.
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["quarter"] = df["order_date"].dt.quarter
    df["weekday_name"] = df["order_date"].dt.day_name()
    df["month_start"] = (
        df["order_date"].dt.to_period("M").dt.to_timestamp()
    )

    # 9. Mark potential revenue outliers using the IQR method.
    q1 = df["revenue"].quantile(0.25)
    q3 = df["revenue"].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    df["is_outlier"] = (
        (df["revenue"] < lower_bound) |
        (df["revenue"] > upper_bound)
    )

    return df.reset_index(drop=True)


if __name__ == "__main__":
    from data_loader import load_data

    raw_df = load_data()
    clean_df = clean_sales(raw_df)

    print("Raw rows:", len(raw_df))
    print("Clean rows:", len(clean_df))
    print("\nCleaned data preview:")
    print(clean_df.head())
    print("\nFinal columns:")
    print(clean_df.columns.tolist())