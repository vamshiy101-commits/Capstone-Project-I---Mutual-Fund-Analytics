import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///bluestock_mf.db")

# Read cleaned files
fund = pd.read_csv("data/raw/01_fund_master.csv")
nav = pd.read_csv("data/processed/02_nav_history.csv")
transactions = pd.read_csv("data/processed/08_investor_transactions.csv")
performance = pd.read_csv("data/processed/07_scheme_performance.csv")

# Create dim_date from NAV dates
date_df = pd.DataFrame()
date_df["full_date"] = pd.to_datetime(nav["date"]).drop_duplicates()
date_df["day"] = date_df["full_date"].dt.day
date_df["month"] = date_df["full_date"].dt.month
date_df["year"] = date_df["full_date"].dt.year
date_df["quarter"] = date_df["full_date"].dt.quarter

# Load tables
fund.to_sql("dim_fund", engine, if_exists="replace", index=False)
date_df.to_sql("dim_date", engine, if_exists="replace", index=False)
nav.to_sql("fact_nav", engine, if_exists="replace", index=False)
transactions.to_sql("fact_transactions", engine, if_exists="replace", index=False)
performance.to_sql("fact_performance", engine, if_exists="replace", index=False)

# AUM table (selected columns from performance)
aum = performance[[
    "amfi_code",
    "aum_crore",
    "expense_ratio_pct",
    "morningstar_rating"
]]

aum.to_sql("fact_aum", engine, if_exists="replace", index=False)

print("All tables loaded successfully!")

