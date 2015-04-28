import gps
import picamera
import time
import json
import requests
import subprocess
import RPi.GPIO as GPIO
import shutil

import os
import datetime

shutil.copy('/home/pi/scripts/logs/nocontrol-gps.txt', '/home/pi/scripts/logs/last-nocontrol-gps.log')
shutil.copy('/home/pi/scripts/logs/nocontrol-gps-err.txt', '/home/pi/scripts/logs/last-nocontrol-gps-err.log')


import sys
sys.stdout = open('/home/pi/scripts/logs/nocontrol-gps.txt','w', 0)
sys.stderr = open('/home/pi/scripts/logs/nocontrol-gps-err.txt','w', 0)

time.sleep(4)

ledGPS = 19
ledWIFI = 26

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledGPS, GPIO.OUT)
#GPIO.output(ledGPS, True)

GPIO.setup(ledWIFI, GPIO.OUT)
GPIO.output(ledWIFI, True)

GPIO.setwarnings(False)

session = None
connected = False


GetGPSSystemDate = False
if datetime.date.today().year < 1980:
	GetGPSSystemDate = True
	os.system("date --set '2015-02-13T12:33:43.000Z'")



auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R' 


while not connected:
	try:
		session = gps.gps()
		session.stream(gps.WATCH_ENABLE)
		connected = True
	except Exception, e:
		print("Could not connected to the GPS module:", e)
		subprocess.call(["/bin/gpsd", "/dev/ttyAMA0"])
		time.sleep(2)

print("Connected to GPS daemon")

PushRate = 30
PushCount = 0
fix = False

def getFix():
	global report
	for satellite in report['satellites']:
		if (satellite['used'] == True):
			return True
	return False


def sendGPS():
#last lat position in the last-gps.json file
	configFile = open('/home/pi/scripts/var/last-gps.json', 'r')
	configInfo = json.load(configFile)

	lat = configInfo['lat']
	lng = configInfo['lon']

	configFile.close()
	print("lat:", lat)
	print("lng:", lng)

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	
	r = requests.post('http://lia-wearable-nocontrol.meteor.com/addDatum', data=json.dumps({'auth': auth, 'lat':lat, 'lng':lng, 'display':1, 'extra':{'type':0}}), headers=headers) 
	if (r.status_code == 200):
		print("Gps Sent Data")
		GPIO.output(ledGPS, True)
		time.sleep(2)
		GPIO.output(ledGPS, False)

while True:
	try:
		report = session.next()
		if report['class'] == 'SKY':
			fix = getFix()
		if not fix:
			if PushCount < PushRate:
				PushCount = PushRate
				print("No Fix")
		else:
			print("Fix")
			if report['class'] == 'TPV':
				if 'time' in report:
					if (GetGPSSystemDate):
						GetGPSSystemDate = False
						os.system("date --set '%s'"%report.time)
					lastpos = open('/home/pi/scripts/var/last-gps.json', 'w')
					jsonpos = json.dumps(dict(report))
					print >> lastpos, jsonpos
					print("ok")
					lastpos.close()
					if (PushCount >= PushRate):
						#GpsLog.flush()
						PushCount = 0
						sendGPS()
				PushCount += 1
	
	except KeyError:
		print("KeyError")
		pass	
	except StopIteration:
		print("Reached StopIteration")
		session = gps.gps()
		session.stream(gps.WATCH_ENABLE)
		continue
