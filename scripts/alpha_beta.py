import pandas as pd
import numpy as np
from scipy.stats import linregress

print("=" * 60)
print("ALPHA & BETA ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# Load fund daily returns
# ------------------------------------------------------------

fund_returns = pd.read_csv(
    "data/processed/daily_returns.csv"
)

fund_returns["date"] = pd.to_datetime(
    fund_returns["date"]
)

# ------------------------------------------------------------
# Load benchmark data
# ------------------------------------------------------------

benchmark = pd.read_csv(
    "data/processed/10_benchmark_indices.csv"
)

benchmark["date"] = pd.to_datetime(
    benchmark["date"]
)

# Keep NIFTY100 only
nifty100 = benchmark[
    benchmark["index_name"] == "NIFTY100"
].copy()

# Sort by date
nifty100 = nifty100.sort_values("date")

# Calculate NIFTY100 daily return
nifty100["benchmark_return"] = (
    nifty100["close_value"].pct_change()
)

nifty100 = nifty100.dropna(
    subset=["benchmark_return"]
)

# Keep required columns
nifty100 = nifty100[
    ["date", "benchmark_return"]
]

# ------------------------------------------------------------
# Load fund master
# ------------------------------------------------------------

fund_master = pd.read_csv(
    "data/processed/01_fund_master.csv"
)

# ------------------------------------------------------------
# Regression for each fund
# ------------------------------------------------------------

results = []

for amfi_code, group in fund_returns.groupby(
    "amfi_code"
):

    # Select fund data
    fund_data = group[
        ["date", "daily_return"]
    ].copy()

    # Merge fund and NIFTY100 returns by date
    merged = fund_data.merge(
        nifty100,
        on="date",
        how="inner"
    )

    # Remove missing values
    merged = merged.dropna(
        subset=[
            "daily_return",
            "benchmark_return"
        ]
    )

    # Need enough observations
    if len(merged) < 30:
        continue

    # OLS regression
    regression = linregress(
        merged["benchmark_return"],
        merged["daily_return"]
    )

    # Daily alpha
    daily_alpha = regression.intercept

    # Annualized alpha
    annual_alpha = (
        daily_alpha * 252
    )

    # Beta
    beta = regression.slope

    # R-squared
    r_squared = regression.rvalue ** 2

    results.append({
        "amfi_code": amfi_code,
        "alpha_annual_pct":
            annual_alpha * 100,
        "beta":
            beta,
        "r_squared":
            r_squared,
        "observations":
            len(merged)
    })

# ------------------------------------------------------------
# Create DataFrame
# ------------------------------------------------------------

alpha_beta = pd.DataFrame(results)

# Add scheme names
alpha_beta = alpha_beta.merge(
    fund_master[
        ["amfi_code", "scheme_name"]
    ],
    on="amfi_code",
    how="left"
)

# Sort by alpha
alpha_beta = alpha_beta.sort_values(
    "alpha_annual_pct",
    ascending=False
)

# Round
alpha_beta["alpha_annual_pct"] = (
    alpha_beta["alpha_annual_pct"]
    .round(2)
)

alpha_beta["beta"] = (
    alpha_beta["beta"]
    .round(3)
)

alpha_beta["r_squared"] = (
    alpha_beta["r_squared"]
    .round(3)
)

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

alpha_beta.to_csv(
    "data/processed/alpha_beta.csv",
    index=False
)

# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print("\nTop 10 Funds by Annualized Alpha")
print("-" * 60)

print(
    alpha_beta[
        [
            "scheme_name",
            "alpha_annual_pct",
            "beta",
            "r_squared",
            "observations"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\nAlpha Statistics")
print("-" * 60)

print(
    alpha_beta["alpha_annual_pct"].describe()
)

print("\nBeta Statistics")
print("-" * 60)

print(
    alpha_beta["beta"].describe()
)

print(
    f"\nFunds processed: {len(alpha_beta)}"
)

print(
    "\nSaved: data/processed/alpha_beta.csv"
)