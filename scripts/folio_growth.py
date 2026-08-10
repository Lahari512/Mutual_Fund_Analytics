import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/raw/raw/06_industry_folio_count.csv")

# Convert month column to datetime
df["month"] = pd.to_datetime(df["month"])

# Create line chart
fig = px.line(
    df,
    x="month",
    y="total_folios_crore",
    markers=True,
    title="Industry Folio Count Growth (Jan 2022 – Dec 2025)"
)

# Add milestone annotations
fig.add_annotation(
    x=pd.Timestamp("2022-01-01"),
    y=13.26,
    text="13.26 Cr (Jan 2022)",
    showarrow=True,
    arrowhead=2
)

fig.add_annotation(
    x=pd.Timestamp("2025-12-01"),
    y=26.12,
    text="26.12 Cr (Dec 2025)",
    showarrow=True,
    arrowhead=2
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="Total Folios (Crore)"
)

# Save dashboard
fig.write_html("dashboard/folio_growth.html")

fig.show()

print("Folio Growth Dashboard created successfully!")