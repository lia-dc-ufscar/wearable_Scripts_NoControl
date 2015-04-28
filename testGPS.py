#send GPS data from file
#import gps
import picamera
import time
import json
import requests
import subprocess
import RPi.GPIO as GPIO

import os
import datetime


ledGPS = 19

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledGPS, GPIO.OUT)
GPIO.output(ledGPS, False)

GPIO.setwarnings(False)


#GetGPSSystemDate = False
#if datetime.date.today().year < 1980:
#	GetGPSSystemDate = True
#		os.system("date --set '2015-02-13T12:33:43.000Z'")

#PushRate = 300
#PushCount = 0


headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
auth = 'ngo93Jqq7LtDgWMkEXztCwmC4sechnwXiu'

#session = None
#connected = False

#while not connected:
#	try:
#		session = gps.gps()
#		session.stream(gps.WATCH_ENABLE)
#		connected = True
#	except Exception, e:
#		print("Could not connected to the GPS module", e)
#		subprocess.call(["/bin/gpsd", "/dev/ttyAMA0"])
#	
#		time.sleep(2)

#fix = False

#def getFix():
#	global report
#	for satellite in report['satellites']:
#		if (satellite['used'] == True):
#			return True
#	return False
lat = 0
lng = 0

#def sendGPS():
#trocar lat e lng , fazer pegar do arquivo ao inves de passar uma fixa
configlat = open('/home/pi/scripts/var/last-gps.json', 'r')
configlatJson = json.load(configlat)
lat = configlatJson['lat']
configlat.close()

configlng = open('/home/pi/scripts/var/last-gps.json', 'r')
configlngJson = json.load(configlng)
lng = configlngJson['lon']
configlng.close()	
 
print ("lat = ", lat)
print ("lng = ", lng)
	
#	r = request.post('http://lia-wearable-nocontrol.meteor.com/addDatum', data=json.dumps({'auth': auth, 'lat': 49.2657, 'lng': -123.247394, 'display': 1, 'extra': {'type': 0}}), headers=headers) 
#r = requests.post('http://lia-wearable-nocontrol.meteor.com/addDatum', data=json.dumps({'auth': auth, 'lat': lat, 'lng': lng, 'display': 1, 'extra': {'type': 0}}), headers=headers) 
#if (r.status_code == 200):
#	GPIO.output(ledGPS, True)
#	time.sleep(2)
#	GPIO.output(ledGPS, False)
#time.sleep(60)

#while True:
#	try:
#		report = session.next()
#		if report['class'] == 'SKY':
#			fix = getFix()
#		if not fix:
#			if PushCount < PushRate:
#				PushCount = PushRate
#		else:
#			if report ['class'] == 'TPV':
#				if 'time' in report:
#					if (GetGPSSystemDate):
#						GetGPSSystemDate = False
#						os.system("date --set '%s'"%report.time)
#					lastpos = open('/home/pi/scripts/var/last-gps.json', 'w')
#					jsonpos = json.dumps(dict(report))
#					print >> lastpos, jsonpos
#					lastpos.close()
#					if PushCount >= PushRate:
#						GpsLog.flush()
#						PushCount = 0
#						sendGPS()
		
#	except StopIteration:
#		session = gpg.gps()
#		session.stream(gps.WATCH_ENABLE)
#		continue
