import requests
import pandas as pd
from pathlib import Path

# AMFI Codes
funds = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

# Output folder
output_folder = Path("data/raw/live_nav")
output_folder.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Fetching Live NAV Data")
print("=" * 60)

for fund_name, amfi_code in funds.items():

    url = f"https://api.mfapi.in/mf/{amfi_code}"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        nav_df = pd.DataFrame(data["data"])

        file_name = output_folder / f"{fund_name}.csv"

        nav_df.to_csv(file_name, index=False)

        print(f"✔ {fund_name} saved successfully.")

    else:
        print(f"❌ Failed to fetch {fund_name}")

print("\nAll NAV files downloaded successfully.")