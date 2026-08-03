import sqlite3

conn = sqlite3.connect("bluestock_mf.db")
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print("\n" + "=" * 60)
    print(f"Table: {table_name}")
    print("=" * 60)

    # Show columns
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    for col in columns:
        print(f"{col[1]} ({col[2]})")

conn.close()