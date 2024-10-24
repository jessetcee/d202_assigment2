import sqlite3

conn = sqlite3.connect("database.db")

# conn.execute('''
#         CREATE TABLE IF NOT EXISTS Sensors (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             sensor_name TEXT NOT NULL,
#             location TEXT NOT NULL
#         )
# ''')

# conn.execute('''
#         CREATE TABLE IF NOT EXISTS TemperatureReadings (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             sensor_id INTEGER,
#             temperature REAL NOT NULL,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (sensor_id) REFERENCES Sensors(id)
#         )
# ''')

# conn.execute('''
#         CREATE TABLE IF NOT EXISTS Users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT NOT NULL UNIQUE,
#             password TEXT NOT NULL,
#             is_admin BOOLEAN NOT NULL DEFAULT 0
#         )
# ''')
# conn.execute('''INSERT INTO Users (username, password, is_admin) VALUES (?, ?, ?)''', ("admin", "admin", 1))
# conn.execute('''INSERT INTO Users (username, password) VALUES (?, ?)''', ("user", "user"))
# conn.commit()
# conn.close()

data = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('SHOWING ALL TABLES AND COLUMNS')
for table in data.fetchall():
    table = table[0]
    columns = conn.execute(f"SELECT * FROM {table}").description

    print(table)
    for column in columns:
        print(f'col: {column[0]}')

# data = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
# print(f'SHOWING TABLES AND ALL DATA')
# for table in data.fetchall():
#     table = table[0]
#     table_data = conn.execute(f"SELECT * FROM {table}").fetchall()
#     for row in table_data:
#         print(row)

# print(conn.execute("SELECT * FROM TemperatureReadings").fetchall())