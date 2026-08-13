import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load investor transaction data
df = pd.read_csv("data/raw/raw/08_investor_transactions.csv")

# Keep SIP transactions only
sip_df = df[df["transaction_type"] == "SIP"].copy()

# Calculate total SIP amount by gender
gender_sip = (
    sip_df.groupby("gender")["amount_inr"]
    .sum()
    .reset_index()
)

# Create bar chart
plt.figure(figsize=(8, 6))

ax = sns.barplot(
    data=gender_sip,
    x="gender",
    y="amount_inr",
    errorbar=None
)

# Add values above bars
for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.0f",
        padding=3
    )

plt.title("Total SIP Amount by Gender", fontsize=16)
plt.xlabel("Gender")
plt.ylabel("Total SIP Amount (₹)")

plt.tight_layout()

# Save PNG
plt.savefig(
    "dashboard/sip_by_gender.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("SIP by Gender chart created successfully.")
print("PNG: dashboard/sip_by_gender.png")