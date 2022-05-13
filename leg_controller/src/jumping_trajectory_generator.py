import numpy as np
from kinematics import leg_fk, leg_ik
base_link_mass = 800
actuator_mass = 500
l1 = 0.17
l2 = 0.18

dist = (actuator_mass*l1)/(base_link_mass+actuator_mass)

def com_jump_traj(h1,H,T):
    a0 = h1
    a1 = 0
    a2 = (16*(H-h1))/T**2
    a3 = -((32*(H-h1))/T**3) #+ 1.634
    a4 = (16*(H-h1))/T**4
    return [a0,a1,a2,a3,a4]

def base_jump_trajectory(theta1,theta2,H,T):
    h1 = leg_fk([theta1,theta2])[0] - dist*np.cos(theta1)
    a = com_jump_traj(h1,H,T)
    return a

def base_current_traj_joint_value(t,a):
    x = a[0] + a[1]*t + a[2]*t**2 + a[3]*t**3+ a[4]*t**4
    return x

def swing_joint_traj(a,H1):
    t1 = (-6*a[3] - (np.sqrt((6*a[3])**2  - 4*2*a[2]*12*a[4])))/(2*12*a[4])
    t2 = (-6*a[3] + (np.sqrt((6*a[3])**2  - 4*2*a[2]*12*a[4])))/(2*12*a[4])
    T = t2 - t1
    b0 = 0
    b1 = (4*H1)/T
    b2 = (-4*H1)/(T**2)
    return [b0,b1,b2],[t1,t2]

    

