import pandas as pd

print("=" * 50)
print("INVESTOR TRANSACTIONS CLEANING")
print("=" * 50)

# Load dataset
df = pd.read_csv("data/processed/08_investor_transactions.csv")

# Convert date column
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

# Standardize transaction types
df["transaction_type"] = (
    df["transaction_type"]
    .str.strip()
    .str.title()
)

mapping = {
    "Sip": "SIP",
    "Lumpsum": "Lumpsum",
    "Redemption": "Redemption"
}

df["transaction_type"] = df["transaction_type"].replace(mapping)

# Validate amount
invalid_amount = (df["amount_inr"] <= 0).sum()

# Check KYC values
valid_kyc = ["Verified", "Pending"]

invalid_kyc = df.loc[
    ~df["kyc_status"].isin(valid_kyc),
    "kyc_status"
].unique()

print(f"Invalid Amount Records : {invalid_amount}")
print(f"Invalid Dates          : {df['transaction_date'].isna().sum()}")
print(f"Invalid KYC Values     : {list(invalid_kyc)}")

# Save cleaned file
df.to_csv(
    "data/processed/investor_transactions_clean.csv",
    index=False
)

print("\nCleaned file saved successfully.")