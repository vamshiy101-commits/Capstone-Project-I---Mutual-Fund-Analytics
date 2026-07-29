import requests
import pandas as pd
import os

# Create output folder if it doesn't exist
os.makedirs("data/raw/live_nav", exist_ok=True)

# Mutual fund schemes
schemes = {
    "HDFC_Top_100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for name, code in schemes.items():
    print(f"\nFetching {name}...")

    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        df = pd.DataFrame(data["data"])

        filename = f"data/raw/live_nav/{name}.csv"

        df.to_csv(filename, index=False)

        print(f"Saved: {filename}")

    else:
        print(f"Failed to fetch {name}")