import logging
from odrive_motor.stop_finder import StopFinder
from odrive_motor.odrive_wrapper import OdriveWrapper
from odrive_motor.motor_config import MotorConfig
from odrive_motor.odrive_error import OdriveError


logging.basicConfig(level=logging.DEBUG)

MotorConfig(MotorConfig.MOTOR_D5065, 0).save_config_to_file()
MotorConfig(MotorConfig.MOTOR_BLY171D, 1).save_config_to_file()
# ow = OdriveWrapper(axis=1, motor=MotorConfig.MOTOR_BLY171D)

# sf = StopFinder(odrive_wrapper=ow, log_level=logging.DEBUG)

# ow.encoder_index_search()
# ow.calibrate_encoder_and_save(force=True)
# ow.run(velocity_limit=30)
# ow.stop()

