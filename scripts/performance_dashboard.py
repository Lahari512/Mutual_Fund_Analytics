import pandas as pd
import plotly.express as px

# Load scheme performance data
df = pd.read_csv("data/raw/raw/07_scheme_performance.csv")

# Create bar chart
fig = px.bar(
    df,
    x="scheme_name",
    y="return_3yr_pct",
    color="fund_house",
    hover_data=[
        "return_1yr_pct",
        "return_5yr_pct",
        "expense_ratio_pct",
        "morningstar_rating"
    ],
    title="3-Year Returns of Mutual Fund Schemes",
)

fig.update_layout(
    xaxis_title="Scheme Name",
    yaxis_title="3-Year Return (%)",
    xaxis_tickangle=-90,
    height=700,
    template="plotly_white"
)

fig.write_html("dashboard/performance_dashboard.html")

fig.show()

print("Performance dashboard created successfully.")