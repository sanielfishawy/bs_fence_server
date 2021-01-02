from asyncio.queues import Queue
import logging
import asyncio
import time
import RPi.GPIO as gpio
from threading import Thread
from periodic import Periodic

class Motor(Thread):

    DIR_PIN = 11
    PULSE_PIN = 13
    CLOCKWISE = gpio.LOW
    COUNTER_CLOCKWISE = gpio.HIGH
    DIRECTION_KEY = 'direction'
    PULSES_KEY = 'pulses'
    POSITION_KEY = 'position'
    PULSES_PER_INCH = 500

    def __init__(self, position=15) -> None:
        super().__init__()
        self.position = position

        self.cls = self.__class__
        self.setup_logging()
        self.queue = asyncio.Queue()
        self.setup_pins()
        self.periodic = Periodic(period_sec=.0003)

    def set_position(self, position):
        self.add_command({self.cls.POSITION_KEY: position})

    def setup_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='(%(threadName)-9s) %(message)s',)

    def setup_pins(self):
        gpio.setmode(gpio.BOARD)
        # gpio.setwarnings(False)
        gpio.setup([self.cls.DIR_PIN, self.cls.PULSE_PIN], gpio.OUT, initial=gpio.LOW)

    def set_direction(self, dir):
        gpio.output(self.cls.DIR_PIN, dir)
        return self

    async def go_to_position(self, position):
        logging.debug('in go to position')
        direction =  self.cls.CLOCKWISE if position > self.position else self.cls.COUNTER_CLOCKWISE
        inches = position - self.position
        pulses = abs(int(inches * self.cls.PULSES_PER_INCH))
        logging.debug(f'direction: {direction}, pulses: {pulses}')
        self.set_direction(direction)
        await self.send_pulses_periodic(pulses)
        self.position = position

    def send_pulse(self):
        gpio.output(self.cls.PULSE_PIN, gpio.HIGH)
        gpio.output(self.cls.PULSE_PIN, gpio.LOW)

    async def send_pulse_periodic(self):
        await self.periodic.wait_for_period_boundary()
        gpio.output(self.cls.PULSE_PIN, gpio.HIGH)
        await self.periodic.wait_for_semi_period_boundary()
        gpio.output(self.cls.PULSE_PIN, gpio.LOW)

    def send_pulses(self, num: int):
        for i in range(num):
            self.send_pulse()
            time.sleep(.0002)
        return self

    async def send_pulses_periodic(self, num):
        for i in range(num):
            await self.send_pulse_periodic()

    def add_command(self, command):
        logging.info(f'Added to queue: {command}')
        self.queue.put_nowait(command)

    async def task(self, name, queue: asyncio.Queue):
        while(True):
            task_desc = await queue.get()
            logging.info(f'processing command: {task_desc}')
            # pulses =task_desc[self.cls.PULSES_KEY]
            # direction = task_desc[self.cls.DIRECTION_KEY]
            # self.set_direction(direction)
            # await self.send_pulses_periodic(pulses)
            position = task_desc[self.cls.POSITION_KEY]
            logging.info(f'position: {position}')
            await self.go_to_position(position)
            self.position = position
            queue.task_done()

    def setup_workers(self):
        logging.debug('in setup workers')
        self.task = asyncio.create_task(self.task('worker1', self.queue))
        logging.debug('setup workers complete')

    async def run_async(self):
        logging.debug('in run_async')
        # await self.queue.join()
        logging.debug('queue joined')
        self.setup_workers()
        print('run async complete')

    def run(self):
        logging.debug('run started')
        self.loop = asyncio.new_event_loop()
        logging.debug('created loop')
        asyncio.set_event_loop(self.loop)
        logging.debug('set loop')
        asyncio.run_coroutine_threadsafe(self.run_async(), self.loop)
        logging.debug('calling async run')
        self.loop.run_forever()
        logging.debug('run forever')


if __name__ == '__main__':
    m = Motor()
    m.start()
    # m.add_command({Motor.DIRECTION_KEY: Motor.CLOCKWISE, Motor.PULSES_KEY: 1000})
    # m.add_command({Motor.DIRECTION_KEY: Motor.COUNTER_CLOCKWISE, Motor.PULSES_KEY: 1000})
    # m.add_command({Motor.POSITION_KEY: 11})
    # m.add_command({Motor.POSITION_KEY: 8.2})
    m.set_position(5)
    m.set_position(10)
    m.set_position(7)
    m.set_position(12)
    m.set_position(2)