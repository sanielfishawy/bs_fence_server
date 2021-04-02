
import time
from threading import Thread
import logging

from flask import Flask
from flask_socketio import SocketIO, send, emit

from saw_state import SawState
from saw_up_down_control import SawUpDownControl
from text_ui import TextUI


logging.basicConfig(level=logging.DEBUG)
SawState.initialize_from_saved_state()

class Commands:
    SAVE_POSITION = 'save_position'
    CHANGE_POSITION = 'change_position'
    UPDATE_STATE = 'update_state'
    FIND_STOPS = 'find_stops'
    CLEAR_ERRORS = 'clear_errors'
    SAVE_REVOLUTIONS_PER_INCH = 'save_revolutions_per_inch'
    SAVE_ZERO_POSITION = 'save_zero_position'

class ParameterKeys:
    COMMAND_KEY = 'command'
    POSITION_KEY = 'position'

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')
    
# app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, cors_allowed_origins="*")

@sio.on('connect')
def test_connect():
    logging.info('Client connected ')
    broadcast_state(SawState.get_state())

@sio.on('disconnect')
def test_disconnect():
    logging.info('Client disconnected')

@sio.on(Commands.SAVE_POSITION)
def save_position(position):
    logging.info(f'save_position {position}')
    SawUpDownControl.set_position_inches(float(position))

@sio.on(Commands.CHANGE_POSITION)
def change_position(position):
    logging.info(f'change_position {position}')
    SawUpDownControl.change_position_inches(float(position))

@sio.on(Commands.FIND_STOPS)
def find_position():
    logging.info('find_stops')
    SawUpDownControl.set_both_stops()

@sio.on(Commands.CLEAR_ERRORS)
def clear_errors():
    logging.info('clear_errors')
    SawState.clear_error()

@sio.on(Commands.SAVE_REVOLUTIONS_PER_INCH)
def save_revolutions_per_inch(rpi):
    logging.info(f'save_revolutions_per_inch {rpi}')
    SawState.set_revolutions_per_inch(float(rpi))

@sio.on(Commands.SAVE_ZERO_POSITION)
def save_zero_position(zero):
    logging.info(f'save_zero_position {zero}')
    SawUpDownControl.set_zero(zero=zero)

def broadcast_state(state):
    sio.emit(Commands.UPDATE_STATE, state, broadcast=True)

SawState.add_observer(broadcast_state)
sio.run(app, host='0.0.0.0', port=80, debug=True, use_reloader=False, log_output=True)