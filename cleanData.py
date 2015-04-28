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

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

r = requests.post('http://lia-wearable-nocontrol.meteor.com/cleanData', data = json.dumps({'auth': auth}), headers=headers)
if r.status_code == 200:
	print("ok")
	
