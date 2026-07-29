# Data Quality Summary

## Project
Mutual Fund ETL Project - Day 1

## Datasets Loaded
- 01_fund_master.csv
- 02_nav_history.csv
- 03_aum_by_fund_house.csv
- 04_monthly_sip_inflows.csv
- 05_category_inflows.csv
- 06_industry_folio_count.csv
- 07_scheme_performance.csv
- 08_investor_transactions.csv
- 09_portfolio_holdings.csv
- 10_benchmark_indices.csv

## Checks Performed

- Successfully loaded all 10 datasets using Pandas.
- Verified dataset shapes.
- Verified data types.
- Displayed first 5 rows of each dataset.
- Checked missing values.
- Successfully fetched live NAV data from MFAPI.
- Downloaded NAV data for six mutual fund schemes.
- Explored Fund Master dataset.
- Identified unique Fund Houses, Categories, Sub Categories and Risk Categories.
- Validated AMFI codes.

## AMFI Validation

- Total AMFI Codes in Fund Master: 40
- Total AMFI Codes in NAV History: 40
- Missing AMFI Codes: 0

## Conclusion

All datasets passed the initial data quality checks and are ready for the ETL process.