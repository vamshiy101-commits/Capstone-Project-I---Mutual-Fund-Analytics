import sqlite3

conn = sqlite3.connect("bluestock_mf.db")
cursor = conn.cursor()

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

for table in tables:
    print(f"\n===== {table} =====")
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()

    for col in columns:
        print(col)

conn.close()