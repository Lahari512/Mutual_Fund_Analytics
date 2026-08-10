import pandas as pd
from sqlalchemy import create_engine

print("=" * 60)
print("LOADING CLEANED DATASETS INTO SQLITE")
print("=" * 60)

# Create SQLite database
engine = create_engine("sqlite:///mutual_fund_analytics.db")

# List of cleaned datasets
datasets = {
    "fund_master": "data/processed/01_fund_master.csv",
    "nav_history": "data/processed/nav_history_clean.csv",
    "aum_by_fund_house": "data/processed/03_aum_by_fund_house.csv",
    "scheme_performance": "data/processed/scheme_performance_clean.csv",
    "investor_transactions": "data/processed/investor_transactions_clean.csv"
}

# Load each dataset
for table_name, file_path in datasets.items():

    print(f"\nLoading {table_name}...")

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"{table_name} loaded successfully.")
    print(f"Rows Loaded: {len(df)}")

print("\nAll datasets loaded successfully!")