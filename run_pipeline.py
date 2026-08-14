"""
Bluestock Mutual Fund Analytics
Master ETL Pipeline

Pipeline:
1. Data Ingestion
2. Data Cleaning
3. SQLite Database Loading

Run:
    python run_pipeline.py
"""

import subprocess
import sys
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent

# ETL scripts
SCRIPTS = [
    ("Data Ingestion", PROJECT_ROOT / "scripts" / "data_ingestion.py"),
    ("Data Cleaning", PROJECT_ROOT / "scripts" / "clean_data.py"),
    ("Database Loading", PROJECT_ROOT / "scripts" / "load_to_sqlite.py"),
]


def run_script(step_name, script_path):
    """
    Run an individual ETL script.

    Parameters
    ----------
    step_name : str
        Name of the ETL step.
    script_path : Path
        Path to the Python script.
    """

    print("\n" + "=" * 70)
    print(f"STARTING: {step_name}")
    print("=" * 70)

    if not script_path.exists():
        raise FileNotFoundError(
            f"Script not found: {script_path}"
        )

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{step_name} failed with exit code "
            f"{result.returncode}"
        )

    print(f"\n{step_name} completed successfully.")


def main():
    """Run the complete Mutual Fund ETL pipeline."""

    print("\n" + "#" * 70)
    print(" BLUESTOCK MUTUAL FUND ANALYTICS - ETL PIPELINE")
    print("#" * 70)

    try:
        for step_name, script_path in SCRIPTS:
            run_script(step_name, script_path)

        print("\n" + "#" * 70)
        print(" ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("#" * 70)

    except Exception as error:
        print("\n" + "!" * 70)
        print(" ETL PIPELINE FAILED")
        print("!" * 70)
        print(f"\nError: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()