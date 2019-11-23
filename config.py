import configparser
import os

class Config:
    config_file = None
    mqtt_host = None
    mqtt_port = None
    mqtt_topic_control = None
    mqtt_topic_status = None
    webhost_host = None
    webhost_port = None
    webhost_listen = None
    gpio_pin = None

    def __init__(self):
        # build path to config file
        thisFolder = os.path.dirname(os.path.abspath(__file__))
        self.configFile = os.path.join(thisFolder, 'config.ini')

    def read(self):
        # read config file
        print("reading configuration : path="+self.configFile)
        config = configparser.ConfigParser()
        config.read(self.configFile)

        # mqtt config
        self.mqtt_host = config.get('mqtt', 'host')
        self.mqtt_port = config.getint('mqtt', 'port')
        self.mqtt_topic_control = config.get('mqtt', 'topic_control')
        self.mqtt_topic_status = config.get('mqtt', 'topic_status')

        # webhost config
        self.webhost_host = config.get('webhost', 'host')
        self.webhost_port = config.get('webhost', 'port')
        self.webhost_listen = config.get('webhost', 'listen')

        # gpio config
        self.gpio_pin = config.getint('gpio', 'pin')