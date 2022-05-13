import odrive
from odrive.enums import *
import time
import math

odrv0 = odrive.find_any()
#odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
#time.sleep(20)
odrv0.axis0.requested_state = AXIS_STATE_IDLE

if(odrv0.vbus_voltage<22):
    print("Vbus voltage is too low. Please check the connection.")
    exit()
else:
    print("Vbus voltage is ok")

odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

odrv0.axis0.controller.input_pos = 0
for i in range(1000):
    #print(odrv0.axis0.encoder.pos_estimate)
    print(odrv0.axis0.motor.current_control.Iq_measured)

    time.sleep(0.1)
odrv0.axis0.requested_state = AXIS_STATE_IDLE
