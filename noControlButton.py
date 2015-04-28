import json
import time
import requests
import picamera
import RPi.GPIO as GPIO
import shutil
#import gps


#SETUP SYSTEM DATE
import datetime
import os

shutil.copy('/home/pi/scripts/logs/nocontrol-button.txt', '/home/pi/scripts/logs/last-nocontrol-button.log')
shutil.copy('/home/pi/scripts/logs/nocontrol-button-err.txt', '/home/pi/scripts/logs/last-nocontrol-button-err.log')

import sys
sys.stdout = open('/home/pi/scripts/logs/nocontrol-button.txt','w', 0);
sys.stderr = open('/home/pi/scripts/logs/nocontrol-button-err.txt','w', 0);

print("Starting Script noControlButton")

time.sleep(7)

ledRequestSendPhoto = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ledRequestSendPhoto, GPIO.OUT)
GPIO.output(ledRequestSendPhoto, True)

GPIO.setwarnings(False)


headers = {'Content-type': 'application/json', 'Accept':'text/plain'}
url_get_new_photo = 'http://lia-wearable-nocontrol.meteor.com/getLastClick'
url_new_position = 'http://lia-wearable-nocontrol.meteor.com/addDatum'
url_clean_clicks = 'http://lia-wearable-nocontrol.meteor.com/cleanClicks'

auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

PhotoCounter = 0
countSave = 0
countSend = 0
countTake = 0

def savePhoto():
	global PhotoCounter
	global countSave

	url = 'http://lia.dc.ufscar.br/image_upload/fileupload.php'
	files = {'file': open('/home/pi/scripts/photos/image'+str(PhotoCounter)+'.jpg', 'rb')}
	f = requests.post(url, files=files)
	countSave = countSave + 1
	print("savePhoto:", countSave)

def sendPhotoGPS():
	global countSend
	global PhotoCounter
	path = 'image'+str(PhotoCounter)+'.jpg'

#last lat position 
	configFile = open('/home/pi/scripts/var/last-gps.json', 'r')
	configInfo = json.load(configFile)

	lat = configInfo['lat']
	lng = configInfo['lon']

	configFile.close()


	data = {'auth': auth, 'lat': lat, 'lng': lng, 'display': 1, 'extra': {'type': 1, 'path': path}}
	r = requests.post(url_new_position, data = json.dumps(data), headers=headers)
	if (r.status_code == 200):
		countSend = countSend + 1
		print("SendPhoto:", countSend)
#		GPIO.output(ledRequestSendPhoto, True)
#		time.sleep(2)
#		GPIO.output(ledRequestSendPhoto, False)


def takePhoto():
	global PhotoCounter
	global countTake

	statusCamera = open('/home/pi/scripts/var/status-camera.json', 'w')
	jsonCamera = json.dumps({"status": 1})
	statusCamera.write(jsonCamera)
	statusCamera.close()

	with picamera.PiCamera() as camera:
		try:
			PhotoCounter = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
			path = '/home/pi/scripts/photos/image'+str(PhotoCounter)+'.jpg'
			
			print("Begin Camera")
			camera.start_preview()
			time.sleep(3)
			camera.capture(path)
			camera.stop_preview()
			



		except:
			print("Could not take photo")
			
	countTake = countTake + 1	
	print("TakePhoto:", countTake)

	statusCamera = open('/home/pi/scripts/var/status-camera.json', 'w')
	jsonCamera = json.dumps({"status": 0})
	statusCamera.write(jsonCamera)
	statusCamera.close()


while True:
	r = requests.post(url_get_new_photo, headers=headers)
	if (r.content == "clicked"):
		print("Botton pressed")
		GPIO.output(ledRequestSendPhoto, False)
		time.sleep(2)
		GPIO.output(ledRequestSendPhoto, True)

		statusCamera = open('/home/pi/scripts/var/status-camera.json', 'r')
		cameraJson = json.load(statusCamera)
		status_camera = cameraJson['status']
		statusCamera.close()

		if status_camera == 0:
			takePhoto()
			savePhoto()
			sendPhotoGPS()

		
