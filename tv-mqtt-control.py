#!/usr/bin/env python3

import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import datetime
import time
import json
import sys
import os

log = open("mqtt-client.log","a")

# redirect print to logfile...
# comment this line below to print to std instead of logfile
sys.stdout = log

from datetime import datetime
from threading import Thread

auth = {
  'username':"user",
  'password':"password"
}

topics = {
	"home/tv"               : { "topic" : "home/tv"             , "function" : "stateTV"       },
	"home/tv/state"         : { "topic" : "home/tv/state"       , "status"   : "OFF"           }
}

# key = topics item, switch = do turn on or off device
def stateTV(key, switch):
	import subprocess
	# get state of device (using ping or wget...)
	# script returns ON or OFF
	proc = subprocess.Popen(["sudo", "sh",  "/home/pi/tv_control/tv_status.sh", "> /dev/null 2>&1"], stdout=subprocess.PIPE)
	out, err = proc.communicate()
	out.decode('ascii')

	if "OFF" in str(out):
		client.publish(key + "/state", "OFF")
		topics[key + "/state"]["status"] = "OFF"
	else:
		client.publish(key + "/state", "ON")
		topics[key + "/state"]["status"] = "ON"

	return topics[key+"/state"]["status"]

def on_subscribe(client, userdata, mid, granted_qos):
	print (datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " - " + "Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
	import subprocess
	print (datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " - " + "Received message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	print (
		datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " -",
		"State changed:",
		msg.topic,
		eval(topics[msg.topic].get("function") + "('"+msg.topic+"', " + ("1" if "OFF" in str(msg.payload) else "0") + ")")
	)

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print (datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " - " + "Connected to broker")

		# loop thru topics dictionary and subscribe to topics...
		for key, val in topics.items():
			if (topics[key].get("function") is not None):
				print (datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " - " + "Subscribed to topic: " + topics[key].get("topic"))
				client.subscribe(topics[key].get("topic"))
	else:
		print (datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " - " + "Connection failed")
 
client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_connect = on_connect
client.username_pw_set( "USERNAME" , "PASSWORD" )
client.connect("MQTT_SERVER_IP_ADDRESS", PORT)

client.loop_start()

try:
	# loop thru devices and execute functions to check if online / offline or whatever...
	while True:
		for key, val in topics.items():
			if (topics[key].get("function") is not None):
				print (
					datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " -",
					"Device state: " + topics[key].get("topic"),
					eval(topics[key].get("function") + "('" + topics[key].get("topic") + "', None)")
				)

		# keep logfile filesize at max 1MB (1024(1KB) * 1024) = 1MB...
		if os.stat('mqtt-client.log').st_size >= (1024 * 1024):
			log.close()
			log = open('mqtt-client.log', 'w')
			sys.stdout = log

		sys.stdout.flush()
		time.sleep(30)

except KeyboardInterrupt:
	print (datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " - " + "Exiting")
	client.disconnect()
	client.loop_stop()
