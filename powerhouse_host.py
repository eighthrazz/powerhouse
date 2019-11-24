from config import Config
from log import Log
import paho.mqtt.client as mqtt
from webhost import WebHost

# webhost func
def webhost_listen_func(request):
    # publish to mqtt signal
    logger.info("Request received from %s. Publishing activation request." % request.remote_addr)
    client.publish(config.mqtt_topic_control, "1")

# init and read configuration
config = Config()
config.read()

# init logging
logger = Log(config.logging_dir, "powerhouse_host")

# init MQTT
client = mqtt.Client()

# conntect mqtt
logger.info("connecting mqtt : host="+config.mqtt_host+" : port="+str(config.mqtt_port))
client.connect(config.mqtt_host, config.mqtt_port, 60)
client.loop_start()

# init webhost
webhost = WebHost(config.webhost_host, config.webhost_port, logger)
webhost.listen(config.webhost_listen, webhost_listen_func)

# webhost connect
logger.info("connecting webhost : host="+config.webhost_host+" : port="+str(config.webhost_port))
webhost.connect()