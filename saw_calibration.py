import logging
from saw_state import SawState
from odrive_motor.stop_finder import StopFinder
from odrive_motor.odrive_wrapper import OdriveWrapper

class SawCalibration:

    MARGIN_FROM_STOP = 2

    @classmethod
    def set_log_level(cls, level=logging.INFO):
        logging.basicConfig(level=level)

    @classmethod
    def set_max_stop(cls):
        SawState.set_max_position(StopFinder().find_stop() - cls.MARGIN_FROM_STOP)

    @classmethod
    def set_min_stop(cls):
        SawState.set_min_position(StopFinder().find_stop(positive_direction=False) + cls.MARGIN_FROM_STOP)

    @classmethod
    def set_both_stops(cls):
        cls.set_max_stop()
        cls.set_min_stop()
        SawState.set_limits_set(True)
        logging.info(f'Set stops: max_pos: {SawState.get_max_position()} min_pos: {SawState.get_min_position()}')

if __name__ == '__main__':
    SawCalibration.set_both_stops()
    print(SawState.get_max_position())
    print(SawState.get_min_position())
    pass