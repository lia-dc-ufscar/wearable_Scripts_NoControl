import json
import time
import requests
import picamera
import RPi.GPIO as GPIO
#import gps


#SETUP SYSTEM DATE
import datetime
import os

time.sleep(10)

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

#auth = 'ngo93Jqq7LtDgWMkEXztCwmC4sechnwXiu'
auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

PhotoCounter = 0
lat = 0
lng = 0


def savePhoto():
	global PhotoCounter
	url = 'http://lia.dc.ufscar.br/image_upload/fileupload.php'
	files = {'file': open('/home/pi/scripts/photos/image'+str(PhotoCounter)+'.jpg', 'rb')}
	f = requests.post(url, files=files)


def sendPhotoGPS():
	global PhotoCounter
	path = 'image'+str(PhotoCounter)+'.jpg'

#last lat position 
	configlat = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlatJson = json.load(configlat)
	lat = configlatJson['lat']
	configlat.close()

#last lon position
	configlng = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlngJson = json.load(configlng)
	lng = configlngJson['lon']
	configlng.close()

	data = {'auth': auth, 'lat': lat, 'lng': lng, 'display': 1, 'extra': {'type': 1, 'path': path}}
	r = requests.post(url_new_position, data = json.dumps(data), headers=headers)
#	if (r.status_code == 200):
#		GPIO.output(ledRequestSendPhoto, True)
#		time.sleep(2)
#		GPIO.output(ledRequestSendPhoto, False)


def takePhoto():
	global PhotoCounter
	with picamera.PiCamera() as camera:
		try:
			PhotoCounter = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
			path = '/home/pi/scripts/photos/image'+str(PhotoCounter)+'.jpg'
			camera.start_preview()
			time.sleep(3)
			camera.capture(path)
			camera.stop_preview()
			savePhoto()
			sendPhotoGPS()

		except:
			print("Could not take photo")
			


while True:
	r = requests.post(url_get_new_photo, headers=headers)
	if (r.content == "clicked"):
		GPIO.output(ledRequestSendPhoto, False)
		time.sleep(2)
		GPIO.output(ledRequestSendPhoto, True)
		takePhoto()
		#10s to verify again
#	time.sleep(5)

