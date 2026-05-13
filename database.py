import sqlite3

# Connect to database
conn = sqlite3.connect("aitutor.db")

# Create cursor
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Save changes
conn.commit()

# Close connection
conn.close()

print("✅ Database and users table created successfully!")