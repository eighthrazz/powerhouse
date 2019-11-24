import paho.mqtt.client as mqtt
import time
from config import Config
from log import Log
from switch import Switch
from scheduler import Scheduler

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    logger.info("mqtt connected : topic="+config.mqtt_topic_control+" : status="+str(rc))

    # start posting the status to MQTT
    status_scheduler.start()

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config.mqtt_topic_control)

# callback when disconnect from MQTT server
def on_disconnect():
    logger.info("disconnected")

    # stop posting the status to MQTT
    status_scheduler.stop()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logger.info("received : topic=%s : payload=%s" % (msg.topic, msg.payload))
    if msg.payload.decode('UTF-8') == '0':
        toggleOff()
    elif msg.payload.decode('UTF-8') == '1':
        toggleOn()

# toggle on
def toggleOn():
    logger.info("toggleOn")
    switch.on()
    publishStatus()

# toggle off
def toggleOff():
    logger.info("toggleOff")
    switch.off()
    publishStatus()

# publish status
def publishStatus():
    logger.debug("publishStatus: "+str(switch.get_status()))
    if switch.get_status():
        client.publish(config.mqtt_topic_status, 'on')
    else:
        client.publish(config.mqtt_topic_status, 'off')

# init and read configuration
config = Config()
config.read()

# init logging
logger = Log(config.logging_dir, "powerhouse")

# init pin
logger.debug("initializing switch...")
switch = Switch(config.gpio_pin)

# init status scheduler
logger.debug("initializing scheduler...")
status_scheduler = Scheduler(publishStatus, 3)

# init MQTT
logger.debug("initializing mqtt...")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# toggle the switch off
toggleOff()

# conntect mqtt
logger.info("connecting mqtt : host="+config.mqtt_host+" : port="+str(config.mqtt_port))
client.connect(config.mqtt_host, config.mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()