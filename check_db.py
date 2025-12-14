import sqlite3

conn = sqlite3.connect("analytics.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM visits").fetchall()
for row in rows:
    print(row)

conn.close()
