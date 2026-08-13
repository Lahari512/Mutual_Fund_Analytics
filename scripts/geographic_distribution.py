import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("data/raw/raw/08_investor_transactions.csv")

# SIP transactions only
sip_df = df[df["transaction_type"] == "SIP"]

# -----------------------------
# 1. SIP Amount by State
# -----------------------------

state_data = (
    sip_df.groupby("state")["amount_inr"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

fig1 = px.bar(
    state_data,
    x="amount_inr",
    y="state",
    orientation="h",
    title="SIP Amount by State"
)

fig1.write_html("dashboard/state_sip_distribution.html")
fig1.write_image("dashboard/state_sip_distribution.png")


# -----------------------------
# 2. T30 vs B30 City Tier
# -----------------------------

tier_data = (
    sip_df["city_tier"]
    .value_counts()
    .reset_index()
)

tier_data.columns = ["city_tier", "count"]

fig2 = px.pie(
    tier_data,
    names="city_tier",
    values="count",
    title="T30 vs B30 City Tier Distribution"
)

fig2.write_html("dashboard/city_tier_distribution.html")
fig2.write_image("dashboard/city_tier_distribution.png")


# Display charts
fig1.show()
fig2.show()

print("Geographic Distribution Dashboard created successfully!")
print("PNG files created:")
print(" - dashboard/state_sip_distribution.png")
print(" - dashboard/city_tier_distribution.png")