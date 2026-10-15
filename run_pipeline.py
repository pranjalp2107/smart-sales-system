
from pathlib import Path

from src.generate_data import generate_sales_data
from src.data_loader import load_data
from src.cleaning import clean_sales
from src.database import save_to_database


def run_pipeline():
    """Run the complete sales data pipeline."""

    project_root = Path(__file__).resolve().parent
    raw_path = project_root / "data" / "raw" / "sales_raw.csv"
    clean_path = project_root / "data" / "processed" / "clean_sales.csv"

    print("\n=== SMART SALES DATA PIPELINE ===")

    # Step 1: Generate raw data if it doesn't exist.
    if not raw_path.exists():
        print("\n1. Generating raw sales data...")
        generate_sales_data()
    else:
        print("\n1. Raw sales data already exists.")

    # Step 2: Load raw data.
    print("\n2. Loading raw data...")
    raw_df = load_data(raw_path)
    print("Raw rows:", len(raw_df))

    # Step 3: Clean the data.
    print("\n3. Cleaning sales data...")
    clean_df = clean_sales(raw_df)
    print("Clean rows:", len(clean_df))

    # Step 4: Save cleaned CSV.
    print("\n4. Saving cleaned CSV...")
    clean_path.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(clean_path, index=False)
    print("Saved to:", clean_path)

    # Step 5: Save SQLite database.
    print("\n5. Saving SQLite database...")
    save_to_database(clean_df)

    print("\n=== PIPELINE COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    run_pipeline()