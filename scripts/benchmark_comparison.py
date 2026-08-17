import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("BENCHMARK COMPARISON ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# Load NAV data
# ------------------------------------------------------------

nav = pd.read_csv(
    "data/processed/nav_history_clean.csv"
)

nav["date"] = pd.to_datetime(nav["date"])

# ------------------------------------------------------------
# Load fund master
# ------------------------------------------------------------

fund_master = pd.read_csv(
    "data/processed/01_fund_master.csv"
)

# ------------------------------------------------------------
# Get top 5 funds from scorecard
# ------------------------------------------------------------

scorecard = pd.read_csv(
    "data/processed/fund_scorecard.csv"
)

top5 = scorecard.sort_values(
    "overall_rank"
).head(5)

top5_codes = top5["amfi_code"].tolist()

top5_names = dict(
    zip(
        top5["amfi_code"],
        top5["scheme_name"]
    )
)

print("\nTop 5 Funds")
print("-" * 60)

print(
    top5[
        [
            "overall_rank",
            "scheme_name",
            "fund_score"
        ]
    ].to_string(index=False)
)

# ------------------------------------------------------------
# Filter NAV for top 5
# ------------------------------------------------------------

fund_nav = nav[
    nav["amfi_code"].isin(top5_codes)
].copy()

# ------------------------------------------------------------
# Create NAV pivot
# ------------------------------------------------------------

fund_pivot = fund_nav.pivot(
    index="date",
    columns="amfi_code",
    values="nav"
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

benchmark = benchmark[
    benchmark["index_name"].isin(
        ["NIFTY50", "NIFTY100"]
    )
].copy()

benchmark_pivot = benchmark.pivot(
    index="date",
    columns="index_name",
    values="close_value"
)

# ------------------------------------------------------------
# Combine fund + benchmark data
# ------------------------------------------------------------

combined = fund_pivot.join(
    benchmark_pivot,
    how="inner"
)

# ------------------------------------------------------------
# Restrict to latest 3 years
# ------------------------------------------------------------

latest_date = combined.index.max()

start_date = (
    latest_date
    - pd.DateOffset(years=3)
)

combined = combined[
    combined.index >= start_date
]

print(
    f"\nComparison period:"
    f" {combined.index.min().date()}"
    f" to {combined.index.max().date()}"
)

# ------------------------------------------------------------
# Calculate daily returns
# ------------------------------------------------------------

returns = combined.pct_change().dropna()

# ------------------------------------------------------------
# Calculate cumulative growth
# ------------------------------------------------------------

cumulative = (
    (1 + returns)
    .cumprod()
)

# ------------------------------------------------------------
# Rename fund columns
# ------------------------------------------------------------

rename_map = {
    code: top5_names[code]
    for code in top5_codes
}

cumulative = cumulative.rename(
    columns=rename_map
)

# ------------------------------------------------------------
# Benchmark comparison chart
# ------------------------------------------------------------

plt.figure(figsize=(15, 8))

for column in cumulative.columns:

    plt.plot(
        cumulative.index,
        cumulative[column],
        label=column,
        linewidth=2
    )

plt.title(
    "Top 5 Mutual Funds vs NIFTY50 and NIFTY100\n"
    "3-Year Cumulative Performance",
    fontsize=16
)

plt.xlabel("Date")
plt.ylabel(
    "Growth of ₹1"
)

plt.legend(
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.grid(
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "dashboard/benchmark_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ------------------------------------------------------------
# Tracking Error
# ------------------------------------------------------------

tracking_results = []

for code in top5_codes:

    fund_name = top5_names[code]

    # Fund vs NIFTY50
    fund_return = returns[code]

    nifty50_return = returns["NIFTY50"]

    nifty100_return = returns["NIFTY100"]

    # Tracking differences
    diff_50 = (
        fund_return - nifty50_return
    )

    diff_100 = (
        fund_return - nifty100_return
    )

    # Annualized tracking error
    tracking_error_50 = (
        diff_50.std()
        * np.sqrt(252)
    )

    tracking_error_100 = (
        diff_100.std()
        * np.sqrt(252)
    )

    tracking_results.append({
        "amfi_code": code,
        "scheme_name": fund_name,
        "tracking_error_nifty50_pct":
            tracking_error_50 * 100,
        "tracking_error_nifty100_pct":
            tracking_error_100 * 100
    })

tracking_df = pd.DataFrame(
    tracking_results
)

tracking_df[
    "tracking_error_nifty50_pct"
] = tracking_df[
    "tracking_error_nifty50_pct"
].round(2)

tracking_df[
    "tracking_error_nifty100_pct"
] = tracking_df[
    "tracking_error_nifty100_pct"
].round(2)

# ------------------------------------------------------------
# Save tracking error
# ------------------------------------------------------------

tracking_df.to_csv(
    "data/processed/tracking_error.csv",
    index=False
)

print("\nTracking Error")
print("-" * 60)

print(
    tracking_df.to_string(
        index=False
    )
)

print(
    "\nSaved:"
    " data/processed/tracking_error.csv"
)

print(
    "Chart:"
    " dashboard/benchmark_comparison.png"
)