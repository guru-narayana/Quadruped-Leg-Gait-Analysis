#!/usr/bin/env python


from kinematics import leg_ik
import time
import rospy
from std_msgs.msg import Float64

def linear_motion(height = 0.32 , speed = 0.09):
    pub1 = rospy.Publisher('/leg_sim/J1_position_controller/command', Float64, queue_size=10)
    pub2 = rospy.Publisher('/leg_sim/J2_position_controller/command', Float64, queue_size=10)
    rospy.init_node('Leg_linear_controller', anonymous=True)
    rate = rospy.Rate(100)
    x = 0.16
    while not rospy.is_shutdown():
        time = rospy.get_time()
        while(x <= height) and not rospy.is_shutdown():
            x = 0.16  + speed*(rospy.get_time()-time)
            theta = leg_ik([x,0])

            print(x)
            pub1.publish(theta[0])
            pub2.publish(theta[1])
            rate.sleep()
        time = rospy.get_time()
        while(x >= 0.16) and not rospy.is_shutdown():
            x = height  - speed*(rospy.get_time()-time)
            theta = leg_ik([x,0])
            print(x)
            pub1.publish(theta[0])
            pub2.publish(theta[1])
            rate.sleep()

if __name__ == '__main__':
    try:
        linear_motion()
    except rospy.ROSInterruptException:
        pass