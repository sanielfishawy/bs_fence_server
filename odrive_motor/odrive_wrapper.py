import time
import logging
import odrive
from odrive.enums import *
if __name__ == '__main__':
    from odrive_error import OdriveError
else:
    from .odrive_error import OdriveError


class OdriveWrapper:
    REVELOUTIONS_PER_INCH = 50/9.828

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

    def __init__(
        self,
        axis=0,
    ):
        self.odrive = odrive.find_any()
        self.axis = self.odrive.axis0 if axis == 0 else self.odrive.axis1
        self.odrive_error = OdriveError(odrv=self.odrive, axis=axis)
        logging.basicConfig(level=logging.INFO)

        self.odrive_error.log_errors()
        self.odrive_error.clear_errors()
        self.stop()
        self.calibrate_encoder()
        self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
        self.axis.controller.config.input_mode = INPUT_MODE_POS_FILTER
        self.axis.controller.config.input_filter_bandwidth = 8
        self.set_velocity_limit(80)
        self.odrive_error.log_errors()

    def calibrate_motor_and_save(self):
        self.axis.requested_state = AXIS_STATE_MOTOR_CALIBRATION
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)
        self.axis.motor.config.pre_calibrated = True
        self.odrive.save_configuration()
        logging.info('Calibrated motor and saved configuration')
        o.odrive_error.log_errors()
        o.odrive_error.clear_errors()

    def calibrate_encoder(self):
        logging.info('Start encoder calibration')
        self.axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)
        logging.info('Done encoder calibration')

    def run(self):
        self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    def stop(self):
        logging.info('Motor stop')
        self.axis.requested_state = AXIS_STATE_IDLE

    def get_axis_current_state(self):
        return self.__class__.AXIS_STATES[self.axis.current_state]

    def get_control_mode(self):
        return self.__class__.CONTROL_MODES[self.axis.controller.config.control_mode]

    def set_position(self, pos):
        self.axis.controller.input_pos = pos

    def set_position_inches(self, pos):
        self.set_position(pos * self.__class__.REVELOUTIONS_PER_INCH)

    def get_position(self):
        return self.axis.encoder.pos_estimate

    def set_velocity_limit(self, limit):
        self.axis.controller.config.vel_limit = limit

    def get_velocity_limit(self):
        return self.axis.controller.config.vel_limit

    def get_input_mode(self):
        return self.__class__.INPUT_MODES[self.axis.controller.config.input_mode]

if __name__ == '__main__':
    o = OdriveWrapper()
    # o.odrive_error.log_errors()
    pass
