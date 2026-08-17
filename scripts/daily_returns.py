import pandas as pd
import numpy as np

print("=" * 60)
print("DAILY RETURN CALCULATION")
print("=" * 60)

# Load cleaned NAV history
nav = pd.read_csv(
    "data/processed/nav_history_clean.csv"
)

# Convert date
nav["date"] = pd.to_datetime(nav["date"])

# Sort correctly
nav = nav.sort_values(
    ["amfi_code", "date"]
)

# Calculate daily return for each scheme
nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
    .pct_change()
)

# Remove rows where return cannot be calculated
returns = nav.dropna(
    subset=["daily_return"]
).copy()

# Validate number of schemes
scheme_count = returns["amfi_code"].nunique()

print(f"\nNumber of schemes: {scheme_count}")
print(f"Total return observations: {len(returns):,}")

# Validate return distribution
print("\nDaily Return Statistics")
print("-" * 60)

print(
    returns["daily_return"].describe()
)

# Check extreme returns
print("\nExtreme Return Check")
print("-" * 60)

print(
    "Returns > +20%:",
    (returns["daily_return"] > 0.20).sum()
)

print(
    "Returns < -20%:",
    (returns["daily_return"] < -0.20).sum()
)

print(
    "Missing returns:",
    returns["daily_return"].isna().sum()
)

# Check infinite values
print(
    "Infinite returns:",
    np.isinf(
        returns["daily_return"]
    ).sum()
)

# Save daily returns
returns.to_csv(
    "data/processed/daily_returns.csv",
    index=False
)

print("\nDaily return calculation completed.")
print(
    "Saved: data/processed/daily_returns.csv"
)