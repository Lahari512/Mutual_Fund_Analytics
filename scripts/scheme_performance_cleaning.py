import pandas as pd

print("=" * 60)
print("SCHEME PERFORMANCE CLEANING")
print("=" * 60)

# Load dataset
df = pd.read_csv("data/processed/07_scheme_performance.csv")

# Return columns
return_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct"
]

# Convert return columns to numeric
for col in return_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("\nChecking Return Columns...")

for col in return_columns:
    invalid = df[col].isna().sum()
    print(f"{col}: {invalid} invalid values")

# Expense Ratio Validation
expense_anomalies = df[
    (df["expense_ratio_pct"] < 0.1) |
    (df["expense_ratio_pct"] > 2.5)
]

print("\nExpense Ratio Check")
print("-------------------------")
print("Anomalies Found:", len(expense_anomalies))

# Save anomaly file (if any)
expense_anomalies.to_csv(
    "data/processed/expense_ratio_anomalies.csv",
    index=False
)

# Save cleaned dataset
df.to_csv(
    "data/processed/scheme_performance_clean.csv",
    index=False
)

print("\nCleaning completed successfully.")
print("Cleaned file saved:")
print("data/processed/scheme_performance_clean.csv")