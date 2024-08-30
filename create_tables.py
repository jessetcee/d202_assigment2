import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

# Create SENSOR table
conn.execute('''
    CREATE TABLE IF NOT EXISTS sensors (
        sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        interval INT NOT NULL
    )
''')
print("Created sensors table successfully!")

# Create TEMPERATURE_READING table
conn.execute('''
    CREATE TABLE IF NOT EXISTS temp_readings (
        reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER NOT NULL,
        temperature FLOAT NOT NULL,
        timestamp DATETIME NOT NULL,
        FOREIGN KEY (sensor_id) REFERENCES sensors (sensor_id)
    )
''')
print("Created temp_readings table successfully!")

# Create USER table
conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0
    )
''')
print("Created users table successfully!")

conn.close()