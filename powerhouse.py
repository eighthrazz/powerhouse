import paho.mqtt.client as mqtt
import configparser
import time
import schedule
import threading
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

# TEMP
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
def scheduler_thread():
    while 1:
        schedule.run_pending()
        time.sleep(1)
def test():
    print("test")
schedule.every(3).seconds.do(test).tag("status")
run_threaded(scheduler_thread)

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
        toggleOff()
    elif msg.payload.decode('UTF-8') == '1':
        toggleOn()

# callback when disconnect from MQTT server
def on_disconnect():
    print("disconnected")

print("initializing mqtt...")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# toggle on
def toggleOn():
    print("toggleOn")
    switch.on()
    global power_house_status
    power_house_status = True
    publishStatus()

# toggle off
def toggleOff():
    print("toggleOff")
    switch.off()
    global power_house_status
    power_house_status = False
    publishStatus()

# publish status
def publishStatus():
    print("publishStatus: "+str(power_house_status))
    if power_house_status:
        client.publish(topic_status, 'on')
    else:
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