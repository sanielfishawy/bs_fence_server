import speech_recognition
import logging

if __name__ != '__main__':
    from .speech_transcriber import SpeechTranscriber
    from .command_interpreter import CommandInterpreter
    from .command_executor import post_command
else:
    from speech_transcriber import SpeechTranscriber
    from command_interpreter import CommandInterpreter
    from command_executor import post_command

logging.basicConfig(level=logging.INFO,
                        format='(%(threadName)-9s) %(message)s',)

class Runner:

    def __init__(self, request_paths, state_helper, host, port):
        self.request_paths = request_paths
        self.state_helper = state_helper
        self.host = host
        self.port = port
        self.command_interpreter = CommandInterpreter(self.request_paths, self.state_helper)

    def run(self) -> SpeechTranscriber:
        logging.info('speech_commands.runner running')
        speech_transcriber = SpeechTranscriber(callback=self.interpret_and_execute)
        speech_transcriber.start()
        return speech_transcriber

    def interpret_and_execute(self, txt):
        command = self.command_interpreter.interpret_command(txt)
        if command:
            logging.info(command.path)
            logging.info(command.payload)
            post_command(command, self.host, self.port)


