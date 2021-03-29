from asyncio.queues import Queue
import logging
import queue
import time
import RPi.GPIO as gpio
import threading

class Motor:

    DIR_PIN = 11
    PULSE_PIN = 13
    CLOCKWISE = gpio.LOW
    COUNTER_CLOCKWISE = gpio.HIGH
    DIRECTION_KEY = 'direction'
    PULSES_KEY = 'pulses'
    POSITION_KEY = 'position'
    PULSES_PER_INCH = 1000

    def __init__(self, position=15) -> None:
        super().__init__()
        self.setup_logging()
        self.cls = self.__class__
        self.position = position

        self.setup_pins()

        self.queue = queue.Queue()
        self.setup_workers()

    def set_position(self, position):
        logging.debug(f'motor setting position: {position}')
        self.add_command({self.cls.POSITION_KEY: position})

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='(%(threadName)-9s) %(message)s',)

    def setup_pins(self):
        gpio.setmode(gpio.BOARD)
        # gpio.setwarnings(False)
        gpio.setup([self.cls.DIR_PIN, self.cls.PULSE_PIN], gpio.OUT, initial=gpio.LOW)

    def set_direction(self, dir):
        gpio.output(self.cls.DIR_PIN, dir)
        return self

    def go_to_position(self, position):
        logging.debug('in go to position')
        direction =  self.cls.CLOCKWISE if position > self.position else self.cls.COUNTER_CLOCKWISE
        inches = position - self.position
        pulses = abs(int(inches * self.cls.PULSES_PER_INCH))
        logging.debug(f'direction: {direction}, pulses: {pulses}')
        self.set_direction(direction)
        self.send_pulses(pulses)
        self.position = position

    def send_pulse(self):
        gpio.output(self.cls.PULSE_PIN, gpio.HIGH)
        time.sleep(.00005)
        gpio.output(self.cls.PULSE_PIN, gpio.LOW)
        time.sleep(.00005)

    def send_pulses(self, num: int):
        for i in range(num):
            self.send_pulse()
        return self

    def add_command(self, command):
        logging.debug(f'Added to queue: {command}')
        self.queue.put_nowait(command)
        logging.debug(f'queue: {self.queue}')

    def worker(self):
        while(True):
            task_desc = self.queue.get()
            logging.info(f'processing command: {task_desc}')
            # pulses =task_desc[self.cls.PULSES_KEY]
            # direction = task_desc[self.cls.DIRECTION_KEY]
            # self.set_direction(direction)
            position = task_desc[self.cls.POSITION_KEY]
            self.go_to_position(position)
            self.position = position
            self.queue.task_done()

    def setup_workers(self):
        logging.debug('in setup workers')
        threading.Thread(target=self.worker, daemon=True).start()
        logging.debug('setup workers complete')



if __name__ == '__main__':
    m = Motor()
    # m.add_command({Motor.DIRECTION_KEY: Motor.CLOCKWISE, Motor.PULSES_KEY: 1000})
    # m.add_command({Motor.DIRECTION_KEY: Motor.COUNTER_CLOCKWISE, Motor.PULSES_KEY: 1000})
    # m.add_command({Motor.POSITION_KEY: 11})
    # m.add_command({Motor.POSITION_KEY: 8.2})
    m.set_position(5)
    m.set_position(10)
    m.set_position(7)
    m.set_position(12)
    m.set_position(2)

    m.queue.join()