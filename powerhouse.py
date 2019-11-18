import paho.mqtt.client as mqtt
import configparser
import time
import os
from gpiozero import LED
from time import sleep

# on/off status
power_house_status = False

# build path to config file
thisFolder = os.path.dirname(os.path.abspath(__file__))
configFile = os.path.join(thisFolder, 'config.ini')

# read config file
print("reading configuration : path="+configFile)
config = configparser.ConfigParser()
config.read(configFile)

# mqtt config
host = config.get('mqtt', 'host')
port = config.getint('mqtt', 'port')
topic_control = config.get('mqtt', 'topic_control')
topic_status = config.get('mqtt', 'topic_status')

# gpio config
pin = config.getint('gpio', 'pin')

# init pin
print("initializing pin...")
switch = LED(pin)

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("connected  : topic="+topic_control+" : status="+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_control)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("received : topic=%s : payload=%s" % (msg.topic, msg.payload))
    if msg.payload.decode('UTF-8') == '0':
        toggleOn()
    elif msg.payload.decode('UTF-8') == '1':
        toggleOff()

print("initializing mqtt...")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# toggle on
def toggleOn():
    print("toggleOn")
    switch.on()
    power_house_status = True
    client.publish(topic_status, 'on')

# toggle off
def toggleOff():
    print("toggleOff")
    switch.off()
    power_house_status = False
    client.publish(topic_status, 'off')

# toggle the switch off
toggleOff()

# conntect mqtt
print("connecting : host="+host+" : port="+str(port))
client.connect(host, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()