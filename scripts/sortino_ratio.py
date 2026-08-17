import pandas as pd
import numpy as np

print("=" * 60)
print("SORTINO RATIO ANALYSIS")
print("=" * 60)

# Load daily returns
returns = pd.read_csv(
    "data/processed/daily_returns.csv"
)

returns["date"] = pd.to_datetime(
    returns["date"]
)

# Load fund master
fund = pd.read_csv(
    "data/processed/01_fund_master.csv"
)

# Parameters
RISK_FREE_RATE = 0.065
TRADING_DAYS = 252

# Daily risk-free rate
daily_rf = (
    (1 + RISK_FREE_RATE)
    ** (1 / TRADING_DAYS)
    - 1
)

results = []

for amfi_code, group in returns.groupby("amfi_code"):

    daily_returns = group["daily_return"].dropna()

    # Excess returns
    excess_returns = (
        daily_returns - daily_rf
    )

    # Annualized excess return
    annual_excess_return = (
        excess_returns.mean()
        * TRADING_DAYS
    )

    # Only negative excess returns
    downside_returns = excess_returns[
        excess_returns < 0
    ]

    # Downside deviation
    downside_deviation = np.sqrt(
        np.mean(
            downside_returns ** 2
        )
    ) * np.sqrt(TRADING_DAYS)

    # Sortino ratio
    if downside_deviation > 0:
        sortino = (
            annual_excess_return
            / downside_deviation
        )
    else:
        sortino = np.nan

    results.append({
        "amfi_code": amfi_code,
        "sortino_ratio": sortino,
        "downside_deviation_pct":
            downside_deviation * 100,
        "negative_days":
            len(downside_returns)
    })

sortino_df = pd.DataFrame(results)

# Add scheme names
sortino_df = sortino_df.merge(
    fund[
        ["amfi_code", "scheme_name"]
    ],
    on="amfi_code",
    how="left"
)

# Rank
sortino_df["sortino_rank"] = (
    sortino_df["sortino_ratio"]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)

# Sort
sortino_df = sortino_df.sort_values(
    "sortino_ratio",
    ascending=False
)

# Round
sortino_df["sortino_ratio"] = (
    sortino_df["sortino_ratio"].round(3)
)

sortino_df["downside_deviation_pct"] = (
    sortino_df["downside_deviation_pct"]
    .round(2)
)

# Save
sortino_df.to_csv(
    "data/processed/sortino_ratio.csv",
    index=False
)

print("\nTop 10 Funds by Sortino Ratio")
print("-" * 60)

print(
    sortino_df[
        [
            "scheme_name",
            "sortino_ratio",
            "downside_deviation_pct",
            "negative_days",
            "sortino_rank"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\nSortino Ratio Statistics")
print("-" * 60)

print(
    sortino_df["sortino_ratio"].describe()
)

print(
    "\nFunds processed:",
    len(sortino_df)
)

print(
    "\nSaved: data/processed/sortino_ratio.csv"
)