import sqlite3

#connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()
# Create a table for job listings
cursor.execute("""CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                required_skills TEXT NOT NULL,
                optional_skills TEXT
            )""")

# Commit the changes and close the connection
conn.commit()   
conn.close()

print("Database and table created successfully.")
print(sqlite3.sqlite_version)