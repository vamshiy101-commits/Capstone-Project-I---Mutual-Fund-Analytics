#Mutual_Fund_ETL_Project_Day - 02
#Data cleaning
import pandas as pd
import numpy as np
print("Data Cleaning Started")

#Read CSV file
nav = pd.read_csv("data/raw/02_nav_history.csv")
transaction = pd.read_csv('data/raw/08_investor_transactions.csv')
performance = pd.read_csv('data/raw/07_scheme_performance.csv')

print('csv files loaded successfully')
print('\nNav History')
print(nav.head())
print('\nInvestor Transactions')
print(transaction.head())
print('\nScheme Performance')
print(performance.head())

print('\n======Nav Information========')
print(nav.info())

print('\n======Missing Values======')
print(nav.isnull().sum())

print('\n======duplicates rows======')
print(nav.duplicated().sum())

print('\n=====convert date to datetime ===')
nav['date'] = pd.to_datetime(nav['date'])
print(nav.dtypes)

print('\n=====sorting data======')
nav = nav.sort_values(['amfi_code','date'])
print(nav.head())

print('\n===== forward fill nav====')
nav['nav'] = nav.groupby('amfi_code')['nav'].ffill()
print(nav.head())

print('\n=====valodating nav=====')
invalid_nav = nav[nav['nav']<=0]
print('Invalid nav rows',len(invalid_nav))

nav.to_csv('data/processed/02_nav_history.csv',index=False)
print('\nNav history data cleaned and saved successfully')



#Clean 08_investor_transactions.csv
#check informantion
print(transaction.info())
#check for missing values
print('\nMissing Values')
print(transaction.isnull().sum())
#check the duplicates
print('\nDuplicate Rows')
print(transaction.duplicated().sum())
#convert transaction date to datetime
transaction['transaction_date'] = pd.to_datetime(transaction['transaction_date'])
print('\nTransaction date datatype')
print(transaction['transaction_date'].dtypes)

print('\n unique transaction types')
print(transaction['transaction_type'].unique())

transaction['transaction_type'] = transaction['transaction_type'].replace({
    'sip':'SIP',
    'Sip':'SIP',
    'systematic_investment_plan':'SIP',
    'lumpsum':'Lumpsum',
    'lump sum':'Lumpsum',
    'redeem':'Redemption',
    'Redeem':'Redemption'
})

print('\ntransaction types after cleaning')
print(transaction['transaction_type'].unique())

#validation amount > 0
invalid_amount = transaction[transaction['amount_inr'] <= 0]
print('\ninvalid_amount rows',len(invalid_amount))

#check KYC status
print('\nunique KYC status')
print(transaction['kyc_status'].unique())
valid_kyc = ['verified','pending','rejected']
invalid_kyc = transaction[
    transaction['kyc_status'].isin(valid_kyc)
]
print('Invalid KYC status rows',len(invalid_kyc))

#Remove duplicates rows
transaction = transaction.drop_duplicates()


#save the cleaned file
transaction.to_csv('data/processed/08_investor_transactions.csv',index=False)
print('\nInvestor transactions data cleaned and saved successfully')


#=== clean 07_scheme_performance.csv===
print(performance.info())
print(performance.isnull().sum())
print(performance.duplicated().sum())
print(performance.dtypes)
print(performance.columns)


print("\n========== VALIDATING RETURN COLUMNS ==========")
return_columns = [
    'return_1yr_pct',
    'return_3yr_pct',
    'return_5yr_pct',
]
for col in return_columns:
    performance[col] = pd.to_numeric(performance[col], errors='coerce')
print("Return columns validated successfully.")


invalid_return = performance[
    (performance['expense_ratio_pct'] < 0.1) |
    (performance['expense_ratio_pct'] > 2.5) 
]
print("Invalid Expense Ratio Rows:", len(invalid_return))




print("\n========== CHECKING RETURN ANOMALIES ==========")

anomalies = performance[
    (performance["return_1yr_pct"] > 100) |
    (performance["return_1yr_pct"] < -100)
]

print("Anomalies Found:", len(anomalies))



performance.to_csv(
    "data/processed/07_scheme_performance.csv",
    index=False
)

print("\nScheme Performance cleaned and saved successfully!")

# -------------------------------
# Clean scheme_performance.csv
# -------------------------------

scheme = pd.read_csv("data/raw/07_scheme_performance.csv")

print("\nScheme Performance Preview")
print(scheme.head())


print("\nInformation")
print(scheme.info())

print("\nMissing Values")
print(scheme.isnull().sum())

print("\nDuplicate Rows")
print(scheme.duplicated().sum())


scheme.drop_duplicates(inplace=True)


numeric_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct",
    "alpha",
    "beta",
    "sharpe_ratio",
    "sortino_ratio",
    "std_dev_ann_pct",
    "max_drawdown_pct",
    "aum_crore",
    "expense_ratio_pct"
]

for col in numeric_columns:
    scheme[col] = pd.to_numeric(scheme[col], errors="coerce")


print(scheme[numeric_columns].isnull().sum())


invalid_expense = scheme[
    (scheme["expense_ratio_pct"] < 0.1) |
    (scheme["expense_ratio_pct"] > 2.5)
]

print(invalid_expense)

anomalies = scheme[
    (scheme["return_1yr_pct"] > 100) |
    (scheme["return_1yr_pct"] < -100)
]

print(anomalies)

scheme.to_csv(
    "data/processed/scheme_performance.csv",
    index=False
)