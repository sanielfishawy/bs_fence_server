import asyncio
import logging
import random

from nextion import Nextion, EventType

def event_handler(type_, data):
    if type_ == EventType.STARTUP:
        print('We have booted up!')
    elif type_ == EventType.TOUCH:
        print('A button (id: %d) was touched on page %d' % (data.component_id, data.page_id))

    logging.info('Event %s data: %s', type, str(data))

async def run():
    client = Nextion('/dev/serial0', 9600, event_handler)
    await client.connect()

    # await client.sleep()
    # await client.wakeup()

    # await client.command('sendxy=0')

    print(await client.get('sleep'))
    print(await client.get('t0.txt'))

    # await client.set('t0.txt', "%.1f" % (random.randint(0, 1000) / 10))
    # await client.set('t1.txt', "%.1f" % (random.randint(0, 1000) / 10))
    # await client.set('t2.txt', "%.1f" % (random.randint(0, 1000) / 10))


    print('finished')

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler()
        ])
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run())
    loop.run_forever()