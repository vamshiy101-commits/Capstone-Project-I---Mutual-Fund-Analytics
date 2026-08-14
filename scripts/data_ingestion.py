"""
Data ingestion module for the Bluestock Mutual Fund Analytics project.

This module reads and validates CSV files from the raw data directory.
"""

from pathlib import Path

import pandas as pd


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Raw data directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def get_csv_files():
    """
    Get all CSV files from the raw data directory.

    Returns
    -------
    list[Path]
        List of CSV file paths.
    """

    return sorted(RAW_DATA_DIR.glob("*.csv"))


def validate_csv_file(file_path):
    """
    Read and validate a CSV file.

    Parameters
    ----------
    file_path : Path
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the dataset is empty.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    try:
        df = pd.read_csv(file_path)

    except Exception as error:
        raise RuntimeError(
            f"Unable to read {file_path.name}: {error}"
        ) from error

    if df.empty:
        raise ValueError(
            f"{file_path.name} is empty."
        )

    return df


def ingest_data():
    """
    Load and validate all raw CSV files.

    Returns
    -------
    dict[str, pandas.DataFrame]
        Dictionary containing loaded datasets.
    """

    csv_files = get_csv_files()

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DATA_DIR}"
        )

    datasets = {}

    for file_path in csv_files:
        datasets[file_path.stem] = validate_csv_file(
            file_path
        )

    return datasets


def main():
    """
    Execute the data ingestion process.
    """

    datasets = ingest_data()

    print(
        f"Data ingestion completed successfully. "
        f"{len(datasets)} CSV files loaded."
    )


if __name__ == "__main__":
    main()