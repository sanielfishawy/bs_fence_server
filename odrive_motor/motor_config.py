import logging
import odrive
from odrive.enums import *
from .odrive_error import OdriveError

class MotorConfig:

    MOTOR_BLY171D = 'bly_171_d'
    MOTOR_D5065 = 'd5065'

    def __init__(self, motor, axis, odrv: odrive=None,) -> None:
        self.motor = motor
        self.odrive = odrv or odrive.find_any()
        self.axis = self.odrive.axis0 if axis == 0 else self.odrive.axis1
        self.oe = OdriveError(odrv=self.odrive, axis=axis)
    
    def configure_and_save(self):
        if self.motor == self.__class__.MOTOR_BLY171D:
            self.configure_bly_171_d()
            self.odrive.save_configuration()

    def configure_bly_171_d(self):
        self.oe.log_errors()
        self.axis.motor.config.pole_pairs = 4
        self.axis.motor.config.calibration_current = 0.25
        self.axis.motor.config.resistance_calib_max_voltage = 15
        self.axis.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
        self.axis.motor.config.current_lim = 60
        self.axis.controller.config.vel_integrator_gain = 0
        self.axis.encoder.config.use_index=True

        self.axis.config.startup_motor_calibration = False
        self.axis.config.startup_encoder_index_search = True
        self.axis.config.startup_encoder_offset_calibration = False
        self.axis.config.startup_closed_loop_control = False
        self.axis.config.startup_sensorless_control = False

        self.axis.controller.config.pos_gain = 200
        self.axis.controller.config.vel_gain = .005
        self.axis.motor.config.torque_constant = .065
    
    def save_config_to_file(self):
        txt  = 'AXIS CONFIGURATION:\n'
        txt += '-------------------\n'
        txt += str(self.axis.config)
        txt += '\n\n\n'
        txt += 'MOTOR CONFIGURATION:\n'
        txt += '--------------------\n'
        txt += str(self.axis.motor.config)
        txt += '\n\n\n'
        txt += 'CONTROLLER CONFIGURATION:\n'
        txt += '-------------------------\n'
        txt += str(self.axis.controller.config)
        txt += '\n\n\n'
        txt += 'ENCODER CONFIGURATION:\n'
        txt += '----------------------\n'
        txt += str(self.axis.encoder.config)

        with open(f'{self.motor}_config.txt', 'w') as writer:
            writer.write(txt)






