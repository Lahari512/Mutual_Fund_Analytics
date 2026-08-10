import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load NAV history
nav = pd.read_csv("data/raw/raw/02_nav_history.csv")

# Select 10 AMFI codes
selected_funds = [
    119551, 119552,
    120503, 118632,
    119092, 120841,
    119598, 119599,
    100016, 125497
]

nav = nav[nav["amfi_code"].isin(selected_funds)]

# Convert date
nav["date"] = pd.to_datetime(nav["date"])

# Pivot NAV values
pivot = nav.pivot(
    index="date",
    columns="amfi_code",
    values="nav"
)

# Daily returns
returns = pivot.pct_change().dropna()

# Correlation matrix
corr = returns.corr()

# Plot
plt.figure(figsize=(10,8))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    square=True
)

plt.title("Correlation Matrix of Daily NAV Returns")

plt.tight_layout()

plt.savefig("dashboard/nav_correlation_matrix.png", dpi=300)

plt.show()

print("NAV Correlation Matrix created successfully!")