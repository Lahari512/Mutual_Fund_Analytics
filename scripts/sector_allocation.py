import pandas as pd
import plotly.express as px

# Load portfolio data
df = pd.read_csv("data/raw/raw/09_portfolio_holdings.csv")

# Aggregate sector weights
sector = (
    df.groupby("sector")["weight_pct"]
    .sum()
    .reset_index()
)

# Create donut chart
fig = px.pie(
    sector,
    names="sector",
    values="weight_pct",
    hole=0.5,
    title="Sector Allocation Across Equity Funds"
)

fig.write_html("dashboard/sector_allocation.html")

fig.show()

print("Sector Allocation chart created successfully!")