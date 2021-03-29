from threading import Thread
from flask import Flask
from flask_socketio import SocketIO
from werkzeug import debug
from saw_up_down_control import SawUpDownControl
from text_ui import TextUI

class Commands:
    SAVE_POSITION= 'save_position'
    CHANGE_POSITION= 'change_position'

class ParameterKeys:
    COMMAND_KEY = 'command'
    POSITION_KEY = 'position'

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('json')
def handle_json(jsn):
    print(str(jsn))
    if get_command(jsn) == Commands.CHANGE_POSITION:
        change = jsn[ParameterKeys.POSITION_KEY]
        SawUpDownControl.change_position_inches(change)

@socketio.on('connect')
def test_connect():
    print('Client connected ')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

def get_command(jsn):
    return jsn[ParameterKeys.COMMAND_KEY]

if __name__ == '__main__':
    TextUI().start()
    socketio.run(app, host='0.0.0.0', port=5005, debug=True, use_reloader=True, log_output=True)
