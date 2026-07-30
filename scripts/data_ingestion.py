import pandas as pd
from pathlib import Path

# Folder containing CSV files
DATA_FOLDER = Path("data/raw/raw")

# Get all CSV files
csv_files = sorted(DATA_FOLDER.glob("*.csv"))

print("=" * 60)
print(f"Found {len(csv_files)} CSV files")
print("=" * 60)

for file in csv_files:
    print(f"\nProcessing: {file.name}")

    try:
        df = pd.read_csv(file)

        print("Shape:")
        print(df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("-" * 60)

    except Exception as e:
        print(f"Error reading {file.name}: {e}")