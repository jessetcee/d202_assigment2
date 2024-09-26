import datetime
import sqlite3
import random
import time
import os
import sqlite3
from flask import render_template, Flask, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'super_secret_key'

DATABASE = 'database.db'
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Path to the SQLite database file

# Create the database file and table if it doesn’t exist
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
    
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sensors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_name TEXT NOT NULL,
                location TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TemperatureReadings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id INTEGER,
                temperature REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sensor_id) REFERENCES Sensors(id)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                is_admin BOOLEAN NOT NULL DEFAULT 0
            )
        ''')

        conn.commit()
        conn.close()


# Function to add a new Sensors to the database
def add_sensor(sensor_name, location):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Sensors (sensor_name, location)
        VALUES (?, ?)
    ''', (sensor_name, location))
    conn.commit()
    conn.close()


# Function to get all sensors from the database
def get_all_sensors():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, sensor_name, location FROM Sensors')
    sensors = cursor.fetchall()
    conn.close()
    return sensors

# Function to insert a new Sensors into the database
def save_sensor_data(sensor_id, temperature):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO TemperatureReadings (sensor_id, temperature)
        VALUES (?, ?)
    ''', (sensor_id, temperature))
    conn.commit()
    conn.close()


def get_latest_readings():
    conn = sqlite3.connect(DATABASE)
    
    cursor = conn.cursor()
    # cursor.execute('''
    #     SELECT DISTINCT s.id, s.sensor_name, s.location, r.temperature, r.timestamp
    #     FROM TemperatureReadings r
    #     JOIN Sensors s ON r.sensor_id = s.id
    #     ORDER BY r.timestamp DESC
    # ''')

    cursor.execute('''
    SELECT
        tr.id,
        tr.sensor_id,
        s.sensor_name,
        s.location,
        tr.temperature,
        tr.timestamp
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY sensor_id
                ORDER BY timestamp DESC
            ) AS rn
        FROM TemperatureReadings
    ) tr
    JOIN Sensors s ON tr.sensor_id = s.id
    WHERE tr.rn = 1;
    ''')

    readings = cursor.fetchall()
    print(readings)
    conn.close()
    return readings

# Function to simulate and save temperature readings
def get_and_save_sensor_data():
    sensors = get_all_sensors()  # Get all sensors from the database
    for Sensors in sensors:
        sensor_id, sensor_name, location = Sensors
        temperature = round(random.uniform(20.0, 30.0), 2)
        save_sensor_data(sensor_id, temperature)  # Save the temperature reading for the Sensors
    # return sensors

# Initialize the database
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['is_admin'] = user['is_admin']  # Store the admin status in the session
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again."
    else:
        return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/dashboard/", methods=['GET'])
def dashboard():
    latest_readings = get_latest_readings()
    return render_template("dashboard.html", readings=latest_readings)

@app.route("/add_reading", methods=['POST'])
def add_reading():
    if request.is_json:
        try:
            data = request.get_json()

            for sensor in data:
                values = (sensor["id"], sensor["reading"], sensor["timestamp"], sensor["location"])

                conn = sqlite3.connect(DATABASE)
                conn.execute('INSERT INTO TemperatureReadings (sensor_id, temperature, timestamp, location) VALUES (?, ?, ?, ?)', values)
                conn.commit()
                conn.close()

            return jsonify({'message': 'Reading added successfully!'}), 201
        except Exception as e:
            print(f'Error: {e}')
            return jsonify({'error': str(e)}), 400
    else:
        print(f'Error: Request body must be JSON')
        return jsonify({'error': 'Request body must be JSON'}), 400

@app.route('/readings')
def readings():
    conn = sqlite3.connect(DATABASE)
    readings = conn.execute('''SELECT Tr.id, Tr.sensor_id, S.sensor_name, S.location, Tr.temperature, Tr.timestamp FROM TemperatureReadings Tr INNER JOIN Sensors S ON Tr.sensor_id = S.id''')
    return render_template('readings.html', readings=readings) 

@app.route('/delete_readings')
def delete_readings():
    conn = sqlite3.connect(DATABASE)
    conn.execute('DELETE FROM TemperatureReadings')
    conn.execute("UPDATE SQLITE_SEQUENCE SET SEQ = 0 WHERE NAME = 'TemperatureReadings'")
    conn.commit()
    conn.close()
    return redirect(url_for('readings'))

@app.route('/sensors')
def sensors():
    conn = sqlite3.connect(DATABASE)
    sensors = conn.execute("SELECT * FROM Sensors").fetchall()
    conn.commit()
    conn.close()

    return render_template('sensors.html', sensors=sensors)

@app.route('/add-Sensors', methods=['GET', 'POST'])
def add_sensor_route():
    if request.method == 'POST':
        sensor_name = request.form['sensor_name']
        location = request.form['location']
        add_sensor(sensor_name, location)  # Add Sensors to the database
        return redirect(url_for('readings'))  # Redirect back to the readings page
    
    return render_template('add_sensor.html')  # Render the form to add a new Sensors


if __name__ == "__main__":
    app.run(debug=True)


