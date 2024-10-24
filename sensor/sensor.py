import time
import json
import random
import requests
import requests.exceptions
import sqlite3
import os

from datetime import datetime

url = 'http://127.0.0.1:5000/api/meters'

def send_meter_data():
    while True:
        data = []
        sensors = request_meter_data()
        
        if sensors:
            for sensor in sensors:
                reading = random.randint(10, 35)
                
                if sensor[4] == "ACTIVE":
                    reading = random.randint(10, 35)

                data.append({
                    "id": sensor[0],
                    "location": sensor[2],
                    "description": sensor[3],
                    "reading": reading,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            json_data = json.dumps(data)

            try:
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, data=json_data, headers=headers)
                print(f"Data sent: {data}, Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f'Error: {e}')

            time.sleep(5)
        else:
            print(f'Endpoint is not available!')
            return

def request_meter_data():
    try:
        headers = {'Accept': "application/json"}
        response = requests.get(url, headers=headers)

        return response.json()
    except Exception as e:
        print(f'Error: {e}')

def add_col_to_table():
    conn = sqlite3.connect("../database.db")
    # conn.execute("ALTER TABLE Sensors ADD COLUMN area VARCHAR(255)")
    # conn.execute("ALTER TABLE Sensors ADD COLUMN description VARCHAR(255)")
    # conn.execute("ALTER TABLE Sensors ADD COLUMN status VARCHAR(8)")

    # conn.execute("ALTER TABLE TemperatureReadings ADD COLUMN location VARCHAR(255)")
    # conn.execute("ALTER TABLE TemperatureReadings DROP COLUMN area")

    # conn.execute("ALTER TABLE Sensors DROP COLUMN area")

    print(conn.execute("SELECT * FROM Sensors").fetchall())

def get_sql_data():
    conn = sqlite3.connect("../database.db")
    data = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")

    for table in data:
        table_name = table[0]
        table_info = conn.execute("SELECT * FROM " + table_name)
        print(table_name)
        # print(table_info.description)
        for column_header in table_info.description:
            print(f'col: {column_header[0]}|')

    # print(conn.execute("SELECT * FROM Sensors").fetchall())

def change_sensor_info():
    db_path = os.path.join(os.path.dirname(__file__), "../database.db")#absolute path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    sensors = cursor.execute("SELECT * FROM Sensors").fetchall()
    conn.commit()

    updated_locations = []  # List to store updated locations

    for Sensors in sensors:
        longitude = random.uniform(-180, 180)
        latitude = random.uniform(-90, 90)
        location = f'{longitude:.3f}, {latitude:.3f}'

        status = "ACTIVE"

        description = "N/A"

        query = f"UPDATE Sensors SET location = '{location}', status = '{status}', description = '{description}' WHERE id = + {str(Sensors[0])}"
        
        updated_locations.append(location)  # Store updated location

        cursor.execute(query)
        conn.commit()
    
    conn.close()

    return updated_locations  # Return list of updated locations

# change_sensor_info()
# add_col_to_table()
# get_sql_data()
# request_meter_data()
send_meter_data()