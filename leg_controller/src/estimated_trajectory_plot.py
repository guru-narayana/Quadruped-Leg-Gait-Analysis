from jumping_trajectory_generator import *
import time
import numpy as np
import time
from kinematics import *
import matplotlib.pyplot as plt

h1 = 0.10
H = 0.35
[theta1,theta2] = leg_ik([h1,0])
T = 1
a = base_jump_trajectory(theta1,theta2,H,T)

H1 = 0.21


b,joint_swing_times = swing_joint_traj(a,H1)


Time_array = np.linspace(0,T,1000)
com_height = []
end_point_height = []
for t in Time_array:
    com_height.append(base_current_traj_joint_value(t,a))
    if t>=joint_swing_times[0] and t<=joint_swing_times[1]:
        end_point_height.append(b[1]*(t-joint_swing_times[0]) + b[2]*(t-joint_swing_times[0])**2)
    else:
        end_point_height.append(0)
plt.plot(Time_array,end_point_height)
plt.plot(Time_array,com_height)
plt.show()
print(com_height[0])