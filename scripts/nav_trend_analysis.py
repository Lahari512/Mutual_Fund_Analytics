import pandas as pd
import plotly.express as px

#load NAV history
nav = pd.read_csv("data/raw/raw/02_nav_history.csv")

#load fund master
fund = pd.read_csv("data/raw/raw/01_fund_master.csv")

# Convert date column
nav["date"] = pd.to_datetime(nav["date"])

# Merge to get scheme names
df = nav.merge(
    fund[["amfi_code", "scheme_name"]],
    on="amfi_code",
    how="left"
)

# Create interactive line chart
fig = px.line(
    df,
    x="date",
    y="nav",
    color="scheme_name",
    title="Daily NAV Trend of All Mutual Fund Schemes (2022–2026)",
    labels={
        "date": "Date",
        "nav": "NAV",
        "scheme_name": "Scheme"
    }
)

# Highlight 2023 Bull Run
fig.add_vrect(
    x0="2023-01-01",
    x1="2023-12-31",
    fillcolor="green",
    opacity=0.15,
    line_width=0,
    annotation_text="2023 Bull Run",
    annotation_position="top left"
)

# Highlight 2024 Market Correction
fig.add_vrect(
    x0="2024-01-01",
    x1="2024-12-31",
    fillcolor="red",
    opacity=0.15,
    line_width=0,
    annotation_text="2024 Market Correction",
    annotation_position="top left"
)

# Improve layout
fig.update_layout(
    template="plotly_white",
    hovermode="x unified",
    height=700,
    width=1300
)

# Save interactive HTML
fig.write_html("dashboard/nav_trend_analysis.html")

# Display chart
fig.show()

print("NAV Trend Analysis completed successfully.")
print("Interactive dashboard saved to dashboard/nav_trend_analysis.html")