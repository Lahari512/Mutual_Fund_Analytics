import pandas as pd
import numpy as np

print("=" * 60)
print("TRACKING ERROR ANALYSIS")
print("=" * 60)

# Load NAV history
nav = pd.read_csv("data/processed/nav_history_clean.csv")
nav["date"] = pd.to_datetime(nav["date"])

# Load fund scorecard
scorecard = pd.read_csv("data/processed/fund_scorecard.csv")

# Top 5 funds
top5 = (
    scorecard
    .sort_values("overall_rank")
    .head(5)
)

print("\nTop 5 Funds")
print("-" * 60)
print(
    top5[
        ["overall_rank", "scheme_name", "fund_score"]
    ].to_string(index=False)
)

# Top 5 AMFI codes
top5_codes = top5["amfi_code"].tolist()

# Fund NAV pivot
fund_nav = nav[
    nav["amfi_code"].isin(top5_codes)
]

fund_pivot = fund_nav.pivot(
    index="date",
    columns="amfi_code",
    values="nav"
)

# Load benchmarks
benchmark = pd.read_csv(
    "data/processed/10_benchmark_indices.csv"
)

benchmark["date"] = pd.to_datetime(
    benchmark["date"]
)

benchmark = benchmark[
    benchmark["index_name"].isin(
        ["NIFTY50", "NIFTY100"]
    )
]

benchmark_pivot = benchmark.pivot(
    index="date",
    columns="index_name",
    values="close_value"
)

# Combine
combined = fund_pivot.join(
    benchmark_pivot,
    how="inner"
)

# Latest 3 years
latest_date = combined.index.max()

start_date = (
    latest_date - pd.DateOffset(years=3)
)

combined = combined[
    combined.index >= start_date
]

print(
    f"\nPeriod: {combined.index.min().date()} "
    f"to {combined.index.max().date()}"
)

# Daily returns
returns = combined.pct_change().dropna()

# Calculate tracking error
results = []

for _, row in top5.iterrows():

    code = row["amfi_code"]
    name = row["scheme_name"]

    fund_return = returns[code]

    for benchmark_name in ["NIFTY50", "NIFTY100"]:

        benchmark_return = returns[
            benchmark_name
        ]

        active_return = (
            fund_return - benchmark_return
        )

        tracking_error = (
            active_return.std()
            * np.sqrt(252)
        )

        results.append({
            "amfi_code": code,
            "scheme_name": name,
            "benchmark": benchmark_name,
            "tracking_error_pct":
                round(tracking_error * 100, 2)
        })

# Create dataframe
tracking_df = pd.DataFrame(results)

print("\nTracking Error")
print("-" * 60)

print(
    tracking_df.to_string(index=False)
)

# Save
tracking_df.to_csv(
    "data/processed/tracking_error.csv",
    index=False
)

print("\nTracking error calculation completed.")
print(
    "Saved: data/processed/tracking_error.csv"
)