import time
import logging
import odrive

from odrive.enums import *
from .odrive_error import OdriveError

class OdriveWrapper:

    # ODrive.Axis.AxisState
    AXIS_STATES = {
        AXIS_STATE_UNDEFINED: 'undefined',
        AXIS_STATE_IDLE: 'idle',
        AXIS_STATE_STARTUP_SEQUENCE: 'startup_sequence',
        AXIS_STATE_FULL_CALIBRATION_SEQUENCE: 'full_calibration_sequence',
        AXIS_STATE_MOTOR_CALIBRATION: 'motor_calibration',
        AXIS_STATE_SENSORLESS_CONTROL: 'sensorless_control',
        AXIS_STATE_ENCODER_INDEX_SEARCH: 'encoder_index_search',
        AXIS_STATE_ENCODER_OFFSET_CALIBRATION: 'encoder_offset_calibration',
        AXIS_STATE_CLOSED_LOOP_CONTROL: 'closed_loop_control',
        AXIS_STATE_LOCKIN_SPIN: 'lockin_spin',
        AXIS_STATE_ENCODER_DIR_FIND: 'encoder_dir_find',
        AXIS_STATE_HOMING: 'homing',
    }

    # ODrive.Controller.ControlMode
    CONTROL_MODES = {
        CONTROL_MODE_VOLTAGE_CONTROL: 'voltage_control',
        CONTROL_MODE_TORQUE_CONTROL: 'torque_control',
        CONTROL_MODE_VELOCITY_CONTROL: 'velocity_control',
        CONTROL_MODE_POSITION_CONTROL: 'position_control',
    }

    INPUT_MODES = {
        INPUT_MODE_INACTIVE: 'inactive',
        INPUT_MODE_PASSTHROUGH: 'pass_through',
        INPUT_MODE_VEL_RAMP: 'vel_ramp',
        INPUT_MODE_POS_FILTER: 'pos_filter',
        INPUT_MODE_MIX_CHANNELS: 'mix_channels',
        INPUT_MODE_TRAP_TRAJ: 'trap_traj',
        INPUT_MODE_TORQUE_RAMP: 'torque_ramp',
        INPUT_MODE_MIRROR: 'mirror',
    }

    _instance = None

    def __init__(
        self,
        axis=0,
    ):
        if self.__class__._instance is not None:
            raise Exception(f'{self.__class__.__name__} is a singleton class call get_instance!')
        self.__class__._instance = self

        self.odrive = self.get_odrive()
        if not self.odrive:
            raise Exception('No odrive found')

        self.axis = self.odrive.axis0 if axis == 0 else self.odrive.axis1
        self.odrive_error = OdriveError(odrv=self.odrive, axis=axis)
        logging.basicConfig(level=logging.INFO)

        self.stop()
        # self.full_calibration_and_save()
        self.calibrate_motor_and_save()
        self.calibrate_encoder_and_save()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            OdriveWrapper()
        return cls._instance

    def get_odrive(self):
        od = odrive.find_any(timeout=2)
        return od

    def check_and_clear_errors(self):
        if self.odrive_error.has_errors():
            self.odrive_error.log_errors()
            self.odrive_error.clear_errors()
            self.odrive_error.log_errors()

    def calibrate_motor_and_save(self, force=False):
        logging.info('Start motor calibration')
        self.check_and_clear_errors()

        if force:
            self.axis.motor.config.pre_calibrated = False

        if self.axis.motor.config.pre_calibrated:
            logging.info('Motor was precalibrated. Use force=True to force another calibration')
            return

        self.axis.requested_state = AXIS_STATE_MOTOR_CALIBRATION
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

        if self.odrive_error.has_errors():
            raise CalibrationError(self.odrive_error.get_error_string())

        self.axis.motor.config.pre_calibrated = True
        self.odrive.save_configuration()
        logging.info('Done motor calibration')

    def calibrate_encoder_and_save(self, force=False):
        logging.info('Start encoder calibration')

        self.check_and_clear_errors()

        if force:
            self.axis.encoder.config.pre_calibrated = False

        if self.axis.encoder.config.pre_calibrated:
            logging.info('Encoder was precalibrated. Use force=True to force another calibration')
            return

        self.axis.encoder.config.use_index = True
        self.encoder_index_search()
        self.axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION

        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

        if self.odrive_error.has_errors():
            raise CalibrationError(self.odrive_error.get_error_string())

        self.axis.encoder.config.pre_calibrated = True
        self.axis.config.startup_encoder_index_search = True
        self.odrive.save_configuration()
        logging.info('Done encoder calibration')

    def full_calibration_and_save(self, force=False):
        logging.info('Start full calibration')
        self.check_and_clear_errors()

        if force:
            self.axis.encoder.config.pre_calibrated = False
            self.axis.motor.config.pre_calibrated = False

        self.axis.encoder.config.use_index = True
        self.axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

        if self.odrive_error.has_errors():
            raise CalibrationError(self.odrive_error.get_error_string())

        self.axis.encoder.config.pre_calibrated = True
        self.axis.motor.config.pre_calibrated = True
        self.odrive.save_configuration()
        logging.info('Done full calibration')

    def encoder_index_search(self):
        logging.info('Start encoder index search')

        self.check_and_clear_errors()

        self.axis.encoder.config.use_index = True
        self.axis.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH

        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

        if self.odrive_error.has_errors():
            raise CalibrationError(self.odrive_error.get_error_string())

        logging.info('Done encoder index search')

    def run(self, filter=True, bandwith=8, pos_gain=300, velocity_limit=30):
        logging.info('Motor run')
        self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
        if filter:
            self.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
        else:
            self.axis.controller.config.input_mode = INPUT_MODE_PASSTHROUGH

        self.axis.controller.config.pos_gain = pos_gain
        self.axis.controller.config.input_filter_bandwidth = bandwith
        self.set_velocity_limit(velocity_limit)
        self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    def stop(self):
        logging.info('Motor stop')
        self.axis.requested_state = AXIS_STATE_IDLE

    def get_axis_current_state(self):
        return self.__class__.AXIS_STATES[self.axis.current_state]

    def get_control_mode(self):
        return self.__class__.CONTROL_MODES[self.axis.controller.config.control_mode]

    def set_position(self, pos):
        logging.info(f'Motor set_position {pos}')
        self.axis.controller.input_pos = pos

    def get_position(self):
        return self.axis.encoder.pos_estimate

    def set_velocity_limit(self, limit):
        self.axis.controller.config.vel_limit = limit

    def get_velocity_limit(self):
        return self.axis.controller.config.vel_limit

    def get_input_mode(self):
        return self.__class__.INPUT_MODES[self.axis.controller.config.input_mode]

class CalibrationError(Exception):
    pass

