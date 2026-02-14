import sqlite3

conn = sqlite3.connect("analytics.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    email TEXT,
    message TEXT,
    page TEXT NOT NULL,
    referrer TEXT,
    device TEXT,
    duration INTEGER CHECK(duration >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


# Create indexes separately
cursor.execute("CREATE INDEX IF NOT EXISTS idx_visits_user_id ON visits(user_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_visits_email ON visits(email)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_visits_page ON visits(page)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_visits_created_at ON visits(created_at)")

conn.commit()
conn.close()

print("Database ready")