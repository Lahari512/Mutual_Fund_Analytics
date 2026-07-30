import pandas as pd
from pathlib import Path

# Input and output folders
RAW_FOLDER = Path("data/raw/raw")
PROCESSED_FOLDER = Path("data/processed")

# Create processed folder if it doesn't exist
PROCESSED_FOLDER.mkdir(exist_ok=True)

# Read all CSV files
csv_files = sorted(RAW_FOLDER.glob("*.csv"))

print("=" * 60)
print("DATA CLEANING STARTED")
print("=" * 60)

for file in csv_files:

    print(f"\nProcessing: {file.name}")

    df = pd.read_csv(file)

    # -----------------------------
    # Remove duplicate rows
    # -----------------------------
    duplicate_rows = df.duplicated().sum()
    print(f"Duplicate Rows: {duplicate_rows}")

    df = df.drop_duplicates()

    # -----------------------------
    # Convert Date Columns
    # -----------------------------
    date_columns = [
        "date",
        "launch_date",
        "transaction_date",
        "portfolio_date",
        "month"
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column])

    # -----------------------------
    # Missing Values
    # -----------------------------
    print("\nMissing Values:")
    print(df.isnull().sum())

    # -----------------------------
    # Save cleaned file
    # -----------------------------
    output_file = PROCESSED_FOLDER / file.name

    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")

print("\nCleaning Completed Successfully!")