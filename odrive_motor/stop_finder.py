import time
import math
import logging

from .odrive_wrapper import OdriveWrapper


class StopFinder:

    def __init__(
            self,
            log_level=logging.INFO,
        ) -> None:

        logging.basicConfig(level=log_level)
        self.odw = OdriveWrapper.get_instance()

    def find_stop(self, positive_direction=True):
        self.odw.run(filter=True, bandwith=8, pos_gain=50)
        pos = self.odw.get_position()
        while True:
            self.odw.set_position(pos)
            time.sleep(.1)
            diff = abs(pos - self.odw.get_position())
            logging.debug(diff)
            if diff > .7:
                return self.odw.get_position()
            if positive_direction:
                pos += .3
            else:
                pos -= .3


