
import pandas as pd

from src.cleaning import clean_sales


def test_negative_and_zero_quantities_are_removed():
    raw_df = pd.DataFrame({
        "order_id": ["A001", "A002", "A003"],
        "order_date": ["2025-01-01", "2025-01-02", "2025-01-03"],
        "customer_id": ["C001", "C002", "C003"],
        "product": ["Laptop", "Phone", "Tablet"],
        "category": ["Electronics", "Electronics", "Electronics"],
        "region": ["North", "South", "East"],
        "quantity": [2, -1, 0],
        "unit_price": [500, 400, 300],
    })

    clean_df = clean_sales(raw_df)

    assert len(clean_df) == 1
    assert (clean_df["quantity"] > 0).all()


def test_revenue_and_text_cleaning():
    raw_df = pd.DataFrame({
        "order_id": ["A001"],
        "order_date": ["2025-01-01"],
        "customer_id": ["C001"],
        "product": [" laptop "],
        "category": ["electronics"],
        "region": ["north"],
        "quantity": [2],
        "unit_price": [500],
    })

    clean_df = clean_sales(raw_df)

    assert clean_df.iloc[0]["revenue"] == 1000
    assert clean_df.iloc[0]["product"] == "Laptop"
    assert clean_df.iloc[0]["region"] == "North"
