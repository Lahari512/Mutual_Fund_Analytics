import pandas as pd
import numpy as np

print("=" * 60)
print("CAGR ANALYSIS")
print("=" * 60)

# Load cleaned NAV history
nav = pd.read_csv(
    "data/processed/nav_history_clean.csv"
)

nav["date"] = pd.to_datetime(nav["date"])

# Load fund master for scheme names
fund = pd.read_csv(
    "data/processed/01_fund_master.csv"
)

# Sort data
nav = nav.sort_values(
    ["amfi_code", "date"]
)

# Latest available date
latest_date = nav["date"].max()

print(f"\nLatest NAV date: {latest_date.date()}")

results = []

# Calculate CAGR for every scheme
for amfi_code, group in nav.groupby("amfi_code"):

    group = group.sort_values("date")

    scheme_name = (
        fund.loc[
            fund["amfi_code"] == amfi_code,
            "scheme_name"
        ].iloc[0]
        if not fund.loc[
            fund["amfi_code"] == amfi_code
        ].empty
        else str(amfi_code)
    )

    latest_row = group.iloc[-1]

    result = {
        "amfi_code": amfi_code,
        "scheme_name": scheme_name
    }

    # CAGR periods
    for years in [1, 3, 5]:

        target_date = latest_date - pd.DateOffset(
            years=years
        )

        # Find closest available NAV on or before target date
        historical = group[
            group["date"] <= target_date
        ]

        if historical.empty:
            result[f"cagr_{years}yr_pct"] = np.nan
            continue

        start_row = historical.iloc[-1]

        start_nav = start_row["nav"]
        end_nav = latest_row["nav"]

        actual_days = (
            latest_row["date"] - start_row["date"]
        ).days

        actual_years = actual_days / 365.25

        if start_nav > 0 and actual_years > 0:
            cagr = (
                (end_nav / start_nav)
                ** (1 / actual_years)
                - 1
            ) * 100

            result[f"cagr_{years}yr_pct"] = cagr

        else:
            result[f"cagr_{years}yr_pct"] = np.nan

    results.append(result)

# Create comparison table
cagr_df = pd.DataFrame(results)

# Sort by 3-year CAGR
cagr_df = cagr_df.sort_values(
    "cagr_3yr_pct",
    ascending=False
)

# Round values
for col in [
    "cagr_1yr_pct",
    "cagr_3yr_pct",
    "cagr_5yr_pct"
]:
    cagr_df[col] = cagr_df[col].round(2)

# Save result
cagr_df.to_csv(
    "data/processed/cagr_analysis.csv",
    index=False
)

print("\nCAGR Comparison")
print("-" * 60)

print(
    cagr_df.to_string(index=False)
)

print("\nCAGR analysis completed.")
print(
    "Saved: data/processed/cagr_analysis.csv"
)