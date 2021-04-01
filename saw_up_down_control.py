import logging
from saw_state import SawState
from odrive_motor.stop_finder import StopFinder
from odrive_motor.odrive_wrapper import OdriveWrapper, OdriveError

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
        try: 
            SawState.set_max_position(StopFinder().find_stop() - cls.MARGIN_FROM_STOP)
        except OdriveError as err:
            SawState.add_error(str(err))
        except:
            raise

    @classmethod
    def set_min_stop(cls):
        try:
            SawState.set_min_position(StopFinder().find_stop(positive_direction=False) + cls.MARGIN_FROM_STOP)
        except OdriveError as err:
            SawState.add_error(str(err))
        except:
            raise

    @classmethod
    def set_both_stops(cls):
        cls.set_max_stop()
        cls.set_min_stop()
        SawState.set_limits_set(True)
        cls.set_zero()
        SawState.save_state()
        logging.info(f'Set stops: max_pos: {SawState.get_max_position()} zero_pos: {SawState.get_zero_position()} min_pos: {SawState.get_min_position()}')

        try:
            SawState.set_position(OdriveWrapper.get_instance().get_position())
        except OdriveError as err:
            SawState.add_error(err)
        except:
            raise

        cls.run() 
    
    @classmethod
    def set_zero(cls, zero=None):
        if not SawState.get_limits_set():
            SawState.add_error('Attempted to set zero before finding stops')
            return False

        if zero:
            SawState.set_zero_position(zero)
        elif cls.get_saved_distance_from_min_stop_to_zero():
            SawState.set_zero_position(SawState.get_min_position() + cls.get_saved_distance_from_min_stop_to_zero())
        else:
            SawState.set_zero_position( (SawState.get_min_position() + SawState.get_max_position()) / 2.0 )
        
        SawState.save_state()

        return True

    @classmethod
    def get_saved_distance_from_min_stop_to_zero(cls):
        return ( 
                SawState.get_saved_zero_position() and 
                SawState.get_saved_min_position() and 
                SawState.get_saved_zero_position() - SawState.get_saved_min_position() )

    @classmethod
    def is_movable(cls):
        return SawState.get_limits_set()

    #
    #  Move blade
    #
    @classmethod
    def run():
        try:
            OdriveWrapper.get_instance().run()
        except OdriveError as err:
            SawState.add_error(str(err))
        except:
            raise

    @classmethod
    def stop():
        try:
            OdriveWrapper.get_instance().stop()
        except OdriveError as err:
            SawState.add_error(str(err))
        except:
            raise

    @classmethod
    def set_position(cls, pos):
        logging.info(f'set_position {pos}')
        if cls.set_error_if_not_movable(): 
            logging.info('not moveable returning')
            return False

        SawState.set_position(pos)
        pos = SawState.get_position()
        try:
            OdriveWrapper.get_instance().set_position(pos)
        except OdriveError as err:
            SawState.add_error(err)
        except:
            raise

        return pos

    @classmethod
    def set_position_inches(cls, inches):
        logging.info(f'set_position_inches {inches}')
        if cls.set_error_if_not_movable():
            logging.info('not moveable returning')
            return False

        SawState.set_position_inches(inches)
        pos = SawState.get_position()
        pos_inches = SawState.get_position_inches()
        try:
            OdriveWrapper.get_instance().set_position(pos)
        except OdriveError as err:
            SawState.add_error(str(err))
        except:
            raise 

        return pos_inches

    @classmethod
    def change_position(cls, pos):
        logging.info(f'change_position {pos}')
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

# if __name__ == '__main__':
#     s = SawUpDownControl
#     s.set_both_stops()
#     s.set_zero(SawState.get_min_position() + 2)

    # pas