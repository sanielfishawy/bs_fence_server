from .speech_transcriber import SpeechTranscriber
from .command_interpreter import CommandInterpreter
from .command_executor import post_command
import logging

logging.basicConfig(level=logging.DEBUG,
                        format='(%(threadName)-9s) %(message)s',)

class Runner:

    def __init__(self, request_paths, state_helper, host, port):
        self.request_paths = request_paths
        self.state_helper = state_helper
        self.host = host
        self.port = port
        self.command_interpreter = CommandInterpreter(self.request_paths, self.state_helper)

    def run(self):
        logging.info('speech_commands.runner running')
        SpeechTranscriber(callback=self.interpret_and_execute).start()

    def interpret_and_execute(self, txt):
        command = self.command_interpreter.interpret_command(txt)
        if command:
            logging.debug(command.path)
            logging.debug(command.payload)
            post_command(command, self.host, self.port)


