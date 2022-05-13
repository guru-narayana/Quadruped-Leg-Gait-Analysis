#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from jumping_trajectory_generator import *
import numpy as np
import time
from kinematics import *
from sensor_msgs.msg import JointState





### target variables



h1 = 0.10 ## intial height of base frame from grounf
H = 0.4 ## jump height required
[theta1,theta2] = leg_ik([h1,0])  
T = 0.5 # total time to perform jump in sec
H1 = 0.21 # height end point of the leg show reach in the jump
a = base_jump_trajectory(theta1,theta2,H,T)
b,joint_swing_times = swing_joint_traj(a,H1)




### initialization

rospy.init_node('jumping_trajectory_exe', anonymous=True)
current_joints_state = []
pub1 = rospy.Publisher('/leg_sim/J1_position_controller/command', Float64, queue_size=10)
pub2 = rospy.Publisher('/leg_sim/J2_position_controller/command', Float64, queue_size=10)
def callback_current_joint_state(jnt):
    global current_joints_state
    current_joints_state = jnt.position

### getting ready for the jumping, reaching to the home position

rospy.Subscriber("/leg_sim/joint_states", JointState, callback_current_joint_state)
while current_joints_state == []:
    if rospy.is_shutdown():
        break
[intial_x,_] = leg_fk(current_joints_state)
vel = 0.06
Time_temporary = abs(h1-intial_x)/vel
intial_time = rospy.get_time()
while (rospy.get_time() - intial_time) < Time_temporary:
    x = intial_x + np.sign(h1-intial_x)*vel*(rospy.get_time() - intial_time)
    [theta1,theta2] = leg_ik([x,0])    
    pub1.publish(theta1)
    pub2.publish(theta2)

### jumping till leg swing phase
intial_time = rospy.get_time()
while (rospy.get_time()-intial_time) < joint_swing_times[0]:
    t = (rospy.get_time()-intial_time)
    x = base_current_traj_joint_value(t,a) + dist*np.cos(current_joints_state[0])
    [theta1,theta2] = leg_ik([x,0])    
    pub1.publish(theta1)
    pub2.publish(theta2)    
x_jump_phase = x
### leg swing phase
while (rospy.get_time()-intial_time) > joint_swing_times[0] and (rospy.get_time()-intial_time) < joint_swing_times[1]:
    t = (rospy.get_time()-intial_time) - joint_swing_times[0]
    x = x_jump_phase - b[1]*t - b[2]*(t**2) 
    [theta1,theta2] = leg_ik([x,0])    
    pub1.publish(theta1)
    pub2.publish(theta2)


# landing trajectory
# while (rospy.get_time()-intial_time) > joint_swing_times[1] and (rospy.get_time()-intial_time) <T:
#     t = (rospy.get_time()-intial_time)
#     x = base_current_traj_joint_value(t,a) + dist*np.cos(current_joints_state[0])
#     print(x)
#     [theta1,theta2] = leg_ik([x,0])    
#     pub1.publish(theta1)
#     pub2.publish(theta2) 