#!/usr/bin/env python3

import odrive
from odrive.enums import *
import time

odrv0 = odrive.find_any()
if(odrv0.vbus_voltage<22):
    print("Vbus voltage is too low. Please check the connection.")
    exit()
else:
    print("Vbus voltage is ok")


axis  = odrv0.axis0
axis.requested_state = AXIS_STATE_IDLE
axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
time.sleep(15)
axis.requested_state = AXIS_STATE_IDLE

axis  = odrv0.axis1
axis.requested_state = AXIS_STATE_IDLE
axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
time.sleep(15)
axis.requested_state = AXIS_STATE_IDLE