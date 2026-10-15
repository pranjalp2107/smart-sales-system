
from pathlib import Path

import pandas as pd


def load_data(path=None):
    """Load raw sales data from a CSV file."""

    if path is None:
        project_root = Path(__file__).resolve().parent.parent
        path = project_root / "data" / "raw" / "sales_raw.csv"

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Sales data not found at: {path}. "
            "Run 'python src/generate_data.py' first."
        )

    df = pd.read_csv(path)

    print(f"Loaded {len(df)} rows from {path.name}")

    return df


if __name__ == "__main__":
    sales_df = load_data()
    print("\nFirst five rows:")
    print(sales_df.head())

    print("\nDataset columns:")
    print(sales_df.columns.tolist())