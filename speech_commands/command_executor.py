import requests
import urllib3
from .command_interpreter import Command
import logging

def post_command(command:Command, host, port):
    try:
        requests.post(f'http://{host}:{port}' + command.path, json=command.payload)
    except:
        logging.error('Connection error. Server probably not running.')
