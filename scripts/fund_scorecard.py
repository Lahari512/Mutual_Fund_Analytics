import pandas as pd
import numpy as np

print("=" * 60)
print("FUND SCORECARD")
print("=" * 60)

# ------------------------------------------------------------
# Load datasets
# ------------------------------------------------------------

cagr = pd.read_csv(
    "data/processed/cagr_analysis.csv"
)

sharpe = pd.read_csv(
    "data/processed/sharpe_ratio.csv"
)

alpha_beta = pd.read_csv(
    "data/processed/alpha_beta.csv"
)

drawdown = pd.read_csv(
    "data/processed/max_drawdown.csv"
)

performance = pd.read_csv(
    "data/processed/scheme_performance_clean.csv"
)

# ------------------------------------------------------------
# Select required columns
# ------------------------------------------------------------

cagr = cagr[
    [
        "amfi_code",
        "scheme_name",
        "cagr_3yr_pct"
    ]
]

sharpe = sharpe[
    [
        "amfi_code",
        "sharpe_ratio"
    ]
]

alpha_beta = alpha_beta[
    [
        "amfi_code",
        "alpha_annual_pct"
    ]
]

drawdown = drawdown[
    [
        "amfi_code",
        "max_drawdown_pct"
    ]
]

performance = performance[
    [
        "amfi_code",
        "expense_ratio_pct"
    ]
]

# ------------------------------------------------------------
# Merge all metrics
# ------------------------------------------------------------

scorecard = cagr.merge(
    sharpe,
    on="amfi_code",
    how="inner"
)

scorecard = scorecard.merge(
    alpha_beta,
    on="amfi_code",
    how="inner"
)

scorecard = scorecard.merge(
    drawdown,
    on="amfi_code",
    how="inner"
)

scorecard = scorecard.merge(
    performance,
    on="amfi_code",
    how="inner"
)

print(
    f"\nFunds after merging: {len(scorecard)}"
)

# ------------------------------------------------------------
# Handle missing values
# ------------------------------------------------------------

required_metrics = [
    "cagr_3yr_pct",
    "sharpe_ratio",
    "alpha_annual_pct",
    "expense_ratio_pct",
    "max_drawdown_pct"
]

missing = scorecard[
    required_metrics
].isna().sum()

print("\nMissing values:")
print(missing)

# Keep funds with complete metrics
scorecard = scorecard.dropna(
    subset=required_metrics
).copy()

print(
    f"\nFunds used in scorecard: {len(scorecard)}"
)

# ------------------------------------------------------------
# Convert metrics into 0–100 percentile scores
# ------------------------------------------------------------

# Higher is better:
# 3-year CAGR
scorecard["return_score"] = (
    scorecard["cagr_3yr_pct"]
    .rank(pct=True) * 100
)

# Higher is better:
# Sharpe
scorecard["sharpe_score"] = (
    scorecard["sharpe_ratio"]
    .rank(pct=True) * 100
)

# Higher is better:
# Alpha
scorecard["alpha_score"] = (
    scorecard["alpha_annual_pct"]
    .rank(pct=True) * 100
)

# Lower is better:
# Expense ratio
scorecard["expense_score"] = (
    scorecard["expense_ratio_pct"]
    .rank(
        pct=True,
        ascending=False
    ) * 100
)

# Lower / less negative is better:
# Maximum drawdown
scorecard["drawdown_score"] = (
    scorecard["max_drawdown_pct"]
    .rank(
        pct=True,
        ascending=False
    ) * 100
)

# ------------------------------------------------------------
# Weighted composite score
# ------------------------------------------------------------

scorecard["fund_score"] = (
    0.30 * scorecard["return_score"]
    + 0.25 * scorecard["sharpe_score"]
    + 0.20 * scorecard["alpha_score"]
    + 0.15 * scorecard["expense_score"]
    + 0.10 * scorecard["drawdown_score"]
)

# Round
scorecard["fund_score"] = (
    scorecard["fund_score"].round(2)
)

# ------------------------------------------------------------
# Final ranking
# ------------------------------------------------------------

scorecard["overall_rank"] = (
    scorecard["fund_score"]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)

scorecard = scorecard.sort_values(
    [
        "overall_rank",
        "scheme_name"
    ]
)

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

output_columns = [
    "overall_rank",
    "amfi_code",
    "scheme_name",
    "cagr_3yr_pct",
    "sharpe_ratio",
    "alpha_annual_pct",
    "expense_ratio_pct",
    "max_drawdown_pct",
    "return_score",
    "sharpe_score",
    "alpha_score",
    "expense_score",
    "drawdown_score",
    "fund_score"
]

scorecard[
    output_columns
].to_csv(
    "data/processed/fund_scorecard.csv",
    index=False
)

# ------------------------------------------------------------
# Display top 10
# ------------------------------------------------------------

print("\nTOP 10 FUNDS")
print("-" * 60)

print(
    scorecard[
        [
            "overall_rank",
            "scheme_name",
            "fund_score",
            "cagr_3yr_pct",
            "sharpe_ratio",
            "alpha_annual_pct",
            "expense_ratio_pct",
            "max_drawdown_pct"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\nScore Statistics")
print("-" * 60)

print(
    scorecard["fund_score"].describe()
) 

print(
    "\nSaved: data/processed/fund_scorecard.csv"
)

print(
    f"Funds scored: {len(scorecard)}"
)