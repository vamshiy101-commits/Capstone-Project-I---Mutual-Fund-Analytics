import pandas as pd
import os

# Folder containing CSV files
folder_path = "data/raw"

# Get all CSV files
csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

print(f"Total CSV Files Found: {len(csv_files)}")

for file in csv_files:
    print("\n" + "=" * 70)
    print(f"Processing File: {file}")

    file_path = os.path.join(folder_path, file)

    try:
        df = pd.read_csv(file_path)

        print("\nShape:")
        print(df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())

        print("\nMissing Values:")
        print(df.isnull().sum())

    except Exception as e:
        print(f"Error reading {file}: {e}")