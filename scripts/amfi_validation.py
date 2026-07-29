import pandas as pd

# Load the datasets
fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")

# Get unique AMFI codes
fund_codes = set(fund_master["amfi_code"])
nav_codes = set(nav_history["amfi_code"])

# Find missing codes
missing_codes = fund_codes - nav_codes

print("===== AMFI Code Validation =====")
print(f"Total AMFI Codes in Fund Master : {len(fund_codes)}")
print(f"Total AMFI Codes in NAV History : {len(nav_codes)}")

if len(missing_codes) == 0:
    print("\n✅ All AMFI codes from fund_master.csv are present in nav_history.csv")
else:
    print("\n❌ Missing AMFI Codes:")
    for code in sorted(missing_codes):
        print(code)