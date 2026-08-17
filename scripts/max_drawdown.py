import pandas as pd
import numpy as np

print("=" * 60)
print("MAXIMUM DRAWDOWN ANALYSIS")
print("=" * 60)

# Load NAV history
nav = pd.read_csv(
    "data/processed/nav_history_clean.csv"
)

nav["date"] = pd.to_datetime(nav["date"])

# Load fund master
fund = pd.read_csv(
    "data/processed/01_fund_master.csv"
)

nav = nav.sort_values(
    ["amfi_code", "date"]
)

results = []

for amfi_code, group in nav.groupby("amfi_code"):

    group = group.sort_values("date").copy()

    # Running maximum NAV
    group["running_max"] = (
        group["nav"].cummax()
    )

    # Drawdown
    group["drawdown"] = (
        group["nav"] /
        group["running_max"]
        - 1
    )

    # Maximum drawdown
    trough_idx = group["drawdown"].idxmin()

    trough_row = group.loc[trough_idx]

    max_drawdown = trough_row["drawdown"]

    # Peak before the trough
    peak_data = group.loc[
        group.index <= trough_idx
    ]

    peak_idx = peak_data["nav"].idxmax()
    peak_row = group.loc[peak_idx]

    # Fund name
    fund_match = fund[
        fund["amfi_code"] == amfi_code
    ]

    if not fund_match.empty:
        scheme_name = fund_match[
            "scheme_name"
        ].iloc[0]
    else:
        scheme_name = str(amfi_code)

    results.append({
        "amfi_code": amfi_code,
        "scheme_name": scheme_name,
        "max_drawdown_pct":
            max_drawdown * 100,
        "peak_date":
            peak_row["date"],
        "peak_nav":
            peak_row["nav"],
        "trough_date":
            trough_row["date"],
        "trough_nav":
            trough_row["nav"],
        "drawdown_days":
            (
                trough_row["date"]
                - peak_row["date"]
            ).days
    })

# Create result DataFrame
dd_df = pd.DataFrame(results)

# Sort from worst to best
dd_df = dd_df.sort_values(
    "max_drawdown_pct"
)

# Round
dd_df["max_drawdown_pct"] = (
    dd_df["max_drawdown_pct"].round(2)
)

dd_df["peak_nav"] = (
    dd_df["peak_nav"].round(4)
)

dd_df["trough_nav"] = (
    dd_df["trough_nav"].round(4)
)

# Save
dd_df.to_csv(
    "data/processed/max_drawdown.csv",
    index=False
)

print("\nWorst 10 Funds by Maximum Drawdown")
print("-" * 60)

print(
    dd_df[
        [
            "scheme_name",
            "max_drawdown_pct",
            "peak_date",
            "trough_date",
            "drawdown_days"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\nMaximum Drawdown Statistics")
print("-" * 60)

print(
    dd_df["max_drawdown_pct"].describe()
)

print(
    f"\nFunds processed: {len(dd_df)}"
)

print(
    "\nSaved: data/processed/max_drawdown.csv"
)