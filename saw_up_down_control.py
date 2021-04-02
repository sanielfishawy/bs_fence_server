import logging
from saw_state import SawState
from odrive_motor.stop_finder import StopFinder
from odrive_motor.odrive_wrapper import OdriveWrapper, OdriveException

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
            SawState.set_max_position(StopFinder().find_stop())
        except OdriveException as err:
            SawState.add_error(str(err))
        except:
            raise

    @classmethod
    def set_min_stop(cls):
        try:
            SawState.set_min_position(StopFinder().find_stop(positive_direction=False))
        except OdriveException as err:
            SawState.add_error(str(err))
        except:
            raise

    @classmethod
    def set_both_stops(cls):
        SawState.set_limits_set(False)
        cls.set_max_stop()
        cls.set_min_stop()
        cls.set_stop_margins()
        SawState.set_limits_set(True)
        cls.set_zero()
        logging.info(f'Set stops: min_pos: {SawState.get_min_position()} zero_pos: {SawState.get_zero_position()} max_pos: {SawState.get_max_position()}')
        SawState.save_state()

        try:
            SawState.set_position(OdriveWrapper.get_instance().get_position())
        except OdriveException as err:
            SawState.add_error(err)
        except:
            raise

        cls.run() 
    
    @classmethod
    def set_stop_margins(cls):
        if SawState.get_min_position() is None or SawState.get_max_position() is None:
            return

        margin = 0.1 * (SawState.get_max_position() - SawState.get_min_position())

        if margin > cls.MARGIN_FROM_STOP:
            margin = cls.MARGIN_FROM_STOP

        SawState.set_min_position(SawState.get_min_position() + margin)
        SawState.set_max_position(SawState.get_max_position() - margin)

    @classmethod
    def set_zero(cls, zero=None):
        if not SawState.get_limits_set():
            print('foo')
            logging.error('Attempted to set zero before finding stops')
            SawState.add_error('Attempted to set zero before finding stops')
            return False

        setpoint = zero
        if setpoint:
            setpoint = max(SawState.get_min_position(), setpoint)
            zero = min(SawState.get_max_position(), setpoint)
        elif cls.get_saved_distance_from_min_stop_to_zero():
            print(f"Using saved distance={cls.get_saved_distance_from_min_stop_to_zero()} from min={SawState.get_min_position()}")
            setpoint = SawState.get_min_position() + cls.get_saved_distance_from_min_stop_to_zero()
            print(f'Got: min_pos: {SawState.get_min_position()} zero_pos: {setpoint} max_pos: {SawState.get_max_position()}')

        if not setpoint or setpoint > SawState.get_max_position():
            print("Using average distance")
            setpoint = (SawState.get_min_position() + SawState.get_max_position()) / 2.0 
            print(f'Got: min_pos: {SawState.get_min_position()} zero_pos: {setpoint} max_pos: {SawState.get_max_position()}')
        
        SawState.set_zero_position(setpoint)
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
    def run(cls):
        try:
            OdriveWrapper.get_instance().run()
        except OdriveException as err:
            SawState.add_error(str(err))
        except:
            raise

    @classmethod
    def stop(cls):
        try:
            OdriveWrapper.get_instance().stop()
        except OdriveException as err:
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
        except OdriveException as err:
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
        except OdriveException as err:
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