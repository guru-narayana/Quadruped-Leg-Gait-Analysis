#!/usr/bin/env python3

import time
import numpy as np
import odrive
from odrive.enums import *
import rospy
from std_msgs.msg import Float64

odrv0 = odrive.find_any()
axis0  = odrv0.axis0
axis1  = odrv0.axis1

axis0.requested_state = AXIS_STATE_IDLE
axis1.requested_state = AXIS_STATE_IDLE

def exit_func():
    print("Shutting Down")
    axis0.requested_state = AXIS_STATE_IDLE
    axis1.requested_state = AXIS_STATE_IDLE

def callback_axis0(data):
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    angle = data.data
    rotations = ((angle)/(3.14*2))*6
    axis0.controller.input_pos = rotations
    
def callback_axis1(data):
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    angle = data.data
    rotations = (angle/(3.14*2))*6
    axis1.controller.input_pos = rotations

rospy.init_node('leg_driver', anonymous=True)
rospy.on_shutdown(exit_func)

axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

rospy.Subscriber("/leg_sim/J2_position_controller/command", Float64, callback_axis0)
rospy.Subscriber("/leg_sim/J1_position_controller/command", Float64, callback_axis1)


rospy.spin()
