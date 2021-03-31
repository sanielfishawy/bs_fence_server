from saw_state import SawState
from threading import Thread
import logging
from flask import Flask
from flask_socketio import SocketIO, send, emit
from werkzeug import debug
from saw_up_down_control import SawUpDownControl
from text_ui import TextUI

logging.basicConfig(level=logging.DEBUG)

class Commands:
    SAVE_POSITION = 'save_position'
    CHANGE_POSITION = 'change_position'
    UPDATE_STATE = 'update_state'

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

@socketio.on(Commands.SAVE_POSITION)
def handle_save_position(jsn):
    pos = jsn[ParameterKeys.POSITION_KEY]
    SawUpDownControl.set_position_inches(pos)

@socketio.on(Commands.CHANGE_POSITION)
def handle_change_position(jsn):
    pos = jsn[ParameterKeys.POSITION_KEY]
    SawUpDownControl.change_position_inches(pos)

@socketio.on('connect')
def test_connect():
    print('Client connected ')
    emit(Commands.UPDATE_STATE, SawState.get_state())

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

def get_command(jsn):
    return jsn[ParameterKeys.COMMAND_KEY]

def broadcast_state(state):
    emit(Commands.UPDATE_STATE, state)

SawState.add_observer(broadcast_state)

if __name__ == '__main__':
    # TextUI().start()
    # socketio.run(app, host='0.0.0.0', port=5005, debug=False, use_reloader=False, log_output=True)
    socketio.run(app, host='localhost', port=5005, debug=False, use_reloader=False, log_output=True)
