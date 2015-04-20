import gps
import json
import time
import requests
import picamera
import RPi.GPIO as GPIO

import os
import datetime

time.sleep(10)

ledPhotoViewed = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ledPhotoViewed, GPIO.OUT)
GPIO.output(ledPhotoViewed, True)

GPIO.setwarnings(False)


headers = {'Content-type': 'application/json', 'Accept':'text/plain'}
url_get_new_clicks = 'http://lia-wearable-nocontrol.meteor.com/getNewClicks'
#auth = 'ngo93Jqq7LtDgWMkEXztCwmC4sechnwXiu'
auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

def verifyNewClick():	
	r = requests.post(url_get_new_clicks, data = json.dumps({'auth': auth}), headers=headers)
	if (r.status_code == 200):
		GPIO.output(ledPhotoViewed, False)
		time.sleep(1)
		GPIO.output(ledPhotoViewed, True)

while True:
	verifyNewClick()	
	time.sleep(1)

