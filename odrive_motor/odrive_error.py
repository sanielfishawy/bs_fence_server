import odrive
from odrive.enums import *
import logging


class OdriveError:
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

    THERMISTOR_ERRORS = {
        THERMISTOR_CURRENT_LIMITER_ERROR_NONE: 'none',
        THERMISTOR_CURRENT_LIMITER_ERROR_OVER_TEMP: 'thermistor_current_limiter_over_temp',
    }

    CAN_ERRORS = {
        CAN_ERROR_NONE: 'none',
        CAN_ERROR_DUPLICATE_CAN_IDS: 'duplicate_can_ids',
    }

    MOTOR_ERRORS = {

        MOTOR_ERROR_NONE: 'none',
        MOTOR_ERROR_PHASE_RESISTANCE_OUT_OF_RANGE: 'phase_resistance_out_of_range',
        MOTOR_ERROR_PHASE_INDUCTANCE_OUT_OF_RANGE: 'phase_inductance_out_of_range',
        MOTOR_ERROR_ADC_FAILED: 'adc_failed',
        MOTOR_ERROR_DRV_FAULT: 'drv_fault',
        MOTOR_ERROR_CONTROL_DEADLINE_MISSED: 'control_deadline_missed',
        MOTOR_ERROR_NOT_IMPLEMENTED_MOTOR_TYPE: 'not_implemented_motor_type',
        MOTOR_ERROR_BRAKE_CURRENT_OUT_OF_RANGE: 'brake_current_out_of_range',
        MOTOR_ERROR_MODULATION_MAGNITUDE: 'modulation_magnitude',
        MOTOR_ERROR_BRAKE_DEADTIME_VIOLATION: 'brake_deadtime_violation',
        MOTOR_ERROR_UNEXPECTED_TIMER_CALLBACK: 'unexpected_timer_callback',
        MOTOR_ERROR_CURRENT_SENSE_SATURATION: 'current_sense_saturation',
        MOTOR_ERROR_CURRENT_LIMIT_VIOLATION: 'current_limit_violation',
        MOTOR_ERROR_BRAKE_DUTY_CYCLE_NAN: 'barke_duty_cycle_nan',
        MOTOR_ERROR_DC_BUS_OVER_REGEN_CURRENT: 'dc_bus_over_regen_current',
        MOTOR_ERROR_DC_BUS_OVER_CURRENT: 'dc_bus_over_current',
    }

    CONTROLLER_ERRORS = {
        CONTROLLER_ERROR_NONE: 'none',
        CONTROLLER_ERROR_OVERSPEED: 'overspeed',
        CONTROLLER_ERROR_INVALID_INPUT_MODE: 'invalid_input_mode',
        CONTROLLER_ERROR_UNSTABLE_GAIN: 'unstable_gain',
        CONTROLLER_ERROR_INVALID_MIRROR_AXIS: 'invalid_mirror_axis',
        CONTROLLER_ERROR_INVALID_LOAD_ENCODER: 'invalid_load_encoder',
        CONTROLLER_ERROR_INVALID_ESTIMATE: 'invalid_estimate',
    }

    ENCODER_ERRORS = {
        ENCODER_ERROR_NONE: 'none',
        ENCODER_ERROR_UNSTABLE_GAIN: 'unstable_gain',
        ENCODER_ERROR_CPR_POLEPAIRS_MISMATCH: 'cpr_polepairs_mismatch',
        ENCODER_ERROR_NO_RESPONSE: 'no_response',
        ENCODER_ERROR_UNSUPPORTED_ENCODER_MODE: 'unsupported_encoder_mode',
        ENCODER_ERROR_ILLEGAL_HALL_STATE: 'illegal_hall_state',
        ENCODER_ERROR_INDEX_NOT_FOUND_YET: 'index_not_found',
        ENCODER_ERROR_ABS_SPI_TIMEOUT: 'spi_timeout',
        ENCODER_ERROR_ABS_SPI_COM_FAIL: 'spi_com_fail',
        ENCODER_ERROR_ABS_SPI_NOT_READY: 'spi_not_ready',
    }

    SENSORLESS_ESTIMATOR_ERRORS = {
        SENSORLESS_ESTIMATOR_ERROR_NONE: 'none',
        SENSORLESS_ESTIMATOR_ERROR_UNSTABLE_GAIN: 'unstable_gain',
    }

    NAME_KEY = 'name'
    ERRORS_KEY = 'errors'
    ODRIVE_COMMAND_KEY = 'command'



    def __init__(self, odrv=None, axis=0):
        self.cls = self.__class__
        self.odrive = odrv or odrive.find_any()
        self.axis = self.odrive.axis0 if axis == 0 else self.odrive.axis1
        self.error_types = self.get_error_types()
        logging.basicConfig(level=logging.INFO)

    def clear_errors(self):
        logging.info('Clear errors')
        self.axis.clear_errors()

    def get_error_types(self):
        return [
            ErrorType('Axis Errors', self.cls.AXIS_ERRORS, self.axis),
            ErrorType('Thermistor Errors', self.cls.THERMISTOR_ERRORS, self.axis.fet_thermistor),
            ErrorType('CAN Bus Errors', self.cls.CAN_ERRORS, self.odrive.can),
            ErrorType('Motor Errors', self.cls.MOTOR_ERRORS, self.axis.motor),
            ErrorType('Controller Errors', self.cls.CONTROLLER_ERRORS, self.axis.controller),
            ErrorType('Encoder Errors', self.cls.ENCODER_ERRORS, self.axis.encoder),
            ErrorType('Sensorless Estimator Errors', self.cls.SENSORLESS_ESTIMATOR_ERRORS, self.axis.sensorless_estimator),
        ]

    def get_errors(self):
        for error_type in self.error_types:
            error_type.get_errors()
        return self.error_types

    def log_errors(self):
        logging.info(f"ODRIVE ERRORS: {'no errors' if not self.has_errors() else ''}")
        errors = self.get_errors()
        for error in errors:
            if error.errors:
                logging.info(f'{error.name}: {error.errors}')

    def get_error_string(self):
        str = ''
        str += f"ODRIVE ERRORS: {'no errors' if not self.has_errors() else ''}\n"
        errors = self.get_errors()
        for error in errors:
            if error.errors:
                str += f'{error.name}: {error.errors}\n'
        return str


    def has_errors(self):
        errors = self.get_errors()
        for error in errors:
            if error.errors: return True
        return False


class ErrorType:

    def __init__( self, name, error_codes, path) -> None:
        self.name = name
        self.error_codes = error_codes
        self.path = path
        self.errors = []

    def get_errors(self):
        self.errors = []
        err = self.path.__getattribute__('error')
        for err_code in self.error_codes.keys():
            if err_code & err != 0:
                self.errors.append(self.error_codes[err_code])