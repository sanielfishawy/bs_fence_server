from logging import log
import os
import logging
import argparse
import sys
from flask import Flask, request, json
import asyncio
import speech_recognition
from werkzeug.serving import is_running_from_reloader
from fence_state import SawState, StateHelper
# from motor.threadbased import Motor
from odrive_motor.odrive_wrapper import OdriveWrapper
# from nextion_client import NextionClient
from speech_commands.runner import Runner as SpeechRunner

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(message)s',)

HOST = '0.0.0.0'

class RequestPaths:
    FENCE_PATH = '/fence'
    SAVE_POSITION_PATH = FENCE_PATH + '/save_position'
    CHANGE_POSITION_PATH = FENCE_PATH + '/change_position'


arg_parser = argparse.ArgumentParser(description='Start fence server.')
arg_parser.add_argument('-p', '--port',
                        default=80,
                        type=int,
                        help='Port to use for server.',
                        metavar='port',)

PORT = arg_parser.parse_known_args()[0].port

fence_state = SawState()
# motor = Motor()
# nextion = NextionClient()
motor = OdriveWrapper(axis=0)
motor.run()

speech_runner = SpeechRunner(RequestPaths, StateHelper, HOST, PORT)
speech_runner.run()


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
    set_state_and_devices(position)
    return fence_state.get_state()

@app.route(RequestPaths.CHANGE_POSITION_PATH, methods=['POST'])
def change_position():
    change = getObjectFromRequest(request)[StateHelper.POSITION_KEY]
    logging.debug(f'server got change: {change}')
    position = fence_state.get_position() + change
    set_state_and_devices(position)
    return fence_state.get_state()

def set_state_and_devices(position):
    fence_state.set_position(position)
    motor.set_position_inches(position)

def getObjectFromRequest(request):
    return json.loads(request.data.decode())

if __name__ == '__main__':
    app.run(host= HOST, debug=False, port=PORT)