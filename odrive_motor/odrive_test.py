"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
o = odrive.find_any()
a = o.axis0

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#my_drive = odrive.find_any("serial:/dev/ttyUSB0")

# Calibrate motor and wait for it to finish
print("starting calibration...")
o.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while o.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

a = o.axis0
c = a.controller
o.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
o.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# To read a value, simply read the property
print("Bus voltage is " + str(o.vbus_voltage) + "V")

# Or to change a value, just assign to the property
o.axis0.controller.input_pos = 3.14
print("Position setpoint is " + str(o.axis0.controller.pos_setpoint))

# And this is how function calls are done:
for i in [1,2,3,4]:
    print('voltage on GPIO{} is {} Volt'.format(i, o.get_adc_voltage(i)))

# A sine wave to test
t0 = time.monotonic()
while True:
    setpoint = 10000.0 * math.sin((time.monotonic() - t0)*2)
    print("goto " + str(int(setpoint)))
    o.axis0.controller.pos_setpoint = setpoint
    time.sleep(0.01)