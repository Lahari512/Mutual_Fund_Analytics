import pandas as pd

# -----------------------------
# Load NAV History
# -----------------------------
nav = pd.read_csv("data/raw/raw/02_nav_history.csv")

print("=" * 50)
print("NAV HISTORY CLEANING")
print("=" * 50)

# -----------------------------
# Convert date to datetime
# -----------------------------
nav["date"] = pd.to_datetime(nav["date"], errors="coerce")

# -----------------------------
# Sort by AMFI code and date
# -----------------------------
nav = nav.sort_values(by=["amfi_code", "date"])

# -----------------------------
# Remove duplicate rows
# -----------------------------
duplicate_count = nav.duplicated().sum()
nav = nav.drop_duplicates()

# -----------------------------
# Forward-fill missing NAV
# -----------------------------
nav["nav"] = nav.groupby("amfi_code")["nav"].ffill()

# -----------------------------
# Validation
# -----------------------------
missing_dates = nav["date"].isna().sum()
missing_nav = nav["nav"].isna().sum()
invalid_nav = (nav["nav"] <= 0).sum()

# -----------------------------
# Print Summary
# -----------------------------
print(f"Duplicate Rows Removed : {duplicate_count}")
print(f"Missing Dates          : {missing_dates}")
print(f"Missing NAV Values     : {missing_nav}")
print(f"Invalid NAV Values     : {invalid_nav}")

# -----------------------------
# Save cleaned file
# -----------------------------
nav.to_csv(
    "data/processed/nav_history_clean.csv",
    index=False
)

print("\nCleaned file saved successfully.")
print("Location: data/processed/nav_history_clean.csv")