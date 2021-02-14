import odrive
from odrive.enums import *
import logging


class OdriveErrorHelper:

    AXIS_ERRORS = {
        AXIS_ERROR_NONE: 'none',
        AXIS_ERROR_INVALID_STATE: 'invalid_state',
        AXIS_ERROR_DC_BUS_UNDER_VOLTAGE: 'dc_bus_under_voltage',
        AXIS_ERROR_DC_BUS_OVER_VOLTAGE: 'dc_bus_over_voltage',
        AXIS_ERROR_CURRENT_MEASUREMENT_TIMEOUT: 'current_measurement_timeout',
        AXIS_ERROR_BRAKE_RESISTOR_DISARMED: 'brake_resistor_disarmed',
        AXIS_ERROR_MOTOR_DISARMED: 'motor_disarmed',
        AXIS_ERROR_MOTOR_FAILED: 'motor_failed',
        AXIS_ERROR_SENSORLESS_ESTIMATOR_FAILED: 'sensorless_estimator_failed',
        AXIS_ERROR_ENCODER_FAILED: 'encoder_failed',
        AXIS_ERROR_CONTROLLER_FAILED: 'controller_failed',
        AXIS_ERROR_POS_CTRL_DURING_SENSORLESS: 'pos_control_during_sensorless',
        AXIS_ERROR_WATCHDOG_TIMER_EXPIRED: 'watchdog_timer_expired',
        AXIS_ERROR_MIN_ENDSTOP_PRESSED: 'min_endstop_pressed',
        AXIS_ERROR_MAX_ENDSTOP_PRESSED: 'max_endstop_pressed',
        AXIS_ERROR_ESTOP_REQUESTED: 'estop_requested',
        AXIS_ERROR_HOMING_WITHOUT_ENDSTOP: 'homing_without_endstop',
        AXIS_ERROR_OVER_TEMP: 'over_temp',
    }

    def __init__(self, axis=0):
        self.odrive = odrive.find_any()
        self.axis = self.odrive.axis0 if axis == 0 else self.odrive.axis1
        logging.basicConfig(level=logging.INFO)

    def display_axis_errors(self):
        err = self.axis.error
        logging.info("Axis Errors:")
        for err_code in self.__class__.AXIS_ERRORS:
            if err & err_code != 0:
                logging.info(self.__class__.AXIS_ERRORS[err_code])

    def clear_errors(self):
        self.axis.clear_errors()


if __name__ == '__main__':
    e = OdriveErrorHelper()
    e.display_axis_errors()
    e.clear_errors()
    e.display_axis_errors()
    pass
