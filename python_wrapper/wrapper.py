#!/usr/bin/python

import serial
import time
ser = serial.Serial('/dev/ttyACM0')

#Connect to MySQL and use the database name RaspPi
import mysql.connector
db = mysql.connector.connect(user='root', password='raspberry', host='localhost', database='RaspPi')

cursor = db.cursor()


#print temperatureH, temperatureL, humidityH, humidityL, pressureH, pressureL, sound, water, smoke
#print "test a"
while True:
	# Get Values from Threshold Table for current Thresholds
	cursor.execute("SELECT upperTempValue FROM Threshold")
	temperatureH=cursor.fetchone()
	cursor.execute("SELECT lowerTempValue FROM Threshold")
	temperatureL=cursor.fetchone()
	cursor.execute("SELECT upperHumidityValue FROM Threshold")
	humidityH=cursor.fetchone()
	cursor.execute("SELECT lowerhumidityValue FROM Threshold")
	humidityL=cursor.fetchone()
	cursor.execute("SELECT upperBiometricValue FROM Threshold")
	pressureH=cursor.fetchone()
	cursor.execute("SELECT lowerBiometricValue FROM Threshold")
	pressureL=cursor.fetchone()
	cursor.execute("SELECT soundValue FROM Threshold")
	sound=cursor.fetchone()
	cursor.execute("SELECT waterValue FROM Threshold")
	water=cursor.fetchone()
	cursor.execute("SELECT waterValue FROM Threshold")
	smoke=cursor.fetchone()

	# Start Listen for new lines from Arduino to start processing data
	sensor = (ser.readline()).strip('\n')             # Get Sensor Name
	value = (ser.readline()).strip('\n')       # Get Sensor Value
	ts = time.strftime('%Y-%m-%d %H:%M:%S')               # Get Time
	#print sensor
	#print value
	#print ts
	if sensor.find('Temperature') == 0:    #Temperature
		#print "test t"                             # Puts values into Temperature table
		insert = ("INSERT INTO Temperature (tempValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '1')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > temperatureH[0]:                                                   # Temperature hight breached
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '1', '1', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
		elif float(value) < temperatureL[0]:                                                  # Temperature low breached
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '1', '2', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
	elif sensor.find('Pressure') == 0:    # Pressure
		#print "test p"
		insert = ("INSERT INTO Biometric (biometricValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '6')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > pressureH[0]:                                                    # Pressure hight breached       !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '6', '3', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
		elif float(value) < pressureL[0]:                                                   # Pressure low breached         !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '6', '4', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
	elif sensor.find('Humidity') == 0:    # Humidity
		#print "test h"
		insert = ("INSERT INTO Humidity (humidityValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '2')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > humidityH[0]:                                                    # Pressure hight breached       !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '2', '5', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
		elif float(value) < humidityL[0]:                                                   # Pressure low breached!!!NEEDS TO BE CHANGED!!!!!!!!!!!!NOT NEEDED?
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '2', '6', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
	elif sensor.find('Sound') == 0:    # Sound
		# print "test s"
		insert = ("INSERT INTO Sound (soundValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '5')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > sound[0]:                                                    # Sound hight breached          !!!!!!!!NEEDS TO BE CHANGED!!!!!!
                        # print "test s2"
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '5', '7', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
	elif sensor.find('Water') == 0:    # Water
		#print "test w"
		insert = ("INSERT INTO WaterFlod (waterFlodValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '3')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) == water[0]:                                                     # Water hight breached          !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '3', '8', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()
	elif sensor.find('Smoke') == 0:    # Smoke
		#print "test sm"
		insert = ("INSERT INTO Smoke (smokeValue, day, sensorID) VALUES (%s, %s, %s);")
		data = (value,ts, '4')
		cursor.execute(insert, data)                                        # Pushes query
		db.commit()
		if float(value) > smoke[0]:                                                     # Water hight breached           !!!!!!!!NEEDS TO BE CHANGED!!!!!!
			insert = ("INSERT INTO Alarms (valueID, sensorID, errorID, date) VALUES (%s, %s, %s, %s);")
			data = (value, '4', '9', ts)
			cursor.execute(insert, data)                                    # Pushes query
			db.commit()

	db.commit()
cursor.close()
db.close()                                                                 # Close connection
