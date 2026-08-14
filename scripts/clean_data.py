"""
Data cleaning module for the Bluestock Mutual Fund Analytics project.

This module cleans and validates:
1. NAV history
2. Investor transactions
3. Scheme performance

Cleaned datasets are saved in the data/processed directory.
"""

from pathlib import Path

import pandas as pd


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def clean_nav_history():
    """
    Clean and validate NAV history data.

    Returns
    -------
    pandas.DataFrame
        Cleaned NAV history dataset.
    """

    input_file = RAW_DATA_DIR / "02_nav_history.csv"
    output_file = PROCESSED_DATA_DIR / "02_nav_history.csv"

    nav = pd.read_csv(input_file)

    nav["date"] = pd.to_datetime(
        nav["date"],
        errors="coerce"
    )

    nav = nav.sort_values(
        ["amfi_code", "date"]
    )

    # Forward-fill missing NAV values within each fund
    nav["nav"] = (
        nav.groupby("amfi_code")["nav"]
        .ffill()
    )

    # Remove invalid NAV values
    nav = nav[nav["nav"] > 0]

    # Remove duplicate records
    nav = nav.drop_duplicates()

    nav.to_csv(
        output_file,
        index=False
    )

    return nav


def clean_transactions():
    """
    Clean and validate investor transaction data.

    Returns
    -------
    pandas.DataFrame
        Cleaned investor transaction dataset.
    """

    input_file = (
        RAW_DATA_DIR /
        "08_investor_transactions.csv"
    )

    output_file = (
        PROCESSED_DATA_DIR /
        "08_investor_transactions.csv"
    )

    transaction = pd.read_csv(input_file)

    # Convert transaction date
    transaction["transaction_date"] = pd.to_datetime(
        transaction["transaction_date"],
        errors="coerce"
    )

    # Standardize transaction types
    transaction["transaction_type"] = (
        transaction["transaction_type"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({
            "sip": "SIP",
            "systematic_investment_plan": "SIP",
            "lumpsum": "Lumpsum",
            "lump sum": "Lumpsum",
            "redeem": "Redemption",
        })
    )

    # Validate transaction amounts
    transaction = transaction[
        transaction["amount_inr"] > 0
    ]

    # Standardize KYC status
    transaction["kyc_status"] = (
        transaction["kyc_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    valid_kyc = [
        "verified",
        "pending",
        "rejected"
    ]

    # Keep only valid KYC statuses
    transaction = transaction[
        transaction["kyc_status"].isin(valid_kyc)
    ]

    # Remove duplicate records
    transaction = transaction.drop_duplicates()

    transaction.to_csv(
        output_file,
        index=False
    )

    return transaction


def clean_scheme_performance():
    """
    Clean and validate mutual fund scheme performance data.

    Returns
    -------
    pandas.DataFrame
        Cleaned scheme performance dataset.
    """

    input_file = (
        RAW_DATA_DIR /
        "07_scheme_performance.csv"
    )

    output_file = (
        PROCESSED_DATA_DIR /
        "07_scheme_performance.csv"
    )

    scheme = pd.read_csv(input_file)

    # Remove duplicate records
    scheme = scheme.drop_duplicates()

    # Numeric columns
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
        "expense_ratio_pct",
        "morningstar_rating",
    ]

    # Convert numeric columns
    for column in numeric_columns:
        scheme[column] = pd.to_numeric(
            scheme[column],
            errors="coerce"
        )

    # Remove invalid expense ratios
    scheme = scheme[
        (scheme["expense_ratio_pct"] >= 0.1)
        & (scheme["expense_ratio_pct"] <= 2.5)
    ]

    # Remove extreme 1-year return anomalies
    scheme = scheme[
        (scheme["return_1yr_pct"] >= -100)
        & (scheme["return_1yr_pct"] <= 100)
    ]

    scheme.to_csv(
        output_file,
        index=False
    )

    return scheme


def main():
    """
    Execute all data cleaning operations.
    """

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    nav = clean_nav_history()
    transactions = clean_transactions()
    performance = clean_scheme_performance()

    print("Data Cleaning completed successfully.")
    print(f"NAV records: {len(nav):,}")
    print(f"Transaction records: {len(transactions):,}")
    print(f"Performance records: {len(performance):,}")


if __name__ == "__main__":
    main()