from logging import log
import os
import logging
import argparse
import sys
from flask import Flask, request, json
import asyncio
from werkzeug.serving import is_running_from_reloader
from fence_state import FenceState, StateHelper
from motor.threadbased import Motor

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(message)s',)

motor = Motor()
motor.set_position(5)
fence_state = FenceState()

HOST = '0.0.0.0'

arg_parser = argparse.ArgumentParser(description='Start fence server.')
arg_parser.add_argument('-p', '--port',
                        default=80,
                        type=int,
                        help='Port to use for server.',
                        metavar='port',)
PORT = arg_parser.parse_known_args()[0].port

class RequestPaths:
    FENCE_PATH = '/fence'
    SAVE_POSITION_PATH = FENCE_PATH + '/save_position'

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route(RequestPaths.FENCE_PATH)
def fence():
    return fence_state.get_state()

@app.route(RequestPaths.SAVE_POSITION_PATH, methods=['POST'])
def save_position():
    position = getObjectFromRequest(request)[StateHelper.POSITION_KEY]
    logging.debug(f'server got pos: {position}')
    fence_state.set_position(position)
    motor.set_position(position)
    return fence_state.get_state()

def getObjectFromRequest(request):
    return json.loads(request.data.decode())

if __name__ == '__main__':
    app.run(host= HOST, debug=False, port=PORT)