import sqlite3

conn = sqlite3.connect("analytics.db")
cursor = conn.cursor()

rows = cursor.execute("""
SELECT id, page, referrer, device, duration, created_at
FROM visits
ORDER BY created_at DESC
""").fetchall()

for row in rows:
    print(row)

conn.close()
