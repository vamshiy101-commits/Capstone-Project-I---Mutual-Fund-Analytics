import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("bluestock_mf.db")

cursor = conn.cursor()

# Read schema.sql
with open("sql/schema.sql", "r") as file:
    sql = file.read()

# Execute the SQL script
cursor.executescript(sql)

print("Schema created successfully!")

conn.commit()
conn.close()


