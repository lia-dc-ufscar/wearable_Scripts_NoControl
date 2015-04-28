import gps
import json
import time
import requests
import picamera
import RPi.GPIO as GPIO
import shutil

import os
import datetime

shutil.copy('/home/pi/scripts/logs/nocontrol-requests.txt', '/home/pi/scripts/logs/last-nocontrol-requests.log')
shutil.copy('/home/pi/scripts/logs/nocontrol-requests-err.txt', '/home/pi/scripts/logs/last-nocontrol-requests-err.log')

import sys
sys.stdout = open('/home/pi/scripts/logs/nocontrol-requests.txt','w', 0)
sys.stderr = open('/home/pi/scripts/logs/nocontrol-requests-err.txt','w', 0)

time.sleep(6)

ledPhotoViewed = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ledPhotoViewed, GPIO.OUT)
GPIO.output(ledPhotoViewed, True)

GPIO.setwarnings(False)


headers = {'Content-type': 'application/json', 'Accept':'text/plain'}
url_get_new_clicks = 'http://lia-wearable-nocontrol.meteor.com/getNewClicks'
auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

def verifyNewClick():	
	r = requests.post(url_get_new_clicks, data = json.dumps({'auth': auth}), headers=headers)
	if (r.status_code == 200):
		print("Photo Viewed")
		GPIO.output(ledPhotoViewed, False)
		time.sleep(1)
		GPIO.output(ledPhotoViewed, True)

while True:
	verifyNewClick()	
	time.sleep(1)

