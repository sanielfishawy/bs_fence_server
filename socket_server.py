
import time
from threading import Thread
import logging

from flask import Flask
from flask_socketio import SocketIO, send, emit
from werkzeug import debug

from saw_state import SawState
from saw_up_down_control import SawUpDownControl
from text_ui import TextUI


logging.basicConfig(level=logging.DEBUG)

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

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# @socketio.on('json')
# def handle_json(jsn):
#     print(str(jsn))
#     if get_command(jsn) == Commands.CHANGE_POSITION:
#         change = jsn[ParameterKeys.POSITION_KEY]
#         SawUpDownControl.change_position_inches(change)
#     elif get_command(jsn) == Commands.SAVE_POSITION:
#         pos = jsn[ParameterKeys.POSITION_KEY]
#         SawUpDownControl.set_position_inches(pos)

# def get_command(jsn):
#     return jsn[ParameterKeys.COMMAND_KEY]


@socketio.on('connect')
def test_connect():
    logging.info('Client connected ')
    emit(Commands.UPDATE_STATE, SawState.get_state())

@socketio.on('disconnect')
def test_disconnect():
    logging.info('Client disconnected')

@socketio.on(Commands.SAVE_POSITION)
def save_position(position):
    logging.info(f'save_position {position}')
    SawUpDownControl.set_position_inches(float(position))

@socketio.on(Commands.CHANGE_POSITION)
def change_position(position):
    logging.info(f'change_position {position}')
    SawUpDownControl.change_position_inches(float(position))

@socketio.on(Commands.FIND_STOPS)
def find_position():
    logging.info('find_stops')
    time.sleep(2)
    SawState.set_zero_position(0)
    SawState.set_min_and_max_position(-10, 10)

@socketio.on(Commands.CLEAR_ERRORS)
def clear_errors():
    logging.info('clear_errors')
    SawState.clear_error()

@socketio.on(Commands.SAVE_REVOLUTIONS_PER_INCH)
def save_revolutions_per_inch(rpi):
    logging.info(f'save_revolutions_per_inch {rpi}')
    SawState.set_revolutions_per_inch(float(rpi))

@socketio.on(Commands.SAVE_ZERO_POSITION)
def save_zero_position(zero):
    logging.info(f'save_zero_position {zero}')
    SawState.set_zero_position(zero)

def broadcast_state(state):
    emit(Commands.UPDATE_STATE, state)

SawState.add_observer(broadcast_state)

if __name__ == '__main__':
    # TextUI().start()
    # socketio.run(app, host='0.0.0.0', port=5005, debug=False, use_reloader=False, log_output=True)
    socketio.run(app, host='localhost', port=5005, debug=True, use_reloader=False, log_output=True)
