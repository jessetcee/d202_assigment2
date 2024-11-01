# d202_assignment2
This is a python flask application that simulated IOT temperature sensors with live updating, storing of data, retrival and functinality to manipulate the sensor data. 

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation
1. Clone the repository:`https://github.com/jessetcee/d202_assignment2.git`
2. Install dependencies: `.\.venv\Scripts\activate.ps1`
                         `python -m pip install flask` -In root directory
                         `pip install requests` -In sensor directory
                         
## Usage
1. flask run -In main directory 
## This runs the flask app.py which is hosting a web server on http://localhost:5000
2. python sensor.py -In sensor directory
## this runs the sensor.py application which holds all the sensor simulation configuration and database functionality for retrieving and posting sensor data to web server

## Application should now be running. 


## Features
- User authentication -Login/Logout
- Sensor temperature readings update
- Dashboard displays instance of all sensors and updates live
- Sensor data contains (Sensorname, location, lat/lot, timestamp, temperature)
- Delete tempreading records from web page
- Admin centre is only accessible by admin user
- Admin center allows admin user to add new sensor by just inputing a sensorname
- Add sensor functionality dynamically assigns sensor details to new sensor and stores in database
- admin user can search and filter sensors by ID or Username and by highest temperatures
- Database to store all sensor data and retrive data
- Dashboard sensor displays utilize colors to displays a graphical representation of temperature at varying locations 


















test
test 2


