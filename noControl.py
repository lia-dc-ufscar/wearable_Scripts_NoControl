import json
import time
import requests
import picamera
import RPi.GPIO as GPIO

#SETUP SYSTEM DATE
import datetime
import os


ledGPS = 26
ledPhotoTaken = 13
ledRequestPhoto = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPhotoTaken, GPIO.OUT)
#GPIO.output(ledGPS, False)
GPIO.output(ledPhotoTaken, False)
#GPIO.output(ledRequestPhoto, False)

GPIO.setwarnings(False)


#headers = {'Content-type': 'application/json', 'Accept':'text/plain'}
#url_get_new_clicks = 'http://wearable-nocontrol.meteor.com/getNewClicks'
#url_new_position = 'http://wearable-nocontrol.meteor.com/addDatum'
#GPS always on
#display = 1
PhotoCounter = 0


#def verifyNewClick():	
#	r = requests.post(url_get_new_clicks, data = json.dumps({'auth': '436174696e7468654d61704c49414a43'}), headers=headers)
#	if (r.status_code == 200):
#		GPIO.output(ledRequestPhoto, True)
#		time.sleep(2)
#		GPIO.output(ledRequestPhoto, False)

def takePhoto():
	global PhotoCounter
	with picamera.PiCamera() as camera:
		try:
			path = '/home/pi/scripts/photos/photo'+str(PhotoCounter)+'.jpg'
			camera.start_preview()
			time.sleep(5)
			camera.capture(path)
			camera.stop_preview()
			PhotoCounter += 1
			GPIO.output(ledPhotoTaken, True)
			time.sleep(2)
			GPIO.output(ledPhotoTaken, False)
		#	time.sleep(120)
		# return actual time

		except:
			print("Could not take photo")
			

def uploadPhoto():
	

#def sendDataGPS():
	
#count = 0
while True:
#	verifyNewClick()	
	#count time =  120s
	#timePhoto= takePhoto()	  
	takePhoto()
	#actual time 
#	count += 1
#	sendDataGPS()

