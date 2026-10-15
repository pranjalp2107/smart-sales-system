
import sqlite3
from pathlib import Path

import pandas as pd


def save_to_database(df, db_path=None):
    """Save cleaned sales data into a SQLite database."""

    if db_path is None:
        project_root = Path(__file__).resolve().parent.parent
        db_path = project_root / "data" / "sales.db"

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # SQLite cannot directly store pandas datetime objects.
    data = df.copy()

    for column in data.columns:
        if pd.api.types.is_datetime64_any_dtype(data[column]):
            data[column] = data[column].astype(str)

    with sqlite3.connect(db_path) as connection:
        data.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False,
        )

    print(f"Saved {len(data)} rows to database: {db_path}")


def load_from_database(db_path=None):
    """Read cleaned sales data from the SQLite database."""

    if db_path is None:
        project_root = Path(__file__).resolve().parent.parent
        db_path = project_root / "data" / "sales.db"

    db_path = Path(db_path)

    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    with sqlite3.connect(db_path) as connection:
        df = pd.read_sql_query("SELECT * FROM sales", connection)

    return df


if __name__ == "__main__":
    from data_loader import load_data
    from cleaning import clean_sales

    raw_df = load_data()
    clean_df = clean_sales(raw_df)

    save_to_database(clean_df)

    saved_df = load_from_database()
    print("\nRows read back from database:", len(saved_df))
    print(saved_df.head())