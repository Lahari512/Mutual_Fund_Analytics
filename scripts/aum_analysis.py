import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/raw/raw/03_aum_by_fund_house.csv")

# Keep latest available date
latest = df["date"].max()
latest_df = df[df["date"] == latest]

# Sort by AUM
latest_df = latest_df.sort_values(
    by="aum_crore",
    ascending=False
)

# Plot
fig = px.bar(
    latest_df,
    x="fund_house",
    y="aum_crore",
    color="aum_crore",
    text="aum_crore",
    title=f"AUM by Fund House ({latest})"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Fund House",
    yaxis_title="AUM (Crore ₹)",
    height=650
)

fig.update_traces(textposition="outside")

fig.write_html("dashboard/aum_analysis.html")

fig.show()

print("AUM dashboard created successfully.")