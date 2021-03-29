import logging
from saw_state import SawState
from odrive_motor.stop_finder import StopFinder
from odrive_motor.odrive_wrapper import OdriveWrapper

class SawUpDownControl:

    MARGIN_FROM_STOP = 2

    @classmethod
    def set_log_level(cls, level=logging.INFO):
        logging.basicConfig(level=level)

    #
    #  Find stops
    #
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
        SawState.set_position(OdriveWrapper.get_instance().get_position())
        OdriveWrapper.get_instance().run()
        logging.info(f'Set stops: max_pos: {SawState.get_max_position()} min_pos: {SawState.get_min_position()}')

    @classmethod
    def is_movable(cls):
        return SawState.get_limits_set()

    #
    #  Move blade
    #
    @classmethod
    def run():
        OdriveWrapper.get_instance().run()

    @classmethod
    def stop():
        OdriveWrapper.get_instance().stop()

    @classmethod
    def set_position(cls, pos):
        if cls.set_error_if_not_movable():
            return False

        SawState.set_position(pos)
        pos = SawState.get_position()
        OdriveWrapper.get_instance().set_position(pos)
        return pos

    @classmethod
    def set_position_inches(cls, inches):
        if cls.set_error_if_not_movable():
            return False

        SawState.set_position_inches(inches)
        pos = SawState.get_position()
        pos_inches = SawState.get_position_inches()
        OdriveWrapper.get_instance().set_position(pos)
        return pos_inches

    @classmethod
    def change_position(cls, pos):
        new_pos = SawState.get_position() + pos
        return cls.set_position(new_pos)

    @classmethod
    def change_position_inches(cls, inches):
        new_inches = SawState.get_position_inches() + inches
        return cls.set_position_inches(new_inches)

    @classmethod
    def set_error_if_not_movable(cls):
        if not cls.is_movable():
            SawState.add_error('Attempted motion before finding stops')
            return True
        return False

if __name__ == '__main__':
    s = SawUpDownControl
    s.set_both_stops()
    s.change_position(1)
    pass