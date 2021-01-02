from asyncio.queues import Queue
from next_test import run
from threading import Thread
import asyncio
import logging
import random

from nextion import Nextion, EventType

class NextionIO(Thread):

    def __init__(
        self,
        event_callback=None,
        get_callback=None,
    ):
        super().__init__()
        self.event_callback = event_callback
        self.get_callback = get_callback
        self.setup_logging()
        self.queue = asyncio.Queue()

    def setup_logging(self):
        logging.basicConfig(
            format='%(levelname)s %(threadName)s %(message)s',
            level=logging.DEBUG,
            handlers=[
                logging.StreamHandler()
            ])

    def event_handler(self, type_, data):
        if self.event_callback:
            self.event_callback(type_, data)

        if type_ == EventType.STARTUP:
            logging.info('We have booted up!')
        elif type_ == EventType.TOUCH:
            logging.info('A button (id: %d) was touched on page %d' % (data.component_id, data.page_id))

        logging.info('Event %s data: %s', type_, str(data))

    def set_field(self, field, value):
        asyncio.run_coroutine_threadsafe(self.set_field_async(field, value), self.loop)

    async def set_field_async(self, field, value):
        await self.client.set(field, value)

    def get_field(self, field):
        asyncio.run_coroutine_threadsafe(self.get_field_async(field), self.loop)

    async def get_field_async(self, field):
        res = await self.client.get(field)
        if self.get_callback:
            self.get_callback(res)

    async def worker(self, worker_name, queue: asyncio.Queue):
        while True:
            val = await queue.get()
            logging.info(f'{worker_name} got {val}')
            queue.task_done()

    async def setup_workers(self):
        self.task = asyncio.create_task(self.worker('worker1', self.queue))
        # await self.queue.join()

    def add_task(self, value):
        self.queue.put_nowait(value)

    async def start_async(self):
        await self.setup_workers()

    async def run_async(self):
        print("in run async")
        await self.setup_workers()
        print('done with workers.')
        self.client = Nextion('/dev/serial0', 9600, self.event_handler, loop=self.loop)
        await self.client.connect()
        # logging.info(await self.client.get('t0.txt'))
        # await self.client.set('t2.txt', "%.1f" % (random.randint(0, 1000) / 10))

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        asyncio.run_coroutine_threadsafe(self.run_async(), self.loop)
        self.loop.run_forever()


if __name__ == '__main__':
    nex = NextionIO()
    nex.start()
    nex.add_task('a')
    nex.add_task('b')
    pass

