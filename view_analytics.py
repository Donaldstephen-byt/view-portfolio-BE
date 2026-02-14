import sqlite3

conn = sqlite3.connect("analytics.db")
cursor = conn.cursor()

# First query
visits = cursor.execute("""
SELECT id, page, referrer, device, duration, created_at
FROM visits
ORDER BY created_at DESC
""").fetchall()

# Second query
contacts = cursor.execute("""
SELECT id, name, email, message, created_at
FROM contacts
""").fetchall()

conn.close()

print("Visits:")
for row in visits:
    print(row)

print("\nContacts:")
for row in contacts:
    print(row)