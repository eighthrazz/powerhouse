import paho.mqtt.client as mqtt
import time
import schedule
import threading
from config import Config
from switch import Switch
from time import sleep

# read config file
config = Config()
config.read()

# init pin
print("initializing switch...")
switch = Switch(config.pin)

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
    print("connected  : topic="+config.topic_control+" : status="+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config.topic_control)

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
    publishStatus()

# toggle off
def toggleOff():
    print("toggleOff")
    switch.off()
    publishStatus()

# publish status
def publishStatus():
    print("publishStatus: "+str(switch.get_status()))
    if switch.get_status():
        client.publish(config.topic_status, 'on')
    else:
        client.publish(config.topic_status, 'off')

# toggle the switch off
toggleOff()

# conntect mqtt
print("connecting : host="+config.host+" : port="+str(config.port))
client.connect(config.host, config.port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()