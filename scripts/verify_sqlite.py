import pandas as pd
from sqlalchemy import create_engine

# Connect to SQLite database
engine = create_engine("sqlite:///mutual_fund_analytics.db")

# Tables and corresponding CSV files
tables = {
    "fund_master": "data/processed/01_fund_master.csv",
    "nav_history": "data/processed/nav_history_clean.csv",
    "scheme_performance": "data/processed/scheme_performance_clean.csv",
    "investor_transactions": "data/processed/investor_transactions_clean.csv"
}

print("=" * 60)
print("SQLITE ROW COUNT VALIDATION")
print("=" * 60)

for table, csv_file in tables.items():

    csv_rows = len(pd.read_csv(csv_file))

    sql_rows = pd.read_sql(
        f"SELECT COUNT(*) AS total FROM {table}",
        engine
    ).iloc[0]["total"]

    print(f"\nTable: {table}")
    print(f"CSV Rows    : {csv_rows}")
    print(f"SQLite Rows : {sql_rows}")

    if csv_rows == sql_rows:
        print("Status      : PASS ✅")
    else:
        print("Status      : FAIL ❌")