from config import Config
import paho.mqtt.client as mqtt
from webhost import WebHost

# webhost func
def webhost_listen_func():
    # publish to mqtt signal
    client.publish(config.mqtt_topic_control, "1")

# init and read configuration
config = Config()
config.read()

# init MQTT
client = mqtt.Client()

# conntect mqtt
print("connecting mqtt : host="+config.mqtt_host+" : port="+str(config.mqtt_port))
client.connect(config.mqtt_host, config.mqtt_port, 60)
client.loop_start()

# init webhost
webhost = WebHost(config.webhost_host, config.webhost_port)
webhost.listen(config.webhost_listen, webhost_listen_func)

# webhost connect
print("connecting webhost : host="+config.webhost_host+" : port="+str(config.webhost_port))
webhost.connect()