import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/raw/raw/04_monthly_sip_inflows.csv")

# Convert month column
df["month"] = pd.to_datetime(df["month"])

# Create line chart
fig = px.line(
    df,
    x="month",
    y="sip_inflow_crore",
    markers=True,
    title="Monthly SIP Inflows (Jan 2022 - Dec 2025)"
)

# Highlight Dec 2025 high
fig.add_annotation(
    x=pd.Timestamp("2025-12-01"),
    y=31002,
    text="₹31,002 Cr (Dec 2025)",
    showarrow=True,
    arrowhead=2
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="SIP Inflow (₹ Crore)",
    template="plotly_white"
)

fig.write_html("dashboard/sip_time_series.html")

fig.show()