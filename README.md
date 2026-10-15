
Smart Sales System
Project Overview

The Smart Sales System processes sales data to prepare it for analysis, forecasting, and visualization.

My Contribution — Data Engineering

My responsibilities include:

Generating sample raw sales data.
Loading CSV data using Pandas.
Cleaning invalid records and duplicate rows.
Handling missing values and standardizing text.
Calculating revenue and date-related columns.
Saving cleaned data to CSV and SQLite.
Creating and testing the data pipeline.
Project Structure
src/generate_data.py — Generates sample sales data.
src/data_loader.py — Loads raw sales data.
src/cleaning.py — Cleans sales records.
src/database.py — Saves and loads SQLite data.
run_pipeline.py — Runs the complete data pipeline.
tests/ — Contains automated tests.
data/raw/ — Stores raw sales data.
data/processed/ — Stores cleaned sales data.
data/sales.db — SQLite database.
Setup

Create and activate a virtual environment, then install dependencies:

python -m venv venv


On Windows PowerShell:

.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

Run the Project

Generate sample data:

python src/generate_data.py


Run the complete pipeline:

python run_pipeline.py


Run automated tests:

python -m pytest -v

Outputs
data/raw/sales_raw.csv
data/processed/clean_sales.csv
data/sales.db