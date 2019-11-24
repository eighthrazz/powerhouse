from flask import Flask, request
from flask_restful import Api, Resource, reqparse

action_func = None

class WebHost():

    app = Flask(__name__)
    logger = None

    def __init__(self, host, port, logging):
        self.host = host
        self.port = port

        global logger
        logger = logging

        # init Api
        self.api = Api(self.app)

    def listen(self, key, action):
        global action_func
        action_func = action
        self.api.add_resource(Action, "/"+key)

    def connect(self):
        self.app.run(debug=False, host=self.host, port=self.port)

    @app.after_request
    def after_request(response):
        # log every request
        logger.info("request: addr=%s, method=%s, path=%s" % (request.remote_addr, request.method, request.full_path))
        return response

class Action(Resource):
    def post(self):
        action_func(request)
        return 202 # Accept