from flask import Flask
from flask_restful import Api, Resource, reqparse

action_func = None

class WebHost():

    def __init__(self, host, port):
        self.host = host
        self.port = port

        # init Flask and Api
        self.app = Flask(__name__)
        self.api = Api(self.app)

    def listen(self, key, action):
        global action_func
        action_func = action
        self.api.add_resource(Action, "/"+key)

    def connect(self):
        self.app.run(debug=True, host=self.host, port=self.port)


class Action(Resource):
    def post(self):
        action_func()
        return 202 # Accept