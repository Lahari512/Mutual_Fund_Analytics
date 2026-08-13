import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/raw/raw/08_investor_transactions.csv")

# -----------------------------
# 1. Age Group Distribution
# -----------------------------

age_counts = df["age_group"].value_counts().reset_index()
age_counts.columns = ["age_group", "count"]

fig1 = px.pie(
    age_counts,
    names="age_group",
    values="count",
    title="Investor Age Group Distribution"
)

fig1.write_html("dashboard/age_group_distribution.html")
fig1.write_image("dashboard/age_group_distribution.png")


# -----------------------------
# 2. SIP Amount by Age Group
# -----------------------------

sip_df = df[df["transaction_type"] == "SIP"]

fig2 = px.box(
    sip_df,
    x="age_group",
    y="amount_inr",
    title="SIP Amount by Age Group"
)

fig2.write_html("dashboard/sip_amount_boxplot.html")
fig2.write_image("dashboard/sip_amount_boxplot.png")


# -----------------------------
# 3. Gender Distribution
# -----------------------------

gender_counts = df["gender"].value_counts().reset_index()
gender_counts.columns = ["gender", "count"]

fig3 = px.pie(
    gender_counts,
    names="gender",
    values="count",
    title="Gender Distribution"
)

fig3.write_html("dashboard/gender_distribution.html")
fig3.write_image("dashboard/gender_distribution.png")


# Display charts
fig1.show()
fig2.show()
fig3.show()

print("Investor Demographics Dashboard created successfully!")
print("HTML and PNG files created successfully.")