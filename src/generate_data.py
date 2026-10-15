
from pathlib import Path

import numpy as np
import pandas as pd


def generate_sales_data(n_rows=1000, seed=42):
    """Generate sample sales data for our project."""

    rng = np.random.default_rng(seed)

    # Locate the main project folder.
    project_root = Path(__file__).resolve().parent.parent
    output_path = project_root / "data" / "raw" / "sales_raw.csv"

    # Create the output directory if it doesn't exist.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    products = ["Laptop", "Phone", "Tablet", "Headphones", "Keyboard"]
    prices = {
        "Laptop": 50000,
        "Phone": 25000,
        "Tablet": 18000,
        "Headphones": 2000,
        "Keyboard": 1000,
    }
    categories = {
        "Laptop": "Electronics",
        "Phone": "Electronics",
        "Tablet": "Electronics",
        "Headphones": "Accessories",
        "Keyboard": "Accessories",
    }

    chosen_products = rng.choice(products, size=n_rows)

    df = pd.DataFrame({
        "order_id": [f"ORD{i:05d}" for i in range(1, n_rows + 1)],
        "order_date": pd.to_datetime(
            rng.integers(
                pd.Timestamp("2023-01-01").value // 10**9,
                pd.Timestamp("2026-01-01").value // 10**9,
                size=n_rows,
            ),
            unit="s",
        ).strftime("%Y-%m-%d"),
        "customer_id": [
            f"CUST{i:04d}"
            for i in rng.integers(1, 301, size=n_rows)
        ],
        "product": chosen_products,
        "category": [categories[p] for p in chosen_products],
        "region": rng.choice(
            ["North", "South", "East", "West"], size=n_rows
        ),
        "quantity": rng.integers(1, 11, size=n_rows),
        "unit_price": [prices[p] for p in chosen_products],
    })

    # Add intentional data-quality issues for cleaning practice.
    if n_rows >= 10:
        df.loc[0, "product"] = "  laptop  "
        df.loc[1, "region"] = " north "
        df.loc[2, "region"] = np.nan
        df.loc[3, "customer_id"] = np.nan
        df.loc[4, "product"] = np.nan
        df.loc[5, "quantity"] = -2
        df.loc[6, "quantity"] = 0
        df.loc[9] = df.loc[8].copy()  # Duplicate row

    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} sales records.")
    print(f"File saved to: {output_path}")

    return df


if __name__ == "__main__":
    sales_df = generate_sales_data()
    print(sales_df.head())