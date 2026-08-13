import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load AUM dataset
df = pd.read_csv("data/raw/raw/03_aum_by_fund_house.csv")

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Extract year
df["year"] = df["date"].dt.year

# Keep 2022–2025
df = df[df["year"].between(2022, 2025)].copy()

# Sort data
df = df.sort_values(["year", "fund_house"])

# Get fund house order
fund_houses = sorted(df["fund_house"].unique())

# Create figure
plt.figure(figsize=(16, 8))

# Grouped bar chart
ax = sns.barplot(
    data=df,
    x="fund_house",
    y="aum_lakh_crore",
    hue="year",
    order=fund_houses,
    errorbar=None
)

# Add title and labels
plt.title(
    "AUM Growth by Fund House (2022–2025)",
    fontsize=18
)

plt.xlabel("Fund House")
plt.ylabel("AUM (₹ Lakh Crore)")

plt.xticks(rotation=45, ha="right")

# Find SBI position
sbi_index = fund_houses.index("SBI Mutual Fund")

# Get SBI 2025 value
sbi_2025 = df[
    (df["fund_house"] == "SBI Mutual Fund") &
    (df["year"] == 2025)
]

if not sbi_2025.empty:

    sbi_value = sbi_2025["aum_lakh_crore"].iloc[0]

    # Calculate x-position for 2025 bar
    num_years = df["year"].nunique()
    bar_width = 0.8 / num_years

    year_position = list(sorted(df["year"].unique())).index(2025)

    x_position = (
        sbi_index
        - 0.4
        + bar_width / 2
        + year_position * bar_width
    )

    # Annotate SBI 2025
    plt.annotate(
        f"SBI 2025: ₹{sbi_value:.1f} Lakh Cr",
        xy=(x_position, sbi_value),
        xytext=(x_position, sbi_value + 1),
        ha="center",
        arrowprops=dict(arrowstyle="->")
    )

# Save PNG
plt.tight_layout()

plt.savefig(
    "dashboard/aum_growth_by_year.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("AUM Growth chart created successfully.")
print("PNG: dashboard/aum_growth_by_year.png")