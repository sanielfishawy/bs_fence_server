import time
import odrive
from odrive.enums import *


class OdriveWrapper:

    def __init__(
        self,
        axis=0,
    ):
        self.odrive = odrive.find_any()
        self.axis = self.odrive.axis0 if axis == 0 else self.odrive.axis1

    def calibrate_motor_and_save(self):
        self.axis.requested_state = AXIS_STATE_MOTOR_CALIBRATION
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)
        self.axis.motor.config.pre_calibrated = True
        self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
        self.odrive.save_configuration()

    def calibrate_encoder(self):
        self.axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        while self.axis.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

    def run(self):
        self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    def stop(self):
        self.axis.requested_state = AXIS_STATE_IDLE


if __name__ == '__main__':
    o = OdriveWrapper()
    pass



