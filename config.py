import configparser
import os

class Config:
    config_file = None
    host = None
    port = None
    topic_control = None
    topic_status = None
    pin = None

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
        self.host = config.get('mqtt', 'host')
        self.port = config.getint('mqtt', 'port')
        self.topic_control = config.get('mqtt', 'topic_control')
        self.topic_status = config.get('mqtt', 'topic_status')

        # gpio config
        self.pin = config.getint('gpio', 'pin')