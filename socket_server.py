from flask import Flask
from flask_socketio import SocketIO
from werkzeug import debug
from odrive_motor.odrive_wrapper import OdriveWrapper
from fence_state import SawState, StateHelper

class Commands:
    SAVE_POSITION= 'save_position'
    CHANGE_POSITION= 'change_position'

class ParameterKeys:
    COMMAND_KEY = 'command'
    POSITION_KEY = 'position'

fence_state = SawState()
motor = OdriveWrapper(axis=0)
motor.run()

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('json')
def handle_json(jsn):
    print(str(jsn))
    if get_command(jsn) == Commands.CHANGE_POSITION:
        change = jsn[ParameterKeys.POSITION_KEY]
        position = fence_state.get_position() + change
        set_state_and_devices(position)

@socketio.on('connect')
def test_connect():
    print('Client connected ')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

def get_command(jsn):
    return jsn[ParameterKeys.COMMAND_KEY]

def set_state_and_devices(position):
    fence_state.set_position(position)
    motor.set_position_inches(fence_state.get_position())

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5005, debug=True, use_reloader=True, log_output=True)