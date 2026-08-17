import pandas as pd
import numpy as np

print("=" * 60)
print("SHARPE RATIO ANALYSIS")
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

# Risk-free rate
RISK_FREE_RATE = 0.065
TRADING_DAYS = 252

# Convert annual risk-free rate to daily rate
daily_rf = (
    (1 + RISK_FREE_RATE)
    ** (1 / TRADING_DAYS)
    - 1
)

print(f"\nAnnual risk-free rate: {RISK_FREE_RATE:.2%}")
print(f"Daily risk-free rate: {daily_rf:.8f}")

results = []

for amfi_code, group in returns.groupby("amfi_code"):

    daily_returns = group["daily_return"].dropna()

    # Daily excess returns
    excess_returns = (
        daily_returns - daily_rf
    )

    # Annualized excess return
    annual_excess_return = (
        excess_returns.mean()
        * TRADING_DAYS
    )

    # Annualized volatility
    annual_volatility = (
        daily_returns.std()
        * np.sqrt(TRADING_DAYS)
    )

    # Sharpe ratio
    if annual_volatility > 0:
        sharpe = (
            annual_excess_return
            / annual_volatility
        )
    else:
        sharpe = np.nan

    results.append({
        "amfi_code": amfi_code,
        "sharpe_ratio": sharpe,
        "annualized_return_pct":
            daily_returns.mean()
            * TRADING_DAYS
            * 100,
        "annualized_volatility_pct":
            annual_volatility * 100
    })

sharpe_df = pd.DataFrame(results)

# Add scheme names
sharpe_df = sharpe_df.merge(
    fund[
        ["amfi_code", "scheme_name"]
    ],
    on="amfi_code",
    how="left"
)

# Rank funds
sharpe_df["sharpe_rank"] = (
    sharpe_df["sharpe_ratio"]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)

# Sort
sharpe_df = sharpe_df.sort_values(
    "sharpe_ratio",
    ascending=False
)

# Round
sharpe_df["sharpe_ratio"] = (
    sharpe_df["sharpe_ratio"].round(3)
)

sharpe_df["annualized_return_pct"] = (
    sharpe_df["annualized_return_pct"].round(2)
)

sharpe_df["annualized_volatility_pct"] = (
    sharpe_df["annualized_volatility_pct"].round(2)
)

# Save
sharpe_df.to_csv(
    "data/processed/sharpe_ratio.csv",
    index=False
)

print("\nTop 10 Funds by Sharpe Ratio")
print("-" * 60)

print(
    sharpe_df[
        [
            "scheme_name",
            "sharpe_ratio",
            "annualized_return_pct",
            "annualized_volatility_pct",
            "sharpe_rank"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\nSharpe Ratio Statistics")
print("-" * 60)
print(
    sharpe_df["sharpe_ratio"].describe()
)

print("\nFunds processed:", len(sharpe_df))

print(
    "\nSaved: data/processed/sharpe_ratio.csv"
)