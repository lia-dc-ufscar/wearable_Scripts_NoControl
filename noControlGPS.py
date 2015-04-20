import gps
import picamera
import time
import json
import requests
import subprocess
import RPi.GPIO as GPIO

import os
import datetime


time.sleep(10)

ledGPS = 19
ledWIFI = 26

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledGPS, GPIO.OUT)
GPIO.output(ledGPS, True)

GPIO.setup(ledWIFI, GPIO.OUT)
GPIO.output(ledWIFI, True)

GPIO.setwarnings(False)

session = None
connected = False


GetGPSSystemDate = False
if datetime.date.today().year < 1980:
	GetGPSSystemDate = True
	os.system("date --set '2015-02-13T12:33:43.000Z'")



#auth = 'ngo93Jqq7LtDgWMkEXztCwmC4sechnwXiu'
auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R' 


while not connected:
	try:
		session = gps.gps()
		session.stream(gps.WATCH_ENABLE)
		connected = True
	except Exception, e:
		print("Could not connected to the GPS module")
		subprocess.call(["/bin/gpsd", "/dev/ttyAMA0"])
		time.sleep(2)

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
	configlat = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlatJson = json.load(configlat)
	lat = configlatJson['lat']
	configlat.close()
	print("lat:", lat)
#last lon position in the last-gps.json file
	configlng = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlngJson = json.load(configlng)
	lng = configlngJson['lon']
	configlng.close()
	print("lng:", lng)
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	
	r = requests.post('http://lia-wearable-nocontrol.meteor.com/addDatum', data=json.dumps({'auth': auth, 'lat':lat, 'lng':lng, 'display':1, 'extra':{'type':0}}), headers=headers) 
	if (r.status_code == 200):
		GPIO.output(ledGPS, True)
		time.sleep(2)
		GPIO.output(ledGPS, False)
	#time.sleep(60)

while True:
	try:
		print("try")
		report = session.next()
		print("next:", report)
		if report['class'] == 'SKY':
			print("class")
			fix = getFix()
			print("bla:", fix)
		if not fix:
			if PushCount < PushRate:
				PushCount = PushRate
				print("fix:", fix)
		else:
			print("entrou else")
			if report['class'] == 'TPV':
				print("TPV")
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
		
	except StopIteration:
		session = gps.gps()
		session.stream(gps.WATCH_ENABLE)
		continue
