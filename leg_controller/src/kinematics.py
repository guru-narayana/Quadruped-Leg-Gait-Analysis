import numpy as np
import math

l1 = 0.17
l2 = 0.18

def leg_ik(pos):
    x = pos[0]
    y = pos[1]
    val1 = x**2 + y**2 -l1**2 - l2**2
    val2 = 2*l1*l2
    delta = np.sqrt(val2**2 - val1**2)
    theta2 = math.atan2(delta,val1)
    theta1 = math.atan2(y,x) - math.atan2(l2*math.sin(theta2),l1+l2*math.cos(theta2))
    return np.array([theta1,theta2])

def leg_fk(theta):
    theta1 = theta[0]
    theta2 = theta[1]
    x = l1*math.cos(theta1) + l2*math.cos(theta1+theta2)
    y = l1*math.sin(theta1) + l2*math.sin(theta1+theta2)
    return np.array([x,y])

if __name__ == '__main__':
    print(leg_ik([0.16,0]))