#!/usr/bin/python

import serial
import time
ser = serial.Serial('/dev/ttyACM0')

#Connect to MySQL and use the database name RaspPi
import mysql.connector
db = mysql.connector.connect(user='root', password='admin', host='localhost', database='RaspPi')
t = 'Temperature'
p = 'Pressure'
h = 'Humidity'
s = 'Sound'
w = 'Water'
sm = 'Smoke'

cursor = db.cursor()
print "test a"
while True:
	sensor = (ser.readline()).strip('\n')             # Get Sensor Name
	value = (ser.readline()).strip('\n')       # Get Sensor Value
	ts = time.strftime('%Y-%m-%d %H:%M:%S')               # Get Time
	print sensor
	print value
	print ts
	if sensor.find('Temperature') == 0:    #Temperature
		print "test t"                             # Puts values into Temperature table
		insert = ("INSERT INTO Temperature (tempValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '1')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > 115.0:                                                   # Temperature hight breached
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '1', '1', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
		elif float(value) < 32.0:                                                  # Temperature low breached
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '1', '2', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
	elif sensor.find('Pressure') == 0:    # Pressure
		print "test p"
		insert = ("INSERT INTO Biometric (biometricValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '6')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > 40.0:                                                    # Pressure hight breached       !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '6', '3', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
		elif float(value) < 5.0:                                                   # Pressure low breached         !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '6', '4', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
	elif sensor.find('Humidity') == 0:    # Humidity
		print "test h"
		insert = ("INSERT INTO Humidity (humidityValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '2')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > 10.0:                                                    # Pressure hight breached       !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '2', '5', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
		elif float(value) < 7.0:                                                   # Pressure low breached!!!NEEDS TO BE CHANGED!!!!!!!!!!!!NOT NEEDED?
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '2', '6', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
	elif sensor.find('Sound') == 0:    # Sound
		print "test s"
		insert = ("INSERT INTO Sound (soundValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '5')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > 11.0:                                                    # Sound hight breached          !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '5', '7', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
	elif sensor.find('Water') == 0:    # Water
		print "test w"
		insert = ("INSERT INTO WaterFlod (waterFlodValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '3')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > 2.0:                                                     # Water hight breached          !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '3', '8', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
	elif sensor.find('Smoke') == 0:    # Smoke
		print "test sm"
		insert = ("INSERT INTO Smoke (smokeValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '4')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > 5.0:                                                     # Water hight breached           !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '4', '9', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()

	db.commit()
cursor.close()
db.close()                                                                 # Close connection
