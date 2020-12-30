from nextion_io import NextionIO
import logging

class NextionClient:

    def __init__(self):
        self.nex = NextionIO(event_callback=self.on_touch, get_callback=self.on_get)
        self.nex.start()
        # self.nex.subscribe()

    def on_touch(self, _type, data):
        if data.component_id == 3:
            logging.info('send button pressed')
            self.nex.get_field('t0.txt')

    def on_get(self, value):
        logging.info(f'got {value}')

    def set_inches(self, inches):
        self.nex.set_field('t0.txt', inches)

    def get_inches(self):
        self.nex.add_task()

if __name__ == '__main__':
    nc = NextionClient()



