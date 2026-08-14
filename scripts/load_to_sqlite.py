"""
Database loading module for the Bluestock Mutual Fund Analytics project.

This module loads processed mutual fund datasets into a SQLite database.

Database tables:
- dim_fund
- dim_date
- fact_nav
- fact_transactions
- fact_performance
- fact_aum
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data directories
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

# SQLite database
DATABASE_PATH = PROJECT_ROOT / "bluestock_mf.db"


def create_database_engine():
    """
    Create and return the SQLite database engine.

    Returns
    -------
    sqlalchemy.Engine
        SQLite database engine.
    """

    return create_engine(
        f"sqlite:///{DATABASE_PATH}"
    )


def load_fund_data(engine):
    """
    Load mutual fund master data into dim_fund.

    Parameters
    ----------
    engine : sqlalchemy.Engine
        SQLite database engine.

    Returns
    -------
    int
        Number of records loaded.
    """

    file_path = RAW_DATA_DIR / "01_fund_master.csv"

    fund = pd.read_csv(file_path)

    fund.to_sql(
        "dim_fund",
        engine,
        if_exists="replace",
        index=False
    )

    return len(fund)


def load_nav_data(engine):
    """
    Load NAV history and create the date dimension.

    Parameters
    ----------
    engine : sqlalchemy.Engine
        SQLite database engine.

    Returns
    -------
    tuple
        Number of NAV records and date records loaded.
    """

    file_path = (
        PROCESSED_DATA_DIR /
        "02_nav_history.csv"
    )

    nav = pd.read_csv(file_path)

    nav["date"] = pd.to_datetime(
        nav["date"],
        errors="coerce"
    )

    date_df = pd.DataFrame()

    date_df["full_date"] = (
        nav["date"]
        .dropna()
        .drop_duplicates()
        .sort_values()
    )

    date_df["day"] = date_df["full_date"].dt.day
    date_df["month"] = date_df["full_date"].dt.month
    date_df["year"] = date_df["full_date"].dt.year
    date_df["quarter"] = date_df["full_date"].dt.quarter

    date_df.to_sql(
        "dim_date",
        engine,
        if_exists="replace",
        index=False
    )

    nav.to_sql(
        "fact_nav",
        engine,
        if_exists="replace",
        index=False
    )

    return len(nav), len(date_df)


def load_transaction_data(engine):
    """
    Load investor transaction data into fact_transactions.

    Parameters
    ----------
    engine : sqlalchemy.Engine
        SQLite database engine.

    Returns
    -------
    int
        Number of transaction records loaded.
    """

    file_path = (
        PROCESSED_DATA_DIR /
        "08_investor_transactions.csv"
    )

    transactions = pd.read_csv(file_path)

    transactions.to_sql(
        "fact_transactions",
        engine,
        if_exists="replace",
        index=False
    )

    return len(transactions)


def load_performance_data(engine):
    """
    Load scheme performance and AUM data.

    Parameters
    ----------
    engine : sqlalchemy.Engine
        SQLite database engine.

    Returns
    -------
    tuple
        Number of performance and AUM records loaded.
    """

    file_path = (
        PROCESSED_DATA_DIR /
        "07_scheme_performance.csv"
    )

    performance = pd.read_csv(file_path)

    performance.to_sql(
        "fact_performance",
        engine,
        if_exists="replace",
        index=False
    )

    aum_columns = [
        "amfi_code",
        "aum_crore",
        "expense_ratio_pct",
        "morningstar_rating"
    ]

    aum = performance[aum_columns].copy()

    aum.to_sql(
        "fact_aum",
        engine,
        if_exists="replace",
        index=False
    )

    return len(performance), len(aum)


def load_all_tables():
    """
    Load all project datasets into the SQLite database.

    Returns
    -------
    dict
        Dictionary containing table names and record counts.
    """

    engine = create_database_engine()

    fund_count = load_fund_data(engine)

    nav_count, date_count = load_nav_data(engine)

    transaction_count = load_transaction_data(
        engine
    )

    performance_count, aum_count = (
        load_performance_data(engine)
    )

    return {
        "dim_fund": fund_count,
        "dim_date": date_count,
        "fact_nav": nav_count,
        "fact_transactions": transaction_count,
        "fact_performance": performance_count,
        "fact_aum": aum_count,
    }


def main():
    """
    Execute the complete database loading process.
    """

    table_counts = load_all_tables()

    print("Database loading completed successfully.")

    for table, count in table_counts.items():
        print(f"{table}: {count:,} records")


if __name__ == "__main__":
    main()