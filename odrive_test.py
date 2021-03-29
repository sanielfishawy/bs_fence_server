import logging
from odrive_motor.stop_finder import StopFinder
from odrive_motor.odrive_wrapper import OdriveWrapper

ow = OdriveWrapper()
sf = StopFinder(odrive_wrapper=ow, log_level=logging.DEBUG)
oe = ow.odrive_error

# ow.encoder_index_search()
# ow.calibrate_encoder_and_save(force=True)
ow.run(velocity_limit=30)
pass

