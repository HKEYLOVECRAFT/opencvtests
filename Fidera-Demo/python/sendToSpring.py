import requests
import time
import datetime
import random

while(True):
	difference = str(random.randint(0, 100))
	timestamp = datetime.datetime.now().strftime("%A %d %m %Y %H:%M:%S")
	params = {"difference": difference, "time": timestamp}
	r = requests.post("http://localhost:8080/data", data=params)
	print(r)
	time.sleep(5)
